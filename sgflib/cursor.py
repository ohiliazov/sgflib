from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .prop import SGFProp
    from .node import SGFNode
    from .tree import SGFTree


class NavigationError(Exception):
    pass


class SGFCursor:
    def __init__(self, tree: "SGFTree"):
        self.root_tree = self.tree = tree
        self.index = 0
        self._stack: List["SGFTree"] = []

    @property
    def current_node(self) -> "SGFNode":
        return self.tree.nodes[self.index]

    @property
    def at_start(self) -> bool:
        return self.index == 0 and not self._stack

    @property
    def at_end(self) -> bool:
        return self.index == len(self.tree.nodes) - 1 and not self.tree.variations

    def next(self, variation: int = 0) -> "SGFNode":
        if self.index + 1 < len(self.tree.nodes):
            if variation != 0:
                raise NavigationError("Invalid variation number.")
            self.index += 1
        elif self.tree.variations:
            if variation < len(self.tree.variations):
                self._stack.append(self.tree)
                self.tree = self.tree.variations[variation]
                self.index = 0
            else:
                raise NavigationError("Invalid variation number.")
        else:
            raise NavigationError("Reached end of SGFTree.")

        return self.current_node

    def previous(self) -> "SGFNode":
        if self.index:
            self.index -= 1
        elif self._stack:
            self.tree = self._stack.pop()
            self.index = len(self.tree.nodes) - 1
        else:
            raise NavigationError("Reached start of SGFTree.")

        return self.current_node

    def insert_tree(self, tree: "SGFTree"):
        return self.tree.insert(tree, self.index)

    def insert_prop(self, prop: "SGFProp"):
        self.current_node.props.append(prop)
