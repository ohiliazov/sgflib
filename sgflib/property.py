from typing import Iterable

from .property_value import SGFPropertyValue
from .utils import escape_text


class SGFProperty:
    def __init__(self, label: str, values: Iterable[str]):
        self.label = label
        self.values = SGFPropertyValue(values)

    def __str__(self):
        return self.label + "[" + "][".join(map(escape_text, sorted(self.values))) + "]"

    def __repr__(self):
        return f"SGFProperty({self})"

    def add(self, value: str):
        self.values.add(value)

    def remove(self, value: str):
        self.values.remove(value)
