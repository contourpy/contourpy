# Test internal API defined in wrap.cpp, mostly constructors. These are not normally called from
# client code as contour_generator() defined in Python is preferred.

from __future__ import annotations

from io import StringIO
import sys
from typing import TYPE_CHECKING

import pytest

from contourpy._contourpy import (
    ContourGenerator, FillType, LineType, Mpl2005ContourGenerator, Mpl2014ContourGenerator,
    SerialContourGenerator, ThreadedContourGenerator, ZInterp,
)

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    KWArgs: TypeAlias = dict[str, int | bool | LineType | FillType | ZInterp]
    XYZMask: TypeAlias = tuple[list[list[int]], list[list[int]], list[list[int]], None]


def all_classes() -> list[type[ContourGenerator]]:
    return [Mpl2005ContourGenerator, Mpl2014ContourGenerator, SerialContourGenerator,
            ThreadedContourGenerator]


def default_kwargs(cls: type[ContourGenerator]) -> KWArgs:
    kwargs: KWArgs = {
        "x_chunk_size": 0,
        "y_chunk_size": 0,
    }

    if cls == Mpl2005ContourGenerator:
        pass
    elif cls == Mpl2014ContourGenerator:
        kwargs["corner_mask"] = True
    else:
        kwargs.update({
            "line_type": LineType.Separate,
            "fill_type": FillType.OuterOffset,
            "corner_mask": True,
            "quad_as_tri": False,
            "z_interp": ZInterp.Linear,
        })
        if cls == ThreadedContourGenerator:
            kwargs["thread_count"] = 1
    return kwargs


@pytest.fixture
def xyz_mask() -> XYZMask:
    x = [[0, 1], [0, 1]]
    y = [[0, 0], [1, 1]]
    z = [[1, 2], [3, 4]]
    return x, y, z, None


@pytest.mark.parametrize("cls", all_classes())
def test_default(cls: type[ContourGenerator], xyz_mask: XYZMask) -> None:
    kwargs = default_kwargs(cls)
    cls(*xyz_mask, **kwargs)


@pytest.mark.parametrize("cls", all_classes())
def test_xyz_ndim(cls: type[ContourGenerator], xyz_mask: XYZMask) -> None:
    x, y, z, mask = xyz_mask
    one_d = [1]
    three_d = [[[1]]]
    kwargs = default_kwargs(cls)
    msg = "x, y and z must all be 2D arrays"

    with pytest.raises(ValueError, match=msg):
        cls(one_d, y, z, mask, **kwargs)
    with pytest.raises(ValueError, match=msg):
        cls(three_d, y, z, mask, **kwargs)

    with pytest.raises(ValueError, match=msg):
        cls(x, one_d, z, mask, **kwargs)
    with pytest.raises(ValueError, match=msg):
        cls(x, three_d, z, mask, **kwargs)

    with pytest.raises(ValueError, match=msg):
        cls(x, y, one_d, mask, **kwargs)
    with pytest.raises(ValueError, match=msg):
        cls(x, y, three_d, mask, **kwargs)


@pytest.mark.parametrize("cls", all_classes())
def test_xyz_shape(cls: type[ContourGenerator], xyz_mask: XYZMask) -> None:
    x, y, z, mask = xyz_mask
    diff_shape = [[0, 1], [2, 3], [4, 5]]
    kwargs = default_kwargs(cls)
    msg = "x, y and z arrays must have the same shape"

    with pytest.raises(ValueError, match=msg):
        cls(diff_shape, y, z, mask, **kwargs)
    with pytest.raises(ValueError, match=msg):
        cls(x, diff_shape, z, mask, **kwargs)
    with pytest.raises(ValueError, match=msg):
        cls(x, y, diff_shape, mask, **kwargs)


@pytest.mark.parametrize("cls", all_classes())
def test_xy_at_least_2x2(cls: type[ContourGenerator]) -> None:
    kwargs = default_kwargs(cls)
    msg = "x, y and z must all be at least 2x2 arrays"

    with pytest.raises(ValueError, match=msg):
        cls([[1, 2]], [[1, 2]], [[1, 2]], None, **kwargs)
    with pytest.raises(ValueError, match=msg):
        cls([[1], [2]], [[1], [2]], [[1], [2]], None, **kwargs)


