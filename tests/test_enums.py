from contourpy import FillType
import pytest
import util_test


@pytest.mark.parametrize('name, value', util_test.all_fill_types_str_value())
def test_fill_type(name, value):
    t = FillType.__members__[name]
    assert t.name == name
    assert t.value == value


def test_all_fill_types():
    # Check that all_fill_types() matches FillType.__members__
    fill_types = dict(util_test.all_fill_types_str_value())
    for name, enum in dict(FillType.__members__).items():
        assert(name in fill_types)
        assert(fill_types[name] == enum.value)
