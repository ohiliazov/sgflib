import re
from string import ascii_letters
from typing import TYPE_CHECKING

from .exceptions import SGFCoordinateError, SGFPointError

if TYPE_CHECKING:
    from .types import SGFCoordinateType

reCharsToEscape = re.compile(r"([]\\])")  # characters that need to be \escaped


def convert_control_chars(s: str) -> str:
    """Converts control characters in [text] to spaces. Override for variant behaviour."""
    return s.translate(
        str.maketrans(
            "\000\001\002\003\004\005\006\007\010\011"
            "\013\014\016\017\020\021\022\023\024\025"
            "\026\027\030\031\032\033\034\035\036\037",
            " " * 30,
        )
    )


def escape_text(s: str):
    return reCharsToEscape.sub(r"\\\1", s)


def coord_to_point(coord: "SGFCoordinateType") -> str:
    x, y = coord
    if not (0 <= x < 52 and 0 <= y < 52):
        raise SGFCoordinateError(f"Invalid SGFCoordinate: {coord}.")
    return ascii_letters[x] + ascii_letters[y]


def point_to_coord(point: str) -> "SGFCoordinateType":
    x, y = point
    if x not in ascii_letters or y not in ascii_letters:
        raise SGFPointError(f"Invalid SGFPoint: {point}.")
    return ascii_letters.index(x), ascii_letters.index(y)
