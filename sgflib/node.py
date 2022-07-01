from typing import Iterable, Mapping, Dict, List

from .property import SGFProperty
from .property_value import SGFPropertyValue


class SGFNode(Dict[str, Iterable[str]]):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            self.update(*args, **kwargs)

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

    @classmethod
    def from_properties(cls, data: Iterable[SGFProperty]):
        return cls([(p.label, p.values) for p in data])

    @property
    def properties(self) -> List[SGFProperty]:
        return sorted(
            [SGFProperty(label, values) for label, values in self.items()],
            key=lambda p: p.label,
        )

    def __str__(self):
        return ";" + "".join(map(str, self.properties))

    def __repr__(self):
        return f"SGFNode({self})"

    def __setitem__(self, key: str, values: Iterable[str]):
        return super().__setitem__(key, SGFPropertyValue(values))
