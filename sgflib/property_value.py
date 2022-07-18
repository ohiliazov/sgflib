from typing import TYPE_CHECKING, Set

from .exceptions import SGFPropertyValueError
from .utils import escape_text

if TYPE_CHECKING:
    from .types import SGFPropertyValueType


class SGFPropertyValue(Set[str]):
    def __init__(self, data: "SGFPropertyValueType"):
        if not data:
            raise SGFPropertyValueError("Cannot be empty")
        super().__init__(data)

    @property
    def sgf(self) -> str:
        return "[" + "][".join(sorted(map(escape_text, self))) + "]"

    def __repr__(self):
        return f"SGFPropertyValue({self.sgf})"

    def copy(self) -> "SGFPropertyValue":
        return SGFPropertyValue(self)

    def clear(self):
        raise SGFPropertyValueError("Cannot clear")

    def pop(self) -> str:
        if len(self) == 1:
            raise SGFPropertyValueError("Cannot pop last element")
        return super().pop()

    def remove(self, element: str):
        if self == {element}:
            raise SGFPropertyValueError("Cannot remove last element")
        return super().remove(element)

    def discard(self, element: str):
        if self == {element}:
            raise SGFPropertyValueError("Cannot discard last element")
        return super().discard(element)
