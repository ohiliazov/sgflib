import pytest

from sgflib import SGFGameTree, SGFNode, SGFProperty
from sgflib.exceptions import EmptySGFGameTreeError, SGFGameTreeInsertionError


@pytest.mark.parametrize(
    "nodes, variations, expected",
    [
        ([SGFNode()], [], "(;)"),
        (
            [
                SGFNode([SGFProperty("AB", {"dd", "pp"})]),
                SGFNode([SGFProperty("W", {"pd"})]),
            ],
            [],
            "(;AB[dd][pp];W[pd])"
        ),
        (
            [
                SGFNode([SGFProperty("B", {"dd"})]),
            ],
            [
                SGFGameTree(
                    [
                        SGFNode([SGFProperty("W", {"pd"})]),
                    ]
                ),
                SGFGameTree(
                    [
                        SGFNode([SGFProperty("W", {"dp"})]),
                    ]
                ),
            ],
            "(;B[dd](;W[pd])(;W[dp]))"
        )
    ]
)
def test_print_tree(nodes, variations, expected):
    tree = SGFGameTree(nodes, variations)
    assert str(tree) == expected
    assert repr(tree) == f"SGFGameTree({expected})"


def test_tree_ops():
    with pytest.raises(EmptySGFGameTreeError):
        _ = SGFGameTree([])

    tree = SGFGameTree(nodes=[SGFNode([SGFProperty("C", {"Root tree."})])])

    moves = SGFGameTree(nodes=[SGFNode([SGFProperty("B", {"dd"})]), SGFNode([SGFProperty("W", {"pp"})])])

    with pytest.raises(SGFGameTreeInsertionError):
        tree.insert(moves, 0)

    with pytest.raises(SGFGameTreeInsertionError):
        tree.insert(moves, 2)

    tree.insert(moves, 1)

    assert tree == SGFGameTree(
        nodes=[
            SGFNode([SGFProperty("C", {"Root tree."})]),
            SGFNode([SGFProperty("B", {"dd"})]),
            SGFNode([SGFProperty("W", {"pp"})]),
        ]
    )

    white_move_2 = SGFGameTree(nodes=[SGFNode([SGFProperty("W", {"pq"})])])

    tree.insert(white_move_2, 2)

    assert tree == SGFGameTree(
        nodes=[
            SGFNode([SGFProperty("C", {"Root tree."})]),
            SGFNode([SGFProperty("B", {"dd"})]),
        ],
        variations=[
            SGFGameTree(nodes=[SGFNode([SGFProperty("W", {"pp"})])]),
            SGFGameTree(nodes=[SGFNode([SGFProperty("W", {"pq"})])]),
        ]
    )

    white_move_3 = SGFGameTree(nodes=[SGFNode([SGFProperty("W", {"qq"})])])

    tree.insert(white_move_3, 2)

    assert tree == SGFGameTree(
        nodes=[
            SGFNode([SGFProperty("C", {"Root tree."})]),
            SGFNode([SGFProperty("B", {"dd"})]),
        ],
        variations=[
            SGFGameTree(nodes=[SGFNode([SGFProperty("W", {"pp"})])]),
            SGFGameTree(nodes=[SGFNode([SGFProperty("W", {"pq"})])]),
            SGFGameTree(nodes=[SGFNode([SGFProperty("W", {"qq"})])]),
        ]
    )
