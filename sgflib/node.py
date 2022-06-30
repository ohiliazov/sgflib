from typing import Iterable, Dict, List

from .property import SGFProperty
from .property_value import SGFPropertyValue


class SGFNode(Dict[str, SGFPropertyValue]):
    def __init__(self, seq=None):
        super().__init__(seq or {})
        self.update({label: SGFPropertyValue(values) for label, values in self.items()})

    @classmethod
    def from_properties(cls, data: Iterable[SGFProperty]):
        return cls([(p.label, p.values) for p in data])

    def properties(self) -> List[SGFProperty]:
        return [SGFProperty(label, values) for label, values in self.items()]

    def __str__(self):
        return ";" + "".join(sorted(map(str, self.properties())))

    def __repr__(self):
        return f"SGFNode({str(self)})"

    def __setitem__(self, key: str, values: Iterable[str]):
        return super().__setitem__(key, SGFPropertyValue(values))
