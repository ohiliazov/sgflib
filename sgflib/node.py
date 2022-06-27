from typing import Iterable
from .exceptions import SGFNodeDuplicatePropError, SGFNodePropNotFoundError

from .prop import SGFProp


class SGFNode:
    def __init__(self, props: Iterable[SGFProp] = None):
        self.props = set(props) if props else set()

    def __str__(self):
        return ";" + "".join(map(str, self.props))

    def __repr__(self):
        return f"SGFNode({str(self)})"

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: "SGFNode"):
        return self.props == other.props

    def pretty_repr(self, offset: int = 0, indent: int = 2):
        s = " " * offset + repr(self)
        for prop in self.props:
            s += "\n" + " " * (offset + indent) + repr(prop)
        return s

    def add(self, new_prop: SGFProp):
        for prop in self.props:
            if prop.label == new_prop.label:
                raise SGFNodeDuplicatePropError()
        self.props.add(new_prop)

    def remove(self, prop: SGFProp):
        try:
            self.props.remove(prop)
        except ValueError:
            raise SGFNodePropNotFoundError()

    def remove_by_label(self, label: str):
        for prop in self.props:
            if prop.label == label:
                return self.remove(prop)
        raise SGFNodePropNotFoundError()
