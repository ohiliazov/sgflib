from typing import Iterable
from .exceptions import DuplicateSGFPropertyError, SGFPropertyNotFoundError

from .property import SGFProperty


class SGFNode:
    def __init__(self, props: Iterable[SGFProperty] = None):
        self.props = set(props) if props else set()

    def __str__(self):
        return ";" + "".join(map(str, sorted(self.props)))

    def __repr__(self):
        return f"SGFNode({str(self)})"

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: "SGFNode"):
        return self.props == other.props

    def __len__(self):
        return len(self.props)

    def repr(self, offset: int = 0, indent: int = 2):
        s = " " * offset + repr(self)
        for prop in self.props:
            s += "\n" + " " * (offset + indent) + repr(prop)
        return s

    def get(self, label: str) -> SGFProperty:
        for prop in self.props:
            if prop.label == label:
                return prop
        raise SGFPropertyNotFoundError(label)

    def add(self, new_prop: SGFProperty):
        for prop in self.props:
            if prop.label == new_prop.label:
                raise DuplicateSGFPropertyError()
        self.props.add(new_prop)

    def remove(self, label: str):
        for prop in self.props:
            if prop.label == label:
                return self.props.remove(prop)
        else:
            raise SGFPropertyNotFoundError()

    def __getitem__(self, label: str) -> SGFProperty:
        return self.get(label)

    def __setitem__(self, label: str, value: Iterable[str]) -> SGFProperty:
        return self.add(SGFProperty(label, value))

    def __delitem__(self, label: str):
        return self.remove(label)
