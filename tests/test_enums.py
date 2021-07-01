from contourpy import FillType, Interp, LineType
import pytest
import util_test


@pytest.mark.parametrize('name, value', util_test.all_fill_types_str_value())
def test_fill_type(name, value):
    t = FillType.__members__[name]
    assert t.name == name
    assert t.value == value


@pytest.mark.parametrize('name, value', util_test.all_line_types_str_value())
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


def test_all_interps():
    # Check that all_interps() matches Interp.__members__
    interps = dict(util_test.all_interps_str_value())
    for name, enum in dict(Interp.__members__).items():
        assert name in interps
        assert interps[name] == enum.value
