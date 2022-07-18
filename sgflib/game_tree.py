from typing import TYPE_CHECKING, List, Tuple, Iterable

from .sequence import SGFSequence
from .exceptions import SGFGameTreeError

if TYPE_CHECKING:
    from .types import SGFSequenceType, SGFGameTreeType


class SGFGameTree(Tuple[SGFSequence, List["SGFGameTree"]]):
    def __new__(
        cls,
        sequence: "SGFSequenceType",
        variations: Iterable["SGFGameTreeType"] = (),
    ):
        sequence = SGFSequence(sequence)
        variations = [SGFGameTree(*tree) for tree in variations]
        return super().__new__(cls, (sequence, variations))

    def __init__(self, *_, **__):
        self.sequence, self.variations = self

    def __repr__(self):
        return f"SGFGameTree({self.sgf})"

    @property
    def sgf(self):
        return (
            "("
            + self.sequence.sgf
            + "".join(tree.sgf for tree in self.variations)
            + ")"
        )

    def __eq__(self, other: "SGFGameTreeType"):
        return super().__eq__(SGFGameTree(*other))

    def copy(self) -> "SGFGameTree":
        return SGFGameTree(
            sequence=self.sequence.copy(),
            variations=[tree.copy() for tree in self.variations],
        )

    def pretty(self, offset: int = 0, indent: int = 2):
        s = " " * offset + "(\n" + " " * (offset + indent) + self.sequence.sgf
        for tree in self.variations:
            s += "\n" + " " * offset + tree.pretty(offset + indent, indent)
        return s + "\n" + " " * offset + ")"

    def insert(self, tree: "SGFGameTreeType", index: int) -> int:
        tree = SGFGameTree(*tree)
        if index < 1 or index > len(self.sequence):
            raise SGFGameTreeError(f"Cannot insert SGFGameTree at index={index}.")
        if index < len(self.sequence):
            main_tree = SGFGameTree(
                sequence=self.sequence.cut(index),
                variations=[tree.copy() for tree in self.variations],
            )
            self.variations.clear()
            self.variations.extend([main_tree, tree])
            return 1
        if self.variations:
            self.variations.append(tree)
            return len(self.variations) - 1

        self.sequence.extend(tree.sequence)
        self.variations.extend(tree.variations)
        return 0

    def cut_tree(self, index: int) -> "SGFGameTree":
        if index < 1 or index > len(self.sequence) - 1:
            raise SGFGameTreeError(f"Cannot cut SGFSequence at index={index}.")
        sequence = self.sequence.cut(index)
        variations = self.variations.copy()
        self.variations.clear()
        return SGFGameTree(sequence, variations)

    def cut_variation(self, index: int):
        if not (0 <= index < len(self.variations)):
            raise SGFGameTreeError(
                f"Cannot cut variation SGFGameTree at index={index}."
            )
        self.variations.pop(index)
