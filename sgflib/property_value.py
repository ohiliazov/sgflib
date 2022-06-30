from typing import Set, Iterable

from .exceptions import SGFPropertyValueError
from .utils import escape_text


class SGFPropertyValue(Set[str]):
    def __init__(self, data: Iterable[str]):
        if not data:
            raise SGFPropertyValueError("Expected at least one value")
        super().__init__(data)

    def __str__(self):
        return "[" + "][".join(sorted(map(escape_text, self))) + "]"

    def clear(self):
        raise SGFPropertyValueError("Cannot clear SGFPropertyValue")

    def pop(self) -> str:
        if len(self) == 1:
            raise SGFPropertyValueError("Cannot pop last element of SGFPropertyValue")
        return super().pop()

    def remove(self, element: str):
        if element not in self:
            raise SGFPropertyValueError("Element not found in SGFPropertyValue")

        if len(self) == 1:
            raise SGFPropertyValueError(
                "Cannot remove last element of SGFPropertyValue"
            )
        return super().remove(element)

    def discard(self, element: str):
        if element in self and len(self) == 1:
            raise SGFPropertyValueError(
                "Cannot discard last element of SGFPropertyValue"
            )
        return super().discard(element)
