import pytest

from sgflib import SGFProp, SGFNode, SGFTree, SGFParser
from sgflib.exceptions import SGFPropValueParseError, SGFPropParseError, SGFNodeParseError, SGFTreeParseError


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "dd"),
        ("[dd][", "dd"),
        ("[dd]C", "dd"),
        ("[dd];", "dd"),
        ("[dd](", "dd"),
        ("[dd])", "dd"),
        ("[John Doe [3d\\] \\\\UA\\\\]", "John Doe [3d] \\UA\\"),
        ("[Go][John Doe [3d\\] \\\\UA\\\\]", "Go"),
    ]
)
def test_parse_prop_value(data, expected):
    parser = SGFParser(data)
    prop = parser.parse_prop_value()
    assert prop == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("dd]", "Expected `[` at the start of SGFProp value."),
        (";B[dd]", "Expected `[` at the start of SGFProp value."),
        ("(;B[dd])", "Expected `[` at the start of SGFProp value."),
        ("[dd", "Expected `]` at the end of SGFProp value."),
        ("[John Doe [3d\\]", "Expected `]` at the end of SGFProp value."),
    ]
)
def test_parse_prop_value_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFPropValueParseError) as err:
        parser.parse_prop_value()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("AB[dd][pp]", SGFProp("AB", ["dd", "pp"])),
        ("AB[dd][pp]C", SGFProp("AB", ["dd", "pp"])),
        ("AB[dd][pp];", SGFProp("AB", ["dd", "pp"])),
        ("AB[dd][pp](", SGFProp("AB", ["dd", "pp"])),
        ("AB[dd][pp])", SGFProp("AB", ["dd", "pp"])),
    ]
)
def test_parse_prop(data, expected):
    parser = SGFParser(data)
    prop = parser.parse_prop()
    assert prop == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expected `[a-zA-Z]` at the start of SGFProp."),
        (";B[dd]", "Expected `[a-zA-Z]` at the start of SGFProp."),
        ("(;B[dd])", "Expected `[a-zA-Z]` at the start of SGFProp."),
        ("B[dd", "Expected at least one SGFProp value."),
    ]
)
def test_parse_prop_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFPropParseError) as err:
        parser.parse_prop()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (";", SGFNode([])),
        (";B[dd]C[Go]", SGFNode([SGFProp("B", ["dd"]), SGFProp("C", ["Go"])])),
        (";B[dd]C[Go];", SGFNode([SGFProp("B", ["dd"]), SGFProp("C", ["Go"])])),
        (";B[dd]C[Go](", SGFNode([SGFProp("B", ["dd"]), SGFProp("C", ["Go"])])),
        (";B[dd]C[Go])", SGFNode([SGFProp("B", ["dd"]), SGFProp("C", ["Go"])])),
    ]
)
def test_parse_node(data, expected):
    parser = SGFParser(data)
    prop = parser.parse_node()
    assert prop == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expected `;` at the start of SGFNode."),
        ("B[dd]", "Expected `;` at the start of SGFNode."),
        ("(;B[dd])", "Expected `;` at the start of SGFNode."),
    ]
)
def test_parse_node_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFNodeParseError) as err:
        parser.parse_node()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("(;)", SGFTree([SGFNode()])),
        ("(;B[dd])", SGFTree([SGFNode([SGFProp("B", ["dd"])])])),
        ("(;B[dd]);", SGFTree([SGFNode([SGFProp("B", ["dd"])])])),
        ("(;B[dd])(", SGFTree([SGFNode([SGFProp("B", ["dd"])])])),
        ("(;B[dd]))", SGFTree([SGFNode([SGFProp("B", ["dd"])])])),
        (
            "(;B[dd](;W[pd];B[dp])(;W[qd]))",
            SGFTree(
                nodes=[SGFNode([SGFProp("B", ["dd"])])],
                variations=[
                    SGFTree(nodes=[SGFNode([SGFProp("W", ["pd"])]), SGFNode([SGFProp("B", ["dp"])])]),
                    SGFTree(nodes=[SGFNode([SGFProp("W", ["qd"])])]),
                ]
            )
        ),
    ]
)
def test_parse_tree(data, expected):
    parser = SGFParser(data)
    prop = parser.parse_tree()
    assert prop == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expected `(` at the start of SGFTree."),
        ("B[dd]", "Expected `(` at the start of SGFTree."),
        (";B[dd]", "Expected `(` at the start of SGFTree."),
        ("(;B[dd]", "Expected `)` at the end of SGFTree."),
        ("()", "Expected at least one SGFNode."),
    ]
)
def test_parse_tree_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFTreeParseError) as err:
        parser.parse_tree()
    assert str(err.value) == expected
