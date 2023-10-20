from __future__ import annotations

from typing import TYPE_CHECKING, cast

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal
import pytest

from contourpy import LineType, contour_generator
from contourpy.util.data import random, simple

from . import util_test

if TYPE_CHECKING:
    import contourpy._contourpy as cpy


@pytest.fixture
def xy_2x2() -> tuple[cpy.CoordinateArray, ...]:
    x, y = np.meshgrid([0.0, 1.0], [0.0, 1.0])
    return x, y


@pytest.fixture
def xy_3x3() -> tuple[cpy.CoordinateArray, ...]:
    x, y = np.meshgrid([0.0, 0.5, 1.0], [0.0, 0.5, 1.0])
    return x, y


@pytest.fixture
def one_loop_one_strip() -> tuple[cpy.PointArray, ...]:
    x, y = np.meshgrid([0., 1., 2., 3.], [0., 1., 2.])
    z = np.array([[1.5, 1.5, 0.9, 0.0],
                  [1.5, 2.8, 0.4, 0.8],
                  [0.0, 0.0, 0.8, 6.0]])
    return x, y, z


@pytest.fixture
def xyz_chunk_test() -> tuple[cpy.CoordinateArray, ...]:
    x, y = np.meshgrid(np.arange(5), np.arange(5))
    z = 0.5*np.abs(y - 2) + 0.1*(x - 2)
    return x, y, z


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("zlevel", [-1e-10, 1.0+1e10, np.nan, -np.nan, np.inf, -np.inf])
def test_level_outside(xy_2x2: tuple[cpy.CoordinateArray, ...], name: str, zlevel: float) -> None:
    x, y = xy_2x2
    z = x
    cont_gen = contour_generator(x, y, z, name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(zlevel)
    if TYPE_CHECKING:
        lines = cast(cpy.LineReturn_SeparateCode, lines)
    assert isinstance(lines, tuple) and len(lines) == 2
    points, codes = lines
    assert isinstance(points, list) and len(points) == 0
    assert isinstance(codes, list) and len(codes) == 0


@pytest.mark.parametrize("name", util_test.all_names())
def test_w_to_e(xy_2x2: tuple[cpy.CoordinateArray, ...], name: str) -> None:
    x, y = xy_2x2
    z = y.copy()
    cont_gen = contour_generator(x, y, z, name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(0.5)
    if TYPE_CHECKING:
        lines = cast(cpy.LineReturn_SeparateCode, lines)
    assert isinstance(lines, tuple) and len(lines) == 2
    points, codes = lines
    assert isinstance(points, list) and len(points) == 1
    assert isinstance(codes, list) and len(codes) == 1
    assert_allclose(points[0], [[0.0, 0.5], [1.0, 0.5]])
    assert_array_equal(codes[0], [1, 2])


@pytest.mark.parametrize("name", util_test.all_names())
def test_e_to_w(xy_2x2: tuple[cpy.CoordinateArray, ...], name: str) -> None:
    x, y = xy_2x2
    z = 1.0 - y.copy()
    cont_gen = contour_generator(x, y, z, name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(0.5)
    if TYPE_CHECKING:
        lines = cast(cpy.LineReturn_SeparateCode, lines)
    assert isinstance(lines, tuple) and len(lines) == 2
    points, codes = lines
    assert isinstance(points, list) and len(points) == 1
    assert isinstance(codes, list) and len(codes) == 1
    if name == "mpl2005":    # Line directions are not consistent.
        assert_allclose(points[0], [[0.0, 0.5], [1.0, 0.5]])
    else:
        assert_allclose(points[0], [[1.0, 0.5], [0.0, 0.5]])
    assert_array_equal(codes[0], [1, 2])


@pytest.mark.parametrize("name", util_test.all_names())
def test_loop(xy_3x3: tuple[cpy.CoordinateArray, ...], name: str) -> None:
    x, y = xy_3x3
    z = np.zeros_like(x)
    z[1, 1] = 1.0
    cont_gen = contour_generator(x, y, z, name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(0.5)
    if TYPE_CHECKING:
        lines = cast(cpy.LineReturn_SeparateCode, lines)
    assert isinstance(lines, tuple) and len(lines) == 2
    points, codes = lines
    assert isinstance(points, list) and len(points) == 1
    assert isinstance(codes, list) and len(codes) == 1
    line = points[0]
    assert line.shape == (5, 2)
    assert_allclose(line[0], line[-1])
    assert_array_equal(codes[0], [1, 2, 2, 2, 79])


@pytest.mark.image
@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_simple(name: str, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40))
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_simple_chunk(name: str, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40))
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, chunk_size=2, thread_count=1,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_chunk.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_lines_simple_chunk_threads(line_type: LineType, thread_count: int) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40))
    cont_gen = contour_generator(
        x, y, z, name="threaded", line_type=line_type, chunk_size=2, thread_count=thread_count,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_chunk.png", f"{line_type}_{thread_count}")


@pytest.mark.image
@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_simple_no_corner_mask(name: str, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type, corner_mask=False)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_no_corner_mask.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_simple_no_corner_mask_chunk(name: str, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, corner_mask=False, chunk_size=2, thread_count=1,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_no_corner_mask_chunk.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_lines_simple_no_corner_mask_chunk_threads(line_type: LineType, thread_count: int) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(
        x, y, z, name="threaded", line_type=line_type, corner_mask=False, chunk_size=2,
        thread_count=thread_count,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "lines_simple_no_corner_mask_chunk.png", f"{line_type}_{thread_count}",
    )


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_lines_simple_corner_mask(name: str) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    line_type = LineType.SeparateCode
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type, corner_mask=True)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_corner_mask.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_lines_simple_corner_mask_chunk(name: str) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    line_type = LineType.SeparateCode
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, corner_mask=True, chunk_size=2, thread_count=1,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_corner_mask_chunk.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_lines_simple_corner_mask_chunk_threads(line_type: LineType, thread_count: int) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40), want_mask=True)
    cont_gen = contour_generator(
        x, y, z, name="threaded", line_type=line_type, corner_mask=True, chunk_size=2,
        thread_count=thread_count,
    )
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "lines_simple_corner_mask_chunk.png", f"{line_type}_{thread_count}",
    )


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_lines_simple_quad_as_tri(name: str) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = simple((30, 40))
    cont_gen = contour_generator(x, y, z, name=name, quad_as_tri=True)
    levels = np.arange(-1.0, 1.01, 0.1)

    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1
    assert cont_gen.quad_as_tri

    line_type = cont_gen.line_type
    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_simple_quad_as_tri.png", f"{name}")


