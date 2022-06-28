import pytest

from sgflib import SGFNode, SGFProperty
from sgflib.exceptions import DuplicateSGFPropertyError, SGFPropertyNotFoundError


@pytest.mark.parametrize(
    "props, expected",
    [
        ([], ";"),
        ([SGFProperty("B", ["dd"])], ";B[dd]"),
        (
            [
                SGFProperty("AB", ["dd", "pp"]),
                SGFProperty("C", ["John Doe [3d] \\UA\\"]),
            ],
            ";AB[dd][pp]C[John Doe [3d\\] \\\\UA\\\\]"
        ),
    ]
)
def test_print_node(props, expected):
    node = SGFNode(props)
    assert str(node) == expected
    assert repr(node) == f"SGFNode({expected})"


def test_node_ops():
    node = SGFNode([SGFProperty("AB", {"dd"})])

    node.add(SGFProperty("AW", {"pp"}))
    assert len(node) == 2
    assert node.props == {SGFProperty("AB", {"dd"}), SGFProperty("AW", {"pp"})}

    with pytest.raises(DuplicateSGFPropertyError):
        node.add(SGFProperty("AW", {"pp"}))

    node.remove("AW")
    assert node.props == {SGFProperty("AB", {"dd"})}

    with pytest.raises(SGFPropertyNotFoundError):
        node.remove("AW")


def test_node_as_dict():
    node = SGFNode()
    node["AB"] = {"dd"}
    assert node.props == {SGFProperty("AB", {"dd"})}

    assert node["AB"] == SGFProperty("AB", {"dd"})

    with pytest.raises(SGFPropertyNotFoundError):
        _ = node["C"]

    node["AW"] = {"pp"}
    assert node.props == {SGFProperty("AB", {"dd"}), SGFProperty("AW", {"pp"})}

    with pytest.raises(DuplicateSGFPropertyError):
        node["AW"] = {"pp"}

    del node["AW"]
    assert node.props == {SGFProperty("AB", {"dd"})}
    with pytest.raises(SGFPropertyNotFoundError):
        del node["AW"]
