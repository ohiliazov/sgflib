from typing import Iterable

from .helpers import escape_text
from .exceptions import DuplicateSGFPropertyValueError, EmptySGFPropertyValueError, SGFPropertyValueNotFoundError


class SGFProperty:
    def __init__(self, label: str, values: Iterable[str] = None):
        self.label = label
        self.values = set(values) if values else set()

    def __str__(self):
        return self.label + "[" + "][".join(map(escape_text, sorted(self.values))) + "]"

    def __repr__(self):
        return f"SGFProperty({str(self)})"

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: "SGFProperty"):
        return self.label == other.label and self.values == other.values

    def __lt__(self, other: "SGFProperty"):
        return self.label < other.label

    def add(self, value: str):
        if value in self.values:
            raise DuplicateSGFPropertyValueError(value)
        self.values.add(value)

    def remove(self, value: str):
        if value not in self.values:
            raise SGFPropertyValueNotFoundError()
        if self.values == {value}:
            raise EmptySGFPropertyValueError()
        self.values.remove(value)
