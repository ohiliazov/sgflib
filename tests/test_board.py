import pytest
from typing import Tuple

from sgflib import SGFBoard
from sgflib.enums import Player
from sgflib.exceptions import SGFBoardError


def test_board_shape():
    board = SGFBoard((3, 3), Player.BLACK)
    assert board.data == [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]


@pytest.mark.parametrize(
    "shape",
    [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 53),
        (52, 0),
        (52, 53),
        (53, 1),
        (53, 0),
        (53, 52),
        (53, 53),
    ],
)
def test_board_wrong_shape(shape: Tuple[int, int]):

    with pytest.raises(SGFBoardError) as err:
        SGFBoard(shape, Player.BLACK)

    assert str(err.value) == "Board dimensions should be between 1 and 52."


@pytest.mark.parametrize(
    "data",
    [
        [[]],
        [
            [0, 0, 0],
            [0, 0, 0],
        ],
        [
            [0, 0],
            [0, 0],
            [0, 0],
        ],
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0],
        ],
    ],
)
def test_board_wrong_data(data):
    with pytest.raises(SGFBoardError) as err:
        SGFBoard(shape=(3, 3), player=Player.BLACK, data=data)

    assert str(err.value) == "Data should be of shape (3, 3)."


def test_board_suicide():
    board = SGFBoard((1, 1), Player.BLACK)
    with pytest.raises(SGFBoardError) as err:
        board.move((0, 0))
    assert str(err.value) == "Illegal move: Suicide."

    board = SGFBoard(
        shape=(2, 2),
        player=Player.BLACK,
        data=[
            [1, 1],
            [1, 0],
        ],
    )
    with pytest.raises(SGFBoardError) as err:
        board.move((1, 1))
    assert str(err.value) == "Illegal move: Suicide."

    board = SGFBoard(
        shape=(3, 3),
        player=Player.WHITE,
        data=[
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ],
    )
    for move in [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]:
        with pytest.raises(SGFBoardError) as err:
            board.move(move)
        assert str(err.value) == "Illegal move: Suicide."


def test_board_allow_suicide():
    board = SGFBoard((1, 1), Player.BLACK)
    with pytest.raises(SGFBoardError) as err:
        board.move((0, 0))
    assert str(err.value) == "Illegal move: Suicide."

    board = SGFBoard(
        shape=(2, 2),
        player=Player.BLACK,
        data=[
            [1, 1],
            [1, 0],
        ],
        allow_suicide=True,
    )
    board.move((1, 1))
    assert board.data == [
        [0, 0],
        [0, 0],
    ]

    board = SGFBoard(
        shape=(3, 3),
        player=Player.WHITE,
        data=[
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ],
        allow_suicide=True,
    )
    for move in [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)]:
        board.move(move)
        assert board.data == [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ]
        board.undo()


@pytest.mark.parametrize("coord", [(-1, 2), (1, 3), (-1, -3), (3, 4)])
def test_board_wrong_coordinate(coord: Tuple[int, int]):
    board = SGFBoard(
        shape=(3, 3),
        player=Player.BLACK,
        data=[
            [1, -1, 0],
            [0, 1, 0],
            [0, 0, 0],
        ],
    )

    with pytest.raises(SGFBoardError) as err:
        board.move(coord)

    assert str(err.value) == "Illegal move: Wrong coordinate."


@pytest.mark.parametrize("coord", [(0, 0), (0, 2), (2, 0), (1, 0)])
def test_board_not_empty(coord: Tuple[int, int]):
    board = SGFBoard(
        shape=(3, 3),
        player=Player.BLACK,
        data=[
            [1, 0, 1],
            [-1, 0, 0],
            [1, 0, 0],
        ],
    )
    with pytest.raises(SGFBoardError) as err:
        board.move(coord)
    assert str(err.value) == "Illegal move: Not empty."


def test_board_ko():
    board = SGFBoard(
        shape=(3, 4),
        player=Player.WHITE,
        data=[
            [0, 1, -1, 0],
            [1, 0, 1, -1],
            [0, 1, -1, 0],
        ],
    )
    board.move((1, 1))
    assert board.data == [
        [0, 1, -1, 0],
        [1, -1, 0, -1],
        [0, 1, -1, 0],
    ]
    with pytest.raises(SGFBoardError) as err:
        board.move((1, 2))

    assert str(err.value) == "Illegal move: Ko."


def test_board_super_ko():
    board = SGFBoard(
        shape=(7, 5),
        player=Player.BLACK,
        data=[
            [0, 1, -1, 0, 0],
            [1, -1, 0, -1, 0],
            [0, 1, -1, 0, 0],
            [1, 0, 1, -1, 0],
            [0, 1, -1, 0, 0],
            [1, -1, 0, -1, 0],
            [0, 1, -1, 0, 0],
        ],
        allow_super_ko=False,
    )
    for move in [(1, 2), (3, 1), (5, 2), (1, 1), (3, 2)]:
        board.move(move)

    assert board.data == [
        [0, 1, -1, 0, 0],
        [1, -1, 0, -1, 0],
        [0, 1, -1, 0, 0],
        [1, 0, 1, -1, 0],
        [0, 1, -1, 0, 0],
        [1, 0, 1, -1, 0],
        [0, 1, -1, 0, 0],
    ]
    with pytest.raises(SGFBoardError) as err:
        board.move((5, 1))

    assert str(err.value) == "Illegal move: Super-Ko."
