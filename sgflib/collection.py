from typing import List

from .game_tree import SGFGameTree


class SGFCollection(list):
    def __init__(self, data: List[SGFGameTree]):
        super().__init__(data)

    def __str__(self):
        return "\n\n".join(map(str, self))

    def __repr__(self):
        return f"SGFCollection({str(self)})"
