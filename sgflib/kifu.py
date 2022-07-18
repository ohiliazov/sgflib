from datetime import date

from . import (
    SGFBoard,
    SGFCursor,
    SGFGameTree,
    SGFNode,
    SGFPropertyValue,
)
from .types import SGFCoordinateType
from .enums import Player, GoRules
from .exceptions import SGFCursorError
from .utils import coord_to_point, point_to_coord


def make_root_node(
    shape: SGFCoordinateType, player: Player, rules: str, komi: float
) -> SGFNode:
    cols, rows = shape

    return SGFNode(
        {
            "GM": ["1"],
            "FF": ["4"],
            "CA": ["UTF-8"],
            "AP": ["sgflib:0.1.0"],
            "ST": ["2"],
            "RU": [rules],
            "SZ": [f"{rows}"] if rows == cols else [f"{rows}:{cols}"],
            "KM": [str(int(komi) + 0.5 if komi % 1 else 0)],
            "DT": [date.today().isoformat()],
            "PL": [player.value],
        }
    )


def make_game_tree(
    shape: SGFCoordinateType, player: Player, rules: str, komi: float
) -> SGFGameTree:
    return SGFGameTree([make_root_node(shape, player, rules, komi)])


class SGFKifu:
    def __init__(
        self,
        shape: SGFCoordinateType = (19, 19),
        player: Player = Player.BLACK,
        rules: GoRules = GoRules.JAPANESE,
        komi: float = 6.5,
        game_tree: SGFGameTree = None,
    ):
        self.board = SGFBoard(shape, player)

        if not game_tree:
            game_tree = make_game_tree(shape, player, rules, komi)

        self.cursor = SGFCursor(game_tree)

    @property
    def player(self) -> Player:
        return self.board.player

    @property
    def sgf(self):
        return self.cursor.root_tree.sgf

    def _node_move(self) -> SGFPropertyValue:
        return self.cursor.node.get(self.player.value)

    def next(self, variation: int = 0):
        self.cursor.next(variation)
        self.board.move(point_to_coord(sorted(self._node_move())[0]))

    def previous(self):
        self.board.undo()
        self.cursor.previous()

    def _get_next_moves(self):
        moves = {}
        variation = 0
        while True:
            try:
                self.cursor.next(variation)
            except SGFCursorError:
                break

            moves[variation] = self._node_move()
            self.cursor.previous()
            variation += 1

        return moves

    def play(self, coord: SGFCoordinateType):
        point = coord_to_point(coord)
        for index, move in self._get_next_moves().items():
            if move == {point}:
                return self.next(index)

        self.board.move(coord)
        tree = ([{(-self.player).value: [point]}], [])
        tree_index = self.cursor.insert(tree)
        self.cursor.next(tree_index)
