from typing import List, Iterable, Dict

from .exceptions import SGFSequenceError
from .node import SGFNode


class SGFSequence(List[Dict[str, Iterable[str]]]):
    def __init__(self, sequence: List[Dict[str, Iterable[str]]]):
        if not sequence:
            raise SGFSequenceError("Expected at least one SGFNode in SGFSequence.")
        super().__init__(map(SGFNode, sequence))

    def __str__(self):
        return "".join(map(str, self))

    def __repr__(self):
        return f"SGFSequence({str(self)})"
