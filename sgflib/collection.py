from typing import TYPE_CHECKING, List, Iterable

from .game_tree import SGFGameTree

if TYPE_CHECKING:
    from .types import SGFGameTreeType


class SGFCollection(List[SGFGameTree]):
    def __init__(self, data: Iterable["SGFGameTreeType"]):
        super().__init__([SGFGameTree(*tree) for tree in data])

    @property
    def sgf(self):
        return "\n\n".join(tree.sgf for tree in self)

    def __repr__(self):
        return f"SGFCollection({self.sgf})"

    def pretty(self):
        return "\n\n".join([tree.pretty() for tree in self])

    def copy(self) -> "SGFCollection":
        return SGFCollection([tree.copy() for tree in self])
