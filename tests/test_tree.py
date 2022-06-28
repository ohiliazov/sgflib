import pytest

from sgflib import SGFTree, SGFNode, SGFProp
from sgflib.exceptions import EmptySGFTreeError, SGFTreeInsertionError


@pytest.mark.parametrize(
    "nodes, variations, expected",
    [
        ([SGFNode()], [], "(;)"),
        (
            [
                SGFNode([SGFProp("AB", {"dd", "pp"})]),
                SGFNode([SGFProp("W", {"pd"})]),
            ],
            [],
            "(;AB[dd][pp];W[pd])"
        ),
        (
            [
                SGFNode([SGFProp("B", {"dd"})]),
            ],
            [
                SGFTree(
                    [
                        SGFNode([SGFProp("W", {"pd"})]),
                    ]
                ),
                SGFTree(
                    [
                        SGFNode([SGFProp("W", {"dp"})]),
                    ]
                ),
            ],
            "(;B[dd](;W[pd])(;W[dp]))"
        )
    ]
)
def test_print_tree(nodes, variations, expected):
    tree = SGFTree(nodes, variations)
    assert str(tree) == expected
    assert repr(tree) == f"SGFTree({expected})"


def test_tree_ops():
    with pytest.raises(EmptySGFTreeError):
        _ = SGFTree([])

    tree = SGFTree(nodes=[SGFNode([SGFProp("C", {"Root tree."})])])

    moves = SGFTree(nodes=[SGFNode([SGFProp("B", {"dd"})]), SGFNode([SGFProp("W", {"pp"})])])

    with pytest.raises(SGFTreeInsertionError):
        tree.insert(moves, 0)

    with pytest.raises(SGFTreeInsertionError):
        tree.insert(moves, 2)

    tree.insert(moves, 1)

    assert tree == SGFTree(
        nodes=[
            SGFNode([SGFProp("C", {"Root tree."})]),
            SGFNode([SGFProp("B", {"dd"})]),
            SGFNode([SGFProp("W", {"pp"})]),
        ]
    )

    white_move_2 = SGFTree(nodes=[SGFNode([SGFProp("W", {"pq"})])])

    tree.insert(white_move_2, 2)

    assert tree == SGFTree(
        nodes=[
            SGFNode([SGFProp("C", {"Root tree."})]),
            SGFNode([SGFProp("B", {"dd"})]),
        ],
        variations=[
            SGFTree(nodes=[SGFNode([SGFProp("W", {"pp"})])]),
            SGFTree(nodes=[SGFNode([SGFProp("W", {"pq"})])]),
        ]
    )

    white_move_3 = SGFTree(nodes=[SGFNode([SGFProp("W", {"qq"})])])

    tree.insert(white_move_3, 2)

    assert tree == SGFTree(
        nodes=[
            SGFNode([SGFProp("C", {"Root tree."})]),
            SGFNode([SGFProp("B", {"dd"})]),
        ],
        variations=[
            SGFTree(nodes=[SGFNode([SGFProp("W", {"pp"})])]),
            SGFTree(nodes=[SGFNode([SGFProp("W", {"pq"})])]),
            SGFTree(nodes=[SGFNode([SGFProp("W", {"qq"})])]),
        ]
    )
