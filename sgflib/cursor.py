from typing import List

from . import SGFNode, SGFGameTree
from .exceptions import SGFCursorError


class SGFCursor:
    def __init__(self, tree: SGFGameTree):
        self.root_tree = self.tree = tree
        self.index = 0
        self._stack: List[SGFGameTree] = []

    @property
    def node(self) -> SGFNode:
        return self.tree.sequence[self.index]

    def next(self, variation: int = 0) -> SGFNode:
        if self.index + 1 < len(self.tree.sequence):
            if variation != 0:
                raise SGFCursorError("Invalid variation number.")
            self.index += 1
        elif self.tree.variations:
            if variation < len(self.tree.variations):
                self._stack.append(self.tree)
                self.tree = self.tree.variations[variation]
                self.index = 0
            else:
                raise SGFCursorError("Invalid variation number.")
        else:
            raise SGFCursorError("Reached end of SGFGameTree.")

        return self.node

    def previous(self) -> SGFNode:
        if self.index:
            self.index -= 1
        elif self._stack:
            self.tree = self._stack.pop()
            self.index = len(self.tree.sequence) - 1
        else:
            raise SGFCursorError("Reached start of SGFGameTree.")

        return self.node
