from contourpy import (
    FillType, LineType, Mpl2005ContourGenerator, Mpl2014ContourGenerator, SerialContourGenerator,
    ThreadedContourGenerator,
)
import pytest
import util_test


def get_class_from_name(name):
    return globals()[name]


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_default_fill_type(class_name):
    cls = get_class_from_name(class_name)
    default = cls.default_fill_type
    assert isinstance(default, FillType)
    if class_name in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator"):
        expect = FillType.OuterCodes
    else:
        expect = FillType.OuterOffsets
    assert default == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_default_line_type(class_name):
    cls = get_class_from_name(class_name)
    default = cls.default_line_type
    assert isinstance(default, LineType)
    if class_name in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator"):
        expect = LineType.SeparateCodes
    else:
        expect = LineType.Separate
    assert default == expect


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
    supports = cls.supports_fill_type(FillType.OuterCodes)
    assert isinstance(supports, bool)
    expect = True
    assert supports == expect
    supports = cls.supports_fill_type(FillType.ChunkCombinedOffsets2)
    assert isinstance(supports, bool)
    expect = class_name not in ("Mpl2005ContourGenerator", "Mpl2014ContourGenerator")
    assert supports == expect


@pytest.mark.parametrize("class_name", util_test.all_class_names())
def test_supports_line_type(class_name):
    cls = get_class_from_name(class_name)
    supports = cls.supports_line_type(LineType.SeparateCodes)
    assert isinstance(supports, bool)
    expect = True
    assert supports == expect
    supports = cls.supports_line_type(LineType.ChunkCombinedOffsets)
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
