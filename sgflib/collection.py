from typing import List

from .game_tree import SGFGameTree


class SGFCollection(List[SGFGameTree]):
    def __str__(self):
        return "\n\n".join(map(str, self))

    def __repr__(self):
        return f"SGFCollection({self})"

    def pretty(self):
        return "\n\n".join([tree.pretty() for tree in self])
