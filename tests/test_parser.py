import pytest

from sgflib import SGFProperty, SGFNode, SGFGameTree, SGFParser
from sgflib.exceptions import (
    SGFPropertyValueParseError,
    SGFPropertyParseError,
    SGFNodeParseError,
    SGFGameTreeParseError,
)


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
    ],
)
def test_parse_prop_value(data, expected):
    parser = SGFParser(data)
    prop = parser.parse_prop_value()
    assert prop == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("dd]", "Expected `[` at the start of SGFProperty value."),
        (";B[dd]", "Expected `[` at the start of SGFProperty value."),
        ("(;B[dd])", "Expected `[` at the start of SGFProperty value."),
        ("[dd", "Expected `]` at the end of SGFProperty value."),
        ("[John Doe [3d\\]", "Expected `]` at the end of SGFProperty value."),
    ],
)
def test_parse_prop_value_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFPropertyValueParseError) as err:
        parser.parse_prop_value()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("AB[dd][pp]", SGFProperty("AB", ["dd", "pp"])),
        ("AB[dd][pp]C", SGFProperty("AB", ["dd", "pp"])),
        ("AB[dd][pp];", SGFProperty("AB", ["dd", "pp"])),
        ("AB[dd][pp](", SGFProperty("AB", ["dd", "pp"])),
        ("AB[dd][pp])", SGFProperty("AB", ["dd", "pp"])),
    ],
)
def test_parse_prop(data, expected):
    parser = SGFParser(data)
    prop = parser.parse_prop()
    assert prop == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expected `[a-zA-Z]` at the start of SGFProperty."),
        (";B[dd]", "Expected `[a-zA-Z]` at the start of SGFProperty."),
        ("(;B[dd])", "Expected `[a-zA-Z]` at the start of SGFProperty."),
        ("B[dd", "Expected at least one SGFProperty value."),
    ],
)
def test_parse_prop_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFPropertyParseError) as err:
        parser.parse_prop()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (";", SGFNode([])),
        (";B[dd]C[Go]", SGFNode([SGFProperty("B", ["dd"]), SGFProperty("C", ["Go"])])),
        (";B[dd]C[Go];", SGFNode([SGFProperty("B", ["dd"]), SGFProperty("C", ["Go"])])),
        (";B[dd]C[Go](", SGFNode([SGFProperty("B", ["dd"]), SGFProperty("C", ["Go"])])),
        (";B[dd]C[Go])", SGFNode([SGFProperty("B", ["dd"]), SGFProperty("C", ["Go"])])),
    ],
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
    ],
)
def test_parse_node_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFNodeParseError) as err:
        parser.parse_node()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("(;)", SGFGameTree([SGFNode()])),
        ("(;B[dd])", SGFGameTree([SGFNode([SGFProperty("B", ["dd"])])])),
        ("(;B[dd]);", SGFGameTree([SGFNode([SGFProperty("B", ["dd"])])])),
        ("(;B[dd])(", SGFGameTree([SGFNode([SGFProperty("B", ["dd"])])])),
        ("(;B[dd]))", SGFGameTree([SGFNode([SGFProperty("B", ["dd"])])])),
        (
            "(;B[dd](;W[pd];B[dp])(;W[qd]))",
            SGFGameTree(
                nodes=[SGFNode([SGFProperty("B", ["dd"])])],
                variations=[
                    SGFGameTree(
                        nodes=[
                            SGFNode([SGFProperty("W", ["pd"])]),
                            SGFNode([SGFProperty("B", ["dp"])]),
                        ]
                    ),
                    SGFGameTree(nodes=[SGFNode([SGFProperty("W", ["qd"])])]),
                ],
            ),
        ),
    ],
)
def test_parse_tree(data, expected):
    parser = SGFParser(data)
    prop = parser.parse_tree()
    assert prop == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expected `(` at the start of SGFGameTree."),
        ("B[dd]", "Expected `(` at the start of SGFGameTree."),
        (";B[dd]", "Expected `(` at the start of SGFGameTree."),
        ("(;B[dd]", "Expected `)` at the end of SGFGameTree."),
        ("()", "Expected at least one SGFNode."),
    ],
)
def test_parse_tree_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFGameTreeParseError) as err:
        parser.parse_tree()
    assert str(err.value) == expected