@pytest.mark.parametrize("cls", all_classes())
def test_mask_2d(cls: type[ContourGenerator], xyz_mask: XYZMask) -> None:
    x, y, z, _ = xyz_mask
    kwargs = default_kwargs(cls)
    msg = "mask array must be a 2D array"

    with pytest.raises(ValueError, match=msg):
        cls(x, y, z, [False, True], **kwargs)
    with pytest.raises(ValueError, match=msg):
        cls(x, y, z, [[[False, True]]], **kwargs)


@pytest.mark.parametrize("cls", all_classes())
def test_mask_shape(cls: type[ContourGenerator], xyz_mask: XYZMask) -> None:
    x, y, z, _ = xyz_mask
    kwargs = default_kwargs(cls)
    msg = "If mask is set it must be a 2D array with the same shape as z"

    with pytest.raises(ValueError, match=msg):
        cls(x, y, z, [[False, True]], **kwargs)
    with pytest.raises(ValueError, match=msg):
        cls(x, y, z, [[False], [True]], **kwargs)


@pytest.mark.parametrize("cls", all_classes())
def test_chunk_size_not_negative(cls: type[ContourGenerator], xyz_mask: XYZMask) -> None:
    x, y, z, mask = xyz_mask
    kwargs = default_kwargs(cls)
    msg = "x_chunk_size and y_chunk_size cannot be negative"

    x_kwargs = kwargs.copy()
    x_kwargs.update({"x_chunk_size": -1})
    with pytest.raises(ValueError, match=msg):
        cls(x, y, z, mask, **x_kwargs)

    y_kwargs = kwargs.copy()
    y_kwargs.update({"y_chunk_size": -1})
    with pytest.raises(ValueError, match=msg):
        cls(x, y, z, mask, **y_kwargs)


@pytest.mark.parametrize("cls", [SerialContourGenerator, ThreadedContourGenerator])
def test_log_z_not_negative(cls: type[ContourGenerator], xyz_mask: XYZMask) -> None:
    x, y, _, mask = xyz_mask
    kwargs = default_kwargs(cls)
    kwargs["z_interp"] = ZInterp.Log
    msg = "z values must be positive if using ZInterp.Log"

    z = [[0, 1],[2, 3]]
    with pytest.raises(ValueError, match=msg):
        cls(x, y, z, mask, **kwargs)

    # Ignore z that are masked out
    mask = [[True, False], [False, False]]
    cls(x, y, z, mask, **kwargs)


@pytest.mark.skipif(sys.platform not in ("darwin", "linux"), reason="sysout redirect not available")
@pytest.mark.parametrize("cls", [SerialContourGenerator, ThreadedContourGenerator])
def test_write_cache(cls: type[ContourGenerator], xyz_mask: XYZMask) -> None:
    from wurlitzer import STDOUT, pipes

    x, y, z, _ = xyz_mask
    mask = [[False, False], [False, True]]
    kwargs = default_kwargs(cls)

    cg = cls(x, y, z, mask, **kwargs)

    cg.filled(2.5, 3.5)
    out = StringIO()
    with pipes(stdout=out, stderr=STDOUT):
        cg._write_cache()  # type: ignore[attr-defined]
    assert out.getvalue() == \
        "---------- Cache ----------\n" \
        "j=1 ...e10....... .SW.20.w..... \n" \
        "j=0 ....00....... ...n00....... \n" \
        "    i=0           i=1           \n" \
        "---------------------------\n"

    cg.lines(2.5)
    out = StringIO()
    with pipes(stdout=out, stderr=STDOUT):
        cg._write_cache()  # type: ignore[attr-defined]
    assert out.getvalue() == \
        "---------- Cache ----------\n" \
        "j=1 ...e10....... .SW.10.w..... \n" \
        "j=0 ....00....... ...n00....... \n" \
        "    i=0           i=1           \n" \
        "---------------------------\n"
