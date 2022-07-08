from typing import Iterable, Mapping, Dict

from .property_value import SGFPropertyValue


class SGFNode(Dict[str, SGFPropertyValue]):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            self.update(*args, **kwargs)

    @property
    def sgf(self) -> str:
        sgf_string = ";"
        for prop_label, prop_value in self.items():
            sgf_string += prop_label + prop_value.sgf
        return sgf_string

    def __repr__(self):
        return f"SGFNode({self.sgf})"

    def update(self, props: Mapping[str, Iterable[str]], **kwargs: Iterable[str]):
        if isinstance(props, Mapping):
            props = props.items()
        props = {label.upper(): SGFPropertyValue(values) for label, values in props}
        kwargs = {
            label.upper(): SGFPropertyValue(values) for label, values in kwargs.items()
        }
        super().update(props, **kwargs)

    def setdefault(
        self, __key: str, __default: Iterable[str] = ...
    ) -> SGFPropertyValue:
        return super().setdefault(__key, SGFPropertyValue(__default))

    def __setitem__(self, key: str, values: Iterable[str]):
        return super().__setitem__(key, SGFPropertyValue(values))
