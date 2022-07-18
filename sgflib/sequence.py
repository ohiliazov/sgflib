from typing import TYPE_CHECKING, List

from .exceptions import SGFSequenceError
from .node import SGFNode

if TYPE_CHECKING:
    from .types import SGFNodeType


class SGFSequence(List[SGFNode]):
    def __init__(self, sequence: List["SGFNodeType"]):
        if not sequence:
            raise SGFSequenceError("Expected at least one SGFNode in SGFSequence.")
        super().__init__(map(SGFNode, sequence))

    @property
    def sgf(self) -> str:
        return "".join(node.sgf for node in self)

    def __repr__(self):
        return f"SGFSequence({self.sgf})"

    def copy(self) -> "SGFSequence":
        return SGFSequence([node.copy() for node in self])

    def cut(self, index: int) -> "SGFSequence":
        removed = []
        while len(self) > index:
            removed.insert(0, self.pop())
        return SGFSequence(removed)
