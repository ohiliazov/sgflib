from typing import List

from .game_tree import SGFGameTree


class SGFCollection(List[SGFGameTree]):
    @property
    def sgf(self):
        return "\n\n".join(tree.sgf for tree in self)

    def __repr__(self):
        return f"SGFCollection({self.sgf})"

    def pretty(self):
        return "\n\n".join([tree.pretty() for tree in self])
