import pytest

from sgflib import SGFNode


@pytest.mark.parametrize(
    "props, expected",
    [
        ({}, ";"),
        ({"B": ["dd"]}, ";B[dd]"),
        (
            {
                "AB": ["dd", "pp"],
                "C": ["John Doe [3d] \\UA\\"],
            },
            ";AB[dd][pp]C[John Doe [3d\\] \\\\UA\\\\]",
        ),
    ],
)
def test_print_node(props, expected):
    node = SGFNode(props)
    assert str(node) == expected
    assert repr(node) == f"SGFNode({expected})"


def test_node_ops():
    node = SGFNode()
    node["AB"] = {"dd"}
    assert node == {"AB": {"dd"}}

    assert node["AB"] == {"dd"}

    with pytest.raises(KeyError):
        _ = node["C"]

    # insert new property
    node["AW"] = {"pp"}
    assert node == {"AB": {"dd"}, "AW": {"pp"}}

    # update existing property
    node["AW"] = {"pq"}
    assert node == {"AB": {"dd"}, "AW": {"pq"}}

    del node["AW"]
    assert node == {"AB": {"dd"}}
    with pytest.raises(KeyError):
        del node["AW"]
