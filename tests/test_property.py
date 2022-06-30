import pytest

from sgflib import SGFProperty
from sgflib.exceptions import SGFPropertyValueError


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
def test_print_property(label, values, expected):
    prop = SGFProperty(label, values)
    assert str(prop) == expected
    assert repr(prop) == f"SGFProperty({expected})"


def test_property_ops():
    prop = SGFProperty("AB", ["dd"])

    with pytest.raises(SGFPropertyValueError) as err:
        prop.remove("dd")

    assert str(err.value) == "Cannot remove last element of SGFPropertyValue"

    prop.add("pp")
    with pytest.raises(SGFPropertyValueError) as err:
        prop.remove("dq")

    assert str(err.value) == "Element not found in SGFPropertyValue"
