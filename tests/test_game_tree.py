import pytest

from sgflib import SGFGameTree, SGFNode
from sgflib.exceptions import SGFGameTreeError, SGFSequenceError


@pytest.mark.parametrize(
    "nodes, variations, expected, expected_pretty",
    [
        ([SGFNode()], [], "(;)", "(\n  ;\n)"),
        (
            [
                SGFNode({"AB": ["dd", "pp"]}),
                SGFNode({"W": ["pd"]}),
            ],
            [],
            "(;AB[dd][pp];W[pd])",
            "(\n  ;AB[dd][pp];W[pd]\n)",
        ),
        (
            [
                SGFNode({"B": ["dd"]}),
            ],
            [
                SGFGameTree(
                    [
                        SGFNode({"W": ["pd"]}),
                    ]
                ),
                SGFGameTree(
                    [
                        SGFNode({"W": ["dp"]}),
                    ]
                ),
            ],
            "(;B[dd](;W[pd])(;W[dp]))",
            "(\n  ;B[dd]\n  (\n    ;W[pd]\n  )\n  (\n    ;W[dp]\n  )\n)",
        ),
    ],
)
def test_print_tree(nodes, variations, expected, expected_pretty):
    tree = SGFGameTree(nodes, variations)
    assert str(tree) == expected
    assert repr(tree) == f"SGFGameTree({expected})"
    assert tree.pretty() == expected_pretty


def test_tree_ops():
    with pytest.raises(SGFSequenceError):
        _ = SGFGameTree([])

    tree = SGFGameTree([{"C": ["Root tree."]}])

    moves = SGFGameTree(sequence=[SGFNode({"B": ["dd"]}), SGFNode({"W": ["pp"]})])

    with pytest.raises(SGFGameTreeError):
        tree.insert(moves, 0)

    with pytest.raises(SGFGameTreeError):
        tree.insert(moves, 2)

    tree.insert(moves, 1)

    assert tree == SGFGameTree(
        sequence=[
            SGFNode({"C": ["Root tree."]}),
            SGFNode({"B": ["dd"]}),
            SGFNode({"W": ["pp"]}),
        ]
    )

    white_move_2 = SGFGameTree(sequence=[SGFNode({"W": ["pq"]})])

    tree.insert(white_move_2, 2)

    assert tree == SGFGameTree(
        sequence=[
            SGFNode({"C": ["Root tree."]}),
            SGFNode({"B": ["dd"]}),
        ],
        variations=[
            SGFGameTree(sequence=[SGFNode({"W": ["pp"]})]),
            SGFGameTree(sequence=[SGFNode({"W": ["pq"]})]),
        ],
    )

    white_move_3 = SGFGameTree(sequence=[SGFNode({"W": ["qq"]})])

    tree.insert(white_move_3, 2)

    assert tree == SGFGameTree(
        sequence=[
            SGFNode({"C": ["Root tree."]}),
            SGFNode({"B": ["dd"]}),
        ],
        variations=[
            SGFGameTree(sequence=[SGFNode({"W": ["pp"]})]),
            SGFGameTree(sequence=[SGFNode({"W": ["pq"]})]),
            SGFGameTree(sequence=[SGFNode({"W": ["qq"]})]),
        ],
    )
