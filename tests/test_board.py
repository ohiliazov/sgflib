import pytest
from typing import Tuple

from sgflib import SGFBoard
from sgflib.board import Location
from sgflib.exceptions import SGFBoardError


def test_board_shape():
    board = SGFBoard((3, 3), Location.BLACK)
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
        SGFBoard(shape, Location.BLACK)

    assert str(err.value) == "Board dimensions should be between 1 and 52."


@pytest.mark.parametrize("turn", [Location.EMPTY, 0])
def test_board_wrong_turn(turn):
    with pytest.raises(SGFBoardError) as err:
        SGFBoard((19, 19), turn)

    assert str(err.value) == "Turn should not be Location.EMPTY."


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
        SGFBoard(shape=(3, 3), turn=Location.BLACK, data=data)

    assert str(err.value) == "Data should be of shape (3, 3)"


def test_board_suicide():
    board = SGFBoard((1, 1), Location.BLACK)
    with pytest.raises(SGFBoardError) as err:
        board.move((0, 0))
    assert str(err.value) == "Illegal move: Suicide."

    board = SGFBoard(
        shape=(2, 2),
        turn=Location.BLACK,
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
        turn=Location.WHITE,
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


@pytest.mark.parametrize("coord", [(-1, 2), (1, 3), (-1, -3), (3, 4)])
def test_board_wrong_coordinate(coord: Tuple[int, int]):
    board = SGFBoard(
        shape=(3, 3),
        turn=Location.BLACK,
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
        turn=Location.BLACK,
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
        turn=Location.WHITE,
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
        turn=Location.BLACK,
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


#
#
# def test_board():
#     board = SGFBoard(
#         shape=(3,3),
#         turn=Location.BLACK,
#         data=[
#             [1, -1, 0],
#             [0, 1, 0],
#             [0, 0, 0],
#         ],
#     )
#     with pytest.raises(SGFBoardError) as err:
#         board.move((-1, 2))
#     assert str(err.value) == "Illegal move: Wrong coordinate."
#
#     board.move((0, 2))
#     assert board.data == [
#         [1, 0, 1],
#         [0, 1, 0],
#         [0, 0, 0],
#     ]
#
#     board = SGFBoard(
#         shape=(3, 3),
#         turn=Location.WHITE,
#         data=[
#             [1, 1, 1],
#             [1, 0, 1],
#             [1, 1, 1],
#         ],
#     )
#
#     board.move((1, 1))
#     assert board.data == [
#         [0, 0, 0],
#         [0, -1, 0],
#         [0, 0, 0],
#     ]
#
#     board = SGFBoard(
#         shape=(3,3),
#         turn=Location.WHITE,
#         data=[
#             [0, 1, 1],
#             [1, 0, 1],
#             [1, 1, 1],
#         ],
#     )
#
#     with pytest.raises(SGFBoardError) as err:
#         board.move((1, 1))
#
#     assert str(err.value) == "Illegal move: Suicide."
#
#     board = SGFBoard(
#         shape=(4,4),
#         turn=Location.WHITE,
#         data=[
#             [0, -1, 1, 0],
#             [-1, 1, 0, 1],
#             [0, -1, 1, 0],
#             [0,  0, 0, 0],
#         ],
#     )
#
#     board.move((1, 2))
#     assert board.data == [
#         [0, -1,  1, 0],
#         [-1, 0, -1, 1],
#         [0, -1,  1, 0],
#         [0,  0,  0, 0],
#     ]
#
#     with pytest.raises(SGFBoardError) as err:
#         board.move((1, 1))
#         print(board.data)
#
#     assert str(err.value) == "Illegal move: Ko."
