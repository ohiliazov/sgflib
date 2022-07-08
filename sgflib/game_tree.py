from typing import List, Dict, Iterable

from .sequence import SGFSequence
from .exceptions import SGFGameTreeError


class SGFGameTree:
    def __init__(
        self,
        sequence: List[Dict[str, Iterable[str]]],
        variations: List["SGFGameTree"] = None,
    ):
        self.sequence = SGFSequence(sequence)
        self.variations = variations or []

    @property
    def sgf(self):
        return (
            "("
            + self.sequence.sgf
            + "".join(tree.sgf for tree in self.variations)
            + ")"
        )

    def __repr__(self):
        return f"SGFGameTree({self.sgf})"

    def __eq__(self, other: "SGFGameTree"):
        return self.sequence == other.sequence and self.variations == other.variations

    def pretty(self, offset: int = 0, indent: int = 2):
        s = " " * offset + "(\n" + " " * (offset + indent) + self.sequence.sgf
        for tree in self.variations:
            s += "\n" + " " * offset + tree.pretty(offset + indent, indent)
        return s + "\n" + " " * offset + ")"

    def insert(self, tree: "SGFGameTree", index: int):
        if index < 1 or index > len(self.sequence):
            raise SGFGameTreeError(f"Cannot insert SGFGameTree at index={index}.")
        if index < len(self.sequence):
            self.variations = [
                SGFGameTree(self.sequence[index:], self.variations),
                tree,
            ]
            self.sequence = SGFSequence(self.sequence[:index])
        elif self.variations:
            self.variations.append(tree)
        else:
            self.sequence.extend(tree.sequence)
            self.variations = tree.variations
