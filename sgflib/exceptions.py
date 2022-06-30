from json import JSONDecodeError


class SGFParserError(JSONDecodeError):
    pass


class SGFPropertyError(Exception):
    pass


class SGFPropertyValueError(Exception):
    pass


class EmptySGFPropertyValueError(SGFPropertyError):
    pass


class DuplicateSGFPropertyValueError(SGFPropertyError):
    pass


class SGFPropertyValueNotFoundError(SGFPropertyError):
    pass


class SGFGameTreeError(Exception):
    pass


class SGFSequenceError(Exception):
    pass


class SGFCursorError(Exception):
    pass
