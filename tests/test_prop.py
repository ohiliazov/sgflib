import pytest

from sgflib import SGFProp
from sgflib.exceptions import DuplicateSGFPropValueError, EmptySGFPropValueError, SGFPropValueNotFoundError


@pytest.mark.parametrize(
    "label, values, expected",
    [
        ("B", ["dd"], "B[dd]"),
        ("B", {"dd"}, "B[dd]"),
        ("AB", ["dd", "pp"], "AB[dd][pp]"),
        ("AB", ["pp", "dd", "pp"], "AB[dd][pp]"),
        ("C", ["John Doe [3d] \\UA\\"], "C[John Doe [3d\\] \\\\UA\\\\]"),
    ]
)
def test_print_prop(label, values, expected):
    prop = SGFProp(label, values)
    assert str(prop) == expected
    assert repr(prop) == f"SGFProp({expected})"


def test_prop_add_value():
    prop = SGFProp("AB", ["dd"])
    prop.add("pp")

    assert prop.values == {"dd", "pp"}


def test_prop_remove_value():
    prop = SGFProp("AB", ["dd", "pp"])
    prop.remove("pp")

    assert prop.values == {"dd"}


def test_prop_add_duplicate_value():
    prop = SGFProp("AB", ["dd"])

    with pytest.raises(DuplicateSGFPropValueError):
        prop.add("dd")


def test_prop_remove_last_value():
    prop = SGFProp("AB", ["dd"])

    with pytest.raises(EmptySGFPropValueError):
        prop.remove("dd")


def test_prop_remove_absent_value():
    prop = SGFProp("AB", ["dd"])

    with pytest.raises(SGFPropValueNotFoundError):
        prop.remove("pp")
