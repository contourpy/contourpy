import pytest

from contourpy import (
    FillType, LineType, Mpl2005ContourGenerator, Mpl2014ContourGenerator, SerialContourGenerator,
    ThreadedContourGenerator,
)

from . import util_test

_lookup = {
    "Mpl2005ContourGenerator": Mpl2005ContourGenerator,
    "Mpl2014ContourGenerator": Mpl2014ContourGenerator,
    "SerialContourGenerator": SerialContourGenerator,
    "ThreadedContourGenerator": ThreadedContourGenerator,
}


def get_class_from_name(class_name):
    return _lookup[class_name]


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_default_fill_type(class_name):
    cls = get_class_from_name(class_name)
    default = cls.default_fill_type
    assert isinstance(default, FillType)
    if class_name in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator"):
        expect = FillType.OuterCode
    else:
        expect = FillType.OuterOffset
    assert default == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_default_line_type(class_name):
    cls = get_class_from_name(class_name)
    default = cls.default_line_type
    assert isinstance(default, LineType)
    if class_name in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator"):
        expect = LineType.SeparateCode
    else:
        expect = LineType.Separate
    assert default == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_has_lines_and_filled(class_name):
    cls = get_class_from_name(class_name)
    for func_name in ["create_contour", "create_filled_contour", "filled", "lines"]:
        assert hasattr(cls, func_name)
        assert callable(getattr(cls, func_name))


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_supports_corner_mask(class_name):
    cls = get_class_from_name(class_name)
    supports = cls.supports_corner_mask()
    assert isinstance(supports, bool)
    expect = class_name != "Mpl2005ContourGenerator"
    assert supports == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_supports_fill_type(class_name):
    cls = get_class_from_name(class_name)
    supports = cls.supports_fill_type(FillType.OuterCode)
    assert isinstance(supports, bool)
    expect = True
    assert supports == expect
    supports = cls.supports_fill_type(FillType.ChunkCombinedOffsetOffset)
    assert isinstance(supports, bool)
    expect = class_name not in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator")
    assert supports == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_supports_line_type(class_name):
    cls = get_class_from_name(class_name)
    supports = cls.supports_line_type(LineType.SeparateCode)
    assert isinstance(supports, bool)
    expect = True
    assert supports == expect
    supports = cls.supports_line_type(LineType.ChunkCombinedOffset)
    assert isinstance(supports, bool)
    expect = class_name not in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator")
    assert supports == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_supports_quad_as_tri(class_name):
    cls = get_class_from_name(class_name)
    supports = cls.supports_quad_as_tri()
    assert isinstance(supports, bool)
    expect = class_name not in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator")
    assert supports == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_supports_threads(class_name):
    cls = get_class_from_name(class_name)
    supports = cls.supports_threads()
    assert isinstance(supports, bool)
    expect = class_name == "ThreadedContourGenerator"
    assert supports == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_supports_z_interp(class_name):
    cls = get_class_from_name(class_name)
    supports = cls.supports_z_interp()
    assert isinstance(supports, bool)
    expect = class_name not in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator")
    assert supports == expect
