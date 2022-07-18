import pytest

from sgflib import (
    SGFNode,
    SGFSequence,
    SGFGameTree,
    SGFCollection,
    SGFParser,
)
from sgflib.exceptions import SGFParserError


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
        ("dd]", "Expecting SGFProperty value: line 1 column 1 (char 0)"),
        (";B[dd]", "Expecting SGFProperty value: line 1 column 1 (char 0)"),
        ("(;B[dd])", "Expecting SGFProperty value: line 1 column 1 (char 0)"),
        ("[dd", "Unterminated SGFProperty value: line 1 column 2 (char 1)"),
        (
            "[John Doe [3d\\]",
            "Unterminated SGFProperty value: line 1 column 16 (char 15)",
        ),
    ],
)
def test_parse_prop_value_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFParserError) as err:
        parser.parse_prop_value()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, label, values",
    [
        ("AB[dd][pp]", "AB", {"dd", "pp"}),
        ("AB[dd][pp]C", "AB", {"dd", "pp"}),
        ("AB[dd][pp];", "AB", {"dd", "pp"}),
        ("AB[dd][pp](", "AB", {"dd", "pp"}),
        ("AB[dd][pp])", "AB", {"dd", "pp"}),
    ],
)
def test_parse_property(data, label, values):
    parser = SGFParser(data)
    prop_label, prop_value = parser.parse_property()
    assert prop_label == label
    assert prop_value == values


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expecting SGFProperty: line 1 column 1 (char 0)"),
        (";B[dd]", "Expecting SGFProperty: line 1 column 1 (char 0)"),
        ("(;B[dd])", "Expecting SGFProperty: line 1 column 1 (char 0)"),
        ("B;", "Expecting SGFProperty value: line 1 column 2 (char 1)"),
        ("B[dd", "Unterminated SGFProperty value: line 1 column 3 (char 2)"),
    ],
)
def test_parse_prop_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFParserError) as err:
        parser.parse_property()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (";", SGFNode({})),
        (";B[dd]C[Go]", SGFNode({"B": ["dd"], "C": ["Go"]})),
        (";B[dd]C[Go];", SGFNode({"B": ["dd"], "C": ["Go"]})),
        (";B[dd]C[Go](", SGFNode({"B": ["dd"], "C": ["Go"]})),
        (";B[dd]C[Go])", SGFNode({"B": ["dd"], "C": ["Go"]})),
    ],
)
def test_parse_node(data, expected):
    parser = SGFParser(data)
    node = parser.parse_node()
    assert node == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expecting SGFNode: line 1 column 1 (char 0)"),
        ("B[dd]", "Expecting SGFNode: line 1 column 1 (char 0)"),
        ("(;B[dd])", "Expecting SGFNode: line 1 column 1 (char 0)"),
    ],
)
def test_parse_node_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFParserError) as err:
        parser.parse_node()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (";", SGFSequence([SGFNode([])])),
        (";B[dd]", SGFSequence([SGFNode({"B": ["dd"]})])),
        (
            ";B[dd];W[pp]",
            SGFSequence(
                [
                    SGFNode({"B": ["dd"]}),
                    SGFNode({"W": ["pp"]}),
                ]
            ),
        ),
        (
            ";B[dd];W[pp](",
            SGFSequence(
                [
                    SGFNode({"B": ["dd"]}),
                    SGFNode({"W": ["pp"]}),
                ]
            ),
        ),
        (
            ";B[dd];W[pp])",
            SGFSequence(
                [
                    SGFNode({"B": ["dd"]}),
                    SGFNode({"W": ["pp"]}),
                ]
            ),
        ),
    ],
)
def test_parse_sequence(data, expected):
    parser = SGFParser(data)
    sequence = parser.parse_sequence()
    assert sequence == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expecting SGFSequence: line 1 column 1 (char 0)"),
        ("B[dd]", "Expecting SGFSequence: line 1 column 1 (char 0)"),
        ("(;B[dd])", "Expecting SGFSequence: line 1 column 1 (char 0)"),
    ],
)
def test_parse_sequence_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFParserError) as err:
        parser.parse_sequence()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("(;)", SGFGameTree([{}], [])),
        ("(;B[dd])", SGFGameTree([SGFNode({"B": ["dd"]})], [])),
        ("(;B[dd]);", SGFGameTree([SGFNode({"B": ["dd"]})], [])),
        ("(;B[dd])(", SGFGameTree([SGFNode({"B": ["dd"]})], [])),
        ("(;B[dd]))", SGFGameTree([SGFNode({"B": ["dd"]})], [])),
        (
            "(;B[dd](;W[pd];B[dp])(;W[qd]))",
            SGFGameTree(
                sequence=[SGFNode({"B": ["dd"]})],
                variations=[
                    SGFGameTree(
                        sequence=[
                            SGFNode({"W": ["pd"]}),
                            SGFNode({"B": ["dp"]}),
                        ],
                        variations=[],
                    ),
                    SGFGameTree(sequence=[SGFNode({"W": ["qd"]})], variations=[]),
                ],
            ),
        ),
    ],
)
def test_parse_game_tree(data, expected):
    parser = SGFParser(data)
    assert parser.parse_game_tree() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expecting SGFGameTree: line 1 column 1 (char 0)"),
        ("B[dd]", "Expecting SGFGameTree: line 1 column 1 (char 0)"),
        (";B[dd]", "Expecting SGFGameTree: line 1 column 1 (char 0)"),
        ("()", "Expecting SGFSequence: line 1 column 2 (char 1)"),
        ("(;B[dd]", "Unterminated SGFGameTree: line 1 column 8 (char 7)"),
    ],
)
def test_parse_game_tree_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFParserError) as err:
        parser.parse_game_tree()
    assert str(err.value) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("(;)", [SGFGameTree([SGFNode()], [])]),
        (
            "(;B[dd])(;B[dc])",
            [
                SGFGameTree([SGFNode({"B": ["dd"]})], []),
                SGFGameTree([SGFNode({"B": ["dc"]})], []),
            ],
        ),
        (
            "(;B[dd])(;B[dc]))",
            [
                SGFGameTree([SGFNode({"B": ["dd"]})], []),
                SGFGameTree([SGFNode({"B": ["dc"]})], []),
            ],
        ),
    ],
)
def test_parse_game_trees(data, expected):
    parser = SGFParser(data)
    assert parser.parse_game_trees() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("(;) ", SGFCollection([SGFGameTree([SGFNode()], [])])),
        (
            "(;B[dd])(;B[dc])",
            SGFCollection(
                [
                    SGFGameTree([SGFNode({"B": ["dd"]})], []),
                    SGFGameTree([SGFNode({"B": ["dc"]})], []),
                ]
            ),
        ),
        (
            "(;B[dd](;W[pp])(;W[pq]))(;B[dc])",
            SGFCollection(
                [
                    SGFGameTree(
                        sequence=[SGFNode({"B": ["dd"]})],
                        variations=[
                            SGFGameTree([SGFNode({"W": ["pp"]})], []),
                            SGFGameTree([SGFNode({"W": ["pq"]})], []),
                        ],
                    ),
                    SGFGameTree([SGFNode({"B": ["dc"]})], []),
                ]
            ),
        ),
    ],
)
def test_parse_collection(data, expected):
    parser = SGFParser(data)
    assert parser.parse_collection() == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[dd]", "Expecting SGFCollection: line 1 column 1 (char 0)"),
        ("B[dd]", "Expecting SGFCollection: line 1 column 1 (char 0)"),
        (";B[dd]", "Expecting SGFCollection: line 1 column 1 (char 0)"),
        ("(;B[dd]))", "Extra data: line 1 column 9 (char 8)"),
    ],
)
def test_parse_collection_error(data, expected):
    parser = SGFParser(data)
    with pytest.raises(SGFParserError) as err:
        parser.parse_collection()
    assert str(err.value) == expected
