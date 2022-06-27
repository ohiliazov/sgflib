from typing import List

from .node import SGFNode


class SGFTree:
    def __init__(self, nodes: List[SGFNode], variations: List["SGFTree"] = None):
        self.nodes = nodes
        self.variations = variations or []

    def __str__(self):
        return "(" + "".join(map(str, self.nodes)) + "".join(map(str, self.variations)) + ")"

    def __repr__(self):
        return f"SGFTree({str(self)})"

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: "SGFTree"):
        return self.nodes == other.nodes and self.variations == other.variations

    def pretty(self, offset: int = 0, indent: int = 2):
        s = " " * offset + "(\n" + " " * (offset+indent) + "".join(map(str, self.nodes))
        for tree in self.variations:
            s += "\n" + " " * offset + tree.pretty(offset+indent, indent)
        return s + "\n" + " " * offset + ")"

    def pretty_repr(self, offset: int = 0, indent: int = 4):
        s = " " * offset + repr(self)
        for node in self.nodes:
            s += "\n" + node.pretty_repr(offset + indent, indent)

        for variation in self.variations:
            s += "\n" + variation.pretty_repr(offset + indent, indent)
        return s

    def insert(self, tree: "SGFTree", index: int = 0):
        if index < len(self.nodes) - 1:
            main_tree = SGFTree(self.nodes[index:], self.variations)
            self.nodes = self.nodes[:index]
            self.variations = [main_tree, tree]
        elif self.variations:
            self.variations.append(tree)
        else:
            self.nodes.extend(tree.nodes)
            self.variations = tree.variations