@pytest.mark.image
@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_random(name: str, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random.png", f"{name}_{line_type}", max_threshold=103)


@pytest.mark.image
@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_random_chunk(name: str, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, chunk_size=2, thread_count=1,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    max_threshold = None
    mean_threshold = None
    if name == "mpl2005":
        max_threshold = 126
        mean_threshold = 0.11

    compare_images(
        image_buffer, "lines_random_chunk.png", f"{name}_{line_type}",
        max_threshold=max_threshold, mean_threshold=mean_threshold,
    )


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_lines_random_chunk_threads(line_type: LineType, thread_count: int) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(
        x, y, z, name="threaded", line_type=line_type, chunk_size=2, thread_count=thread_count,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "lines_random_chunk.png", f"{line_type}_{thread_count}",
    )


@pytest.mark.image
@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_random_no_corner_mask(name: str, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type, corner_mask=False)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_no_corner_mask.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
def test_lines_random_no_corner_mask_chunk(name: str, line_type: LineType) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    if name in ("mpl2005"):
        pytest.skip()  # mpl2005 does not support chunks for lines.

    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, corner_mask=False, chunk_size=2, thread_count=1,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_no_corner_mask_chunk.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_lines_random_no_corner_mask_chunk_threads(line_type: LineType, thread_count: int) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name="threaded", line_type=line_type, corner_mask=False, chunk_size=2,
        thread_count=thread_count,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "lines_random_no_corner_mask_chunk.png", f"{line_type}_{thread_count}",
    )


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_lines_random_corner_mask(name: str) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    line_type = LineType.SeparateCode
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=True, line_type=line_type)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_corner_mask.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.corner_mask_names())
def test_lines_random_corner_mask_chunk(name: str) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    line_type = LineType.SeparateCode
    cont_gen = contour_generator(
        x, y, z, name=name, corner_mask=True, line_type=line_type, chunk_size=2, thread_count=1,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == 1

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_corner_mask_chunk.png", f"{name}_{line_type}")


@pytest.mark.image
@pytest.mark.threads
@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("thread_count", util_test.thread_counts())
def test_lines_random_corner_mask_chunk_threads(line_type: LineType, thread_count: int) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.05)
    cont_gen = contour_generator(
        x, y, z, name="threaded", corner_mask=True, line_type=line_type, chunk_size=2,
        thread_count=thread_count,
    )
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (15, 20)
    assert cont_gen.thread_count == thread_count

    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(
        image_buffer, "lines_random_corner_mask_chunk.png", f"{line_type}_{thread_count}",
    )


