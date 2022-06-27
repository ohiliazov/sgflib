import re

reCharsToEscape = re.compile(r"([]\\])")  # characters that need to be \escaped


def convert_control_chars(s: str) -> str:
    """Converts control characters in [text] to spaces. Override for variant behaviour."""
    return s.translate(
        str.maketrans(
            "\000\001\002\003\004\005\006\007\010\011"
            "\013\014\016\017\020\021\022\023\024\025"
            "\026\027\030\031\032\033\034\035\036\037",
            " " * 30)
    )


def escape_text(s: str):
    return reCharsToEscape.sub(r"\\\1", s)
