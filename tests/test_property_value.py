import pytest

from sgflib import SGFPropertyValue
from sgflib.exceptions import SGFPropertyValueError


@pytest.mark.parametrize(
    "values, expected",
    [
        (["dd"], "[dd]"),
        (["dd"], "[dd]"),
        (["dd", "pp"], "[dd][pp]"),
        (["pp", "dd", "pp"], "[dd][pp]"),
        (["John Doe [3d] \\UA\\"], "[John Doe [3d\\] \\\\UA\\\\]"),
    ],
)
def test_print_property_value(values, expected):
    prop_value = SGFPropertyValue(values)
    assert prop_value.sgf == expected
    assert repr(prop_value) == f"SGFPropertyValue({expected})"


def test_copy_property_value():
    prop_value = SGFPropertyValue({"aa", "bb"})
    copy_prop_value = prop_value.copy()

    assert copy_prop_value == prop_value

    copy_prop_value.add("cc")
    assert prop_value == {"aa", "bb"}
    assert copy_prop_value == {"aa", "bb", "cc"}


def test_property_value_ops():
    with pytest.raises(SGFPropertyValueError) as err:
        _ = SGFPropertyValue([])
    assert str(err.value) == "Cannot be empty"

    prop_value = SGFPropertyValue(["dd"])

    with pytest.raises(SGFPropertyValueError) as err:
        prop_value.clear()
    assert str(err.value) == "Cannot clear"

    with pytest.raises(SGFPropertyValueError) as err:
        prop_value.pop()
    assert str(err.value) == "Cannot pop last element"

    with pytest.raises(SGFPropertyValueError) as err:
        prop_value.remove("dd")
    assert str(err.value) == "Cannot remove last element"

    prop_value.add("pp")
    assert prop_value == {"dd", "pp"}

    with pytest.raises(KeyError) as err:
        prop_value.remove("dq")

    prop_value.remove("pp")
    assert prop_value == {"dd"}

    prop_value.add("pp")
    assert prop_value == {"dd", "pp"}

    value = prop_value.pop()
    assert value not in prop_value

    prop_value = SGFPropertyValue({"dd", "pp"})

    prop_value.discard("dd")
    assert prop_value == {"pp"}

    with pytest.raises(SGFPropertyValueError) as err:
        prop_value.discard("pp")
    assert str(err.value) == "Cannot discard last element"