@pytest.mark.image
@pytest.mark.parametrize("name", util_test.quad_as_tri_names())
def test_lines_random_quad_as_tri(name: str) -> None:
    from contourpy.util.mpl_renderer import MplTestRenderer

    from .image_comparison import compare_images

    x, y, z = random((30, 40), mask_fraction=0.0)
    cont_gen = contour_generator(x, y, z, name=name, quad_as_tri=True)
    levels = np.arange(0.0, 1.01, 0.2)

    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1
    assert cont_gen.quad_as_tri

    line_type = cont_gen.line_type
    renderer = MplTestRenderer()
    for i in range(len(levels)):
        renderer.lines(cont_gen.lines(levels[i]), line_type, color=f"C{i}")
    image_buffer = renderer.save_to_buffer()

    compare_images(image_buffer, "lines_random_quad_as_tri.png", f"{name}")


@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("name", ["serial", "threaded"])
def test_return_by_line_type(
    one_loop_one_strip: tuple[cpy.PointArray, ...],
    name: str,
    line_type: LineType,
) -> None:
    x, y, z = one_loop_one_strip
    cont_gen = contour_generator(x, y, z, name=name, line_type=line_type)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1

    lines = cont_gen.lines(2.0)

    util_test.assert_lines(lines, line_type)

    if line_type == LineType.Separate:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_Separate, lines)
        points = lines
        assert len(points) == 2
        assert points[0].shape == (5, 2)
        assert points[1].shape == (2, 2)
    elif line_type == LineType.SeparateCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_SeparateCode, lines)
        points, codes = lines
        assert len(points) == 2
        assert points[0].shape == (5, 2)
        assert points[1].shape == (2, 2)
        assert_array_equal(codes[0], [1, 2, 2, 2, 79])
        assert_array_equal(codes[1], [1, 2])
    elif line_type == LineType.ChunkCombinedCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedCode, lines)
        assert len(lines[0]) == 1  # Single chunk.
        points_or_none, codes_or_none = lines[0][0], lines[1][0]
        assert points_or_none is not None
        assert codes_or_none is not None
        assert points_or_none.shape == (7, 2)
        assert_array_equal(codes_or_none, [1, 2, 2, 2, 79, 1, 2])
    elif line_type == LineType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedOffset, lines)
        assert len(lines[0]) == 1  # Single chunk.
        points_or_none, offsets_or_none = lines[0][0], lines[1][0]
        assert points_or_none is not None
        assert offsets_or_none is not None
        assert points_or_none.shape == (7, 2)
        assert_array_equal(offsets_or_none, [0, 5, 7])
    elif line_type == LineType.ChunkCombinedNan:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedNan, lines)
        assert len(lines[0]) == 1  # Single chunk
        points_or_none = lines[0][0]
        assert points_or_none is not None
        assert points_or_none.shape == (8, 2)
        assert np.all(np.isnan(points_or_none[5, :]))
    else:
        raise RuntimeError(f"Unexpected line_type {line_type}")


@pytest.mark.threads
@pytest.mark.parametrize("line_type", LineType.__members__.values())
@pytest.mark.parametrize("name, thread_count",
                         [("serial", 1), ("threaded", 1), ("threaded", 2)])
