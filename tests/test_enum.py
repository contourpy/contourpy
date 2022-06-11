import pytest

from contourpy import FillType, LineType, ZInterp
from contourpy.enum_util import as_fill_type, as_line_type, as_z_interp

from . import util_test


@pytest.mark.parametrize("name, value", util_test.all_fill_types_str_value())
def test_fill_type(name, value):
    t = FillType.__members__[name]
    assert t.name == name
    assert t.value == value


@pytest.mark.parametrize("name, value", util_test.all_line_types_str_value())
def test_line_type(name, value):
    t = LineType.__members__[name]
    assert t.name == name
    assert t.value == value


def test_all_fill_types():
    # Check that all_fill_types() matches FillType.__members__
    fill_types = dict(util_test.all_fill_types_str_value())
    for name, enum in dict(FillType.__members__).items():
        assert name in fill_types
        assert fill_types[name] == enum.value


def test_all_line_types():
    # Check that all_line_types() matches LineType.__members__
    line_types = dict(util_test.all_line_types_str_value())
    for name, enum in dict(LineType.__members__).items():
        assert name in line_types
        assert line_types[name] == enum.value


def test_all_z_interps():
    # Check that all_z_interps() matches ZInterp.__members__
    z_interps = dict(util_test.all_z_interps_str_value())
    for name, enum in dict(ZInterp.__members__).items():
        assert name in z_interps
        assert z_interps[name] == enum.value


@pytest.mark.parametrize(
    ["enum_type", "from_string_function"],
    [(FillType, as_fill_type), (LineType, as_line_type), (ZInterp, as_z_interp)])
def test_string_to_enum(enum_type, from_string_function):
    for name, enum in enum_type.__members__.items():
        line_type = from_string_function(name)
        assert line_type == enum

    msg = "'unknown'"
    with pytest.raises(KeyError, match=msg):
        _ = from_string_function("unknown")
