from typing import List, Iterable, Dict

from .exceptions import SGFSequenceError
from .node import SGFNode


class SGFSequence(List[SGFNode]):
    def __init__(self, sequence: List[Dict[str, Iterable[str]]]):
        if not sequence:
            raise SGFSequenceError("Expected at least one SGFNode in SGFSequence.")
        super().__init__(map(SGFNode, sequence))

    @property
    def sgf(self) -> str:
        return "".join(node.sgf for node in self)

    def __repr__(self):
        return f"SGFSequence({self.sgf})"
