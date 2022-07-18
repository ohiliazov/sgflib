from enum import Enum, IntEnum


class Location(IntEnum):
    EMPTY = 0
    BLACK = 1
    WHITE = -1

    def pretty(self):
        if self is self.BLACK:
            return "⬤"
        if self is self.WHITE:
            return "◯"
        return "+"


class Player(str, Enum):
    BLACK = "B"
    WHITE = "W"

    def __neg__(self) -> "Player":
        return Player.BLACK if self is Player.WHITE else Player.WHITE

    def loc(self) -> "Location":
        return Location.BLACK if self is Player.BLACK else Location.WHITE


class GoRules(str, Enum):
    JAPANESE = "Japanese"
    CHINESE = "Chinese"
