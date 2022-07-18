import pytest

from sgflib import SGFGameTree
from sgflib.exceptions import SGFGameTreeError, SGFSequenceError


@pytest.mark.parametrize(
    "nodes, variations, expected, expected_pretty",
    [
        ([{}], [], "(;)", "(\n  ;\n)"),
        (
            [
                {"AB": ["dd", "pp"]},
                {"W": ["pd"]},
            ],
            [],
            "(;AB[dd][pp];W[pd])",
            "(\n  ;AB[dd][pp];W[pd]\n)",
        ),
        (
            [{"B": ["dd"]}],
            [
                ([{"W": ["pd"]}],),
                ([{"W": ["dp"]}],),
            ],
            "(;B[dd](;W[pd])(;W[dp]))",
            "(\n  ;B[dd]\n  (\n    ;W[pd]\n  )\n  (\n    ;W[dp]\n  )\n)",
        ),
    ],
)
def test_print_tree(nodes, variations, expected, expected_pretty):
    tree = SGFGameTree(nodes, variations)
    assert tree.sgf == expected
    assert repr(tree) == f"SGFGameTree({expected})"
    assert tree.pretty() == expected_pretty


def test_tree_ops():
    with pytest.raises(SGFSequenceError):
        _ = SGFGameTree([], [])

    tree = SGFGameTree(
        [{"C": ["Root tree."]}],
    )

    moves = SGFGameTree(
        [{"B": ["dd"]}, {"W": ["pp"]}],
    )

    with pytest.raises(SGFGameTreeError):
        tree.insert(moves, 0)

    with pytest.raises(SGFGameTreeError):
        tree.insert(moves, 2)

    tree.insert(moves, 1)

    assert tree == (
        [
            {"C": ["Root tree."]},
            {"B": ["dd"]},
            {"W": ["pp"]},
        ],
    )

    white_move_2 = ([{"W": ["pq"]}], [])

    tree.insert(white_move_2, 2)

    assert tree == (
        [
            {"C": ["Root tree."]},
            {"B": ["dd"]},
        ],
        [
            ([{"W": ["pp"]}],),
            ([{"W": ["pq"]}],),
        ],
    )

    white_move_3 = ([{"W": ["qq"]}], [])

    tree.insert(white_move_3, 2)

    assert tree == (
        [
            {"C": ["Root tree."]},
            {"B": ["dd"]},
        ],
        [
            ([{"W": ["pp"]}],),
            ([{"W": ["pq"]}],),
            ([{"W": ["qq"]}],),
        ],
    )

    with pytest.raises(SGFGameTreeError) as err:
        tree.cut_variation(-1)

    assert str(err.value) == "Cannot cut variation SGFGameTree at index=-1."

    with pytest.raises(SGFGameTreeError) as err:
        tree.cut_variation(3)

    assert str(err.value) == "Cannot cut variation SGFGameTree at index=3."

    tree.cut_variation(2)

    assert tree.variations == [
        ([{"W": ["pp"]}],),
        ([{"W": ["pq"]}],),
    ]

    with pytest.raises(SGFGameTreeError) as err:
        tree.cut_tree(0)

    assert str(err.value) == "Cannot cut SGFSequence at index=0."

    with pytest.raises(SGFGameTreeError) as err:
        tree.cut_tree(2)

    assert str(err.value) == "Cannot cut SGFSequence at index=2."

    tree.cut_tree(1)

    assert tree == ([{"C": ["Root tree."]}],)
