import pytest

from sgflib import SGFNode, SGFProp
from sgflib.exceptions import DuplicateSGFPropError, SGFPropNotFoundError


@pytest.mark.parametrize(
    "props, expected",
    [
        ([], ";"),
        ([SGFProp("B", ["dd"])], ";B[dd]"),
        (
            [
                SGFProp("AB", ["dd", "pp"]),
                SGFProp("C", ["John Doe [3d] \\UA\\"]),
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
    node = SGFNode([SGFProp("AB", {"dd"})])

    node.add(SGFProp("AW", {"pp"}))
    assert len(node) == 2
    assert node.props == {SGFProp("AB", {"dd"}), SGFProp("AW", {"pp"})}

    with pytest.raises(DuplicateSGFPropError):
        node.add(SGFProp("AW", {"pp"}))

    node.remove("AW")
    assert node.props == {SGFProp("AB", {"dd"})}

    with pytest.raises(SGFPropNotFoundError):
        node.remove("AW")


def test_node_as_dict():
    node = SGFNode()
    node["AB"] = {"dd"}
    assert node.props == {SGFProp("AB", {"dd"})}

    assert node["AB"] == SGFProp("AB", {"dd"})

    with pytest.raises(SGFPropNotFoundError):
        _ = node["C"]

    node["AW"] = {"pp"}
    assert node.props == {SGFProp("AB", {"dd"}), SGFProp("AW", {"pp"})}

    with pytest.raises(DuplicateSGFPropError):
        node["AW"] = {"pp"}

    del node["AW"]
    assert node.props == {SGFProp("AB", {"dd"})}
    with pytest.raises(SGFPropNotFoundError):
        del node["AW"]
