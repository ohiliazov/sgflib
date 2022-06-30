from collections import UserList
from typing import List

from .exceptions import SGFSequenceError
from .node import SGFNode


class SGFSequence(UserList):
    def __init__(self, nodes: List[SGFNode]):
        if not nodes:
            raise SGFSequenceError("Expected at least one SGFNode in SGFSequence.")
        super(SGFSequence, self).__init__(nodes)

    def __str__(self):
        return "".join(map(str, self.data))

    def __repr__(self):
        return f"SGFSequence({str(self)})"