def test_return_by_line_type_chunk(
    xyz_chunk_test: tuple[cpy.CoordinateArray, ...],
    name: str,
    thread_count: int,
    line_type: LineType,
) -> None:
    x, y, z = xyz_chunk_test
    cont_gen = contour_generator(
        x, y, z, name=name, line_type=line_type, chunk_count=2, thread_count=thread_count,
    )

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (2, 2)
    assert cont_gen.chunk_size == (2, 2)
    assert cont_gen.thread_count == thread_count

    lines = cont_gen.lines(0.45)

    util_test.assert_lines(lines, line_type)

    # Expected points by chunk.
    expected: list[cpy.PointArray] = [
        np.asarray([[2.0, 1.1], [1.5, 1.0], [1.0, 0.9], [0.0, 0.7]]),
        np.asarray([[4.0, 1.5], [3.0, 1.3], [2.0, 1.1]]),
        np.asarray([[0.0, 3.3], [1.0, 3.1], [1.5, 3.0], [2.0, 2.9]]),
        np.asarray([[2.0, 2.9], [3.0, 2.7], [4.0, 2.5]]),
    ]

    if line_type == LineType.Separate:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_Separate, lines)
        assert len(lines) == 4
        if name == "threaded" and cont_gen.thread_count > 1:
            # Lines may be in any order so sort lines and expected.
            lines = util_test.sort_by_first_xy(lines)
            expected = util_test.sort_by_first_xy(expected)
        for chunk in range(4):
            assert_allclose(lines[chunk], expected[chunk])
    elif line_type == LineType.SeparateCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_SeparateCode, lines)
        assert len(lines[0]) == 4
        if name == "threaded" and cont_gen.thread_count > 1:
            # Lines may be in any order so sort lines and expected.
            lines = util_test.sort_by_first_xy(lines[0], lines[1])
            expected = util_test.sort_by_first_xy(expected)
        for chunk in range(4):
            assert_allclose(lines[0][chunk], expected[chunk])
            assert_array_equal(lines[1][chunk], [1] + [2]*(len(expected[chunk])-1))
    elif line_type == LineType.ChunkCombinedCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedCode, lines)
        assert len(lines[0]) == 4
        for chunk in range(4):
            points_or_none, codes_or_none = lines[0][chunk], lines[1][chunk]
            assert points_or_none is not None
            assert codes_or_none is not None
            assert_allclose(points_or_none, expected[chunk])
            assert_array_equal(codes_or_none, [1] + [2]*(len(expected[chunk])-1))
    elif line_type == LineType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedOffset, lines)
        assert len(lines[0]) == 4
        for chunk in range(4):
            points_or_none, offsets_or_none = lines[0][chunk], lines[1][chunk]
            assert points_or_none is not None
            assert offsets_or_none is not None
            assert_allclose(points_or_none, expected[chunk])
            assert_array_equal(offsets_or_none, [0, len(expected[chunk])])
    elif line_type == LineType.ChunkCombinedNan:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedNan, lines)
        assert len(lines[0]) == 4
        for chunk in range(4):
            # Only a single line per chunk, so no nans here.
            points_or_none = lines[0][chunk]
            assert points_or_none is not None
            assert_allclose(points_or_none, expected[chunk])
    else:
        raise RuntimeError(f"Unexpected line_type {line_type}")


@pytest.mark.parametrize("name, line_type", util_test.all_names_and_line_types())
@pytest.mark.parametrize("corner_mask", [None, False, True])
def test_lines_random_big(name: str, line_type: LineType, corner_mask: bool) -> None:
    if corner_mask and name in ["mpl2005", "mpl2014"]:
        pytest.skip()

    x, y, z = random((1000, 1000), mask_fraction=0.0 if corner_mask is None else 0.05)
    cont_gen = contour_generator(x, y, z, name=name, corner_mask=corner_mask, line_type=line_type)
    levels = np.arange(0.0, 1.01, 0.1)

    assert cont_gen.line_type == line_type
    assert cont_gen.chunk_count == (1, 1)
    assert cont_gen.thread_count == 1

    for level in levels:
        lines = cont_gen.lines(level)
        util_test.assert_lines(lines, line_type)


@pytest.mark.parametrize("name", util_test.all_names())
@pytest.mark.parametrize("z", [np.nan, -np.nan, np.inf, -np.inf])
@pytest.mark.parametrize("zlevel", [0.0, np.nan, -np.nan, np.inf, -np.inf])
def test_lines_z_nonfinite(name: str, z: float, zlevel: float) -> None:
    cont_gen = contour_generator(z=[[z, z], [z, z]], name=name, line_type=LineType.SeparateCode)
    lines = cont_gen.lines(zlevel)
    assert lines == ([], [])


@pytest.mark.parametrize("name", util_test.all_names())
def test_lines_infinite_level(name: str) -> None:
    cont_gen = contour_generator(z=[[0, 0], [1, 1]], name=name, line_type=LineType.SeparateCode)
    for level in (-np.inf, np.inf):
        lines = cont_gen.lines(level)
        assert len(lines[0]) == 0  # No lines
