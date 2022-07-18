from typing import Tuple, List, Iterable, Mapping


SGFPropertyValueType = Iterable[str]
SGFNodeType = Mapping[str, SGFPropertyValueType]
SGFSequenceType = List[SGFNodeType]
SGFGameTreeType = Tuple[SGFSequenceType, List["SGFGameTreeType"]]

SGFCoordinateType = Tuple[int, int]
