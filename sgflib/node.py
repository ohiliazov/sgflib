from typing import TYPE_CHECKING, Mapping, Dict

from .property_value import SGFPropertyValue

if TYPE_CHECKING:
    from .types import SGFNodeType, SGFPropertyValueType


class SGFNode(Dict[str, SGFPropertyValue]):
    def __init__(self, data: "SGFNodeType" = None, **kwargs: "SGFPropertyValueType"):
        super().__init__()
        self.update(data, **kwargs)

    @property
    def sgf(self) -> str:
        sgf_string = ";"
        for prop_label, prop_value in sorted(self.items()):
            sgf_string += prop_label + prop_value.sgf
        return sgf_string

    def __repr__(self):
        return f"SGFNode({self.sgf})"

    def copy(self) -> "SGFNode":
        return SGFNode({key: value.copy() for key, value in self.items()})

    def update(
        self,
        data: "SGFNodeType" = None,
        **kwargs: "SGFPropertyValueType",
    ):
        data = data or []
        if isinstance(data, Mapping):
            data = data.items()
        data = {label.upper(): SGFPropertyValue(values) for label, values in data}

        kwargs = {
            label.upper(): SGFPropertyValue(values) for label, values in kwargs.items()
        }
        super().update(data, **kwargs)

    def setdefault(
        self, key: str, default: "SGFPropertyValueType" = ...
    ) -> SGFPropertyValue:
        return super().setdefault(key, SGFPropertyValue(default))

    def __setitem__(self, key: str, values: "SGFPropertyValueType"):
        return super().__setitem__(key, SGFPropertyValue(values))
