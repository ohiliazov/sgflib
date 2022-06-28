import pytest

from sgflib import SGFProperty
from sgflib.exceptions import (
    DuplicateSGFPropertyValueError,
    EmptySGFPropertyValueError,
    SGFPropertyValueNotFoundError,
)


@pytest.mark.parametrize(
    "label, values, expected",
    [
        ("B", ["dd"], "B[dd]"),
        ("B", {"dd"}, "B[dd]"),
        ("AB", ["dd", "pp"], "AB[dd][pp]"),
        ("AB", ["pp", "dd", "pp"], "AB[dd][pp]"),
        ("C", ["John Doe [3d] \\UA\\"], "C[John Doe [3d\\] \\\\UA\\\\]"),
    ],
)
def test_print_prop(label, values, expected):
    prop = SGFProperty(label, values)
    assert str(prop) == expected
    assert repr(prop) == f"SGFProperty({expected})"


def test_prop_add_value():
    prop = SGFProperty("AB", ["dd"])
    prop.add("pp")

    assert prop.values == {"dd", "pp"}


def test_prop_remove_value():
    prop = SGFProperty("AB", ["dd", "pp"])
    prop.remove("pp")

    assert prop.values == {"dd"}


def test_prop_add_duplicate_value():
    prop = SGFProperty("AB", ["dd"])

    with pytest.raises(DuplicateSGFPropertyValueError):
        prop.add("dd")


def test_prop_remove_last_value():
    prop = SGFProperty("AB", ["dd"])

    with pytest.raises(EmptySGFPropertyValueError):
        prop.remove("dd")


def test_prop_remove_absent_value():
    prop = SGFProperty("AB", ["dd"])

    with pytest.raises(SGFPropertyValueNotFoundError):
        prop.remove("pp")
