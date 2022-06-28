from typing import List

from .node import SGFNode
from .exceptions import EmptySGFGameTreeError, SGFGameTreeInsertionError


class SGFGameTree:
    def __init__(self, nodes: List[SGFNode], variations: List["SGFGameTree"] = None):
        if not nodes:
            raise EmptySGFGameTreeError("Expected at least one SGFNode in nodes.")

        self.nodes = nodes
        self.variations = variations or []

    def __str__(self):
        return "(" + "".join(map(str, self.nodes)) + "".join(map(str, self.variations)) + ")"

    def __repr__(self):
        return f"SGFGameTree({str(self)})"

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: "SGFGameTree"):
        return self.nodes == other.nodes and self.variations == other.variations

    def pretty(self, offset: int = 0, indent: int = 2):
        s = " " * offset + "(\n" + " " * (offset+indent) + "".join(map(str, self.nodes))
        for tree in self.variations:
            s += "\n" + " " * offset + tree.pretty(offset+indent, indent)
        return s + "\n" + " " * offset + ")"

    def repr(self, offset: int = 0, indent: int = 2):
        s = " " * offset + repr(self)
        for node in self.nodes:
            s += "\n" + node.repr(offset + indent, indent)

        for variation in self.variations:
            s += "\n" + variation.repr(offset + indent, indent)
        return s

    def insert(self, tree: "SGFGameTree", index: int):
        if index < 1:
            raise SGFGameTreeInsertionError("Cannot insert SGFGameTree to the beginning")
        if index < len(self.nodes):
            self.variations = [SGFGameTree(self.nodes[index:], self.variations), tree]
            self.nodes = self.nodes[:index]
        elif self.variations:
            self.variations.append(tree)
        elif index == len(self.nodes):
            self.nodes.extend(tree.nodes)
            self.variations = tree.variations
        else:
            raise SGFGameTreeInsertionError("Index out of bounds of SGFGameTree.")
