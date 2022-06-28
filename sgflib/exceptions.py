class SGFPropertyValueParseError(Exception):
    pass


class SGFPropertyParseError(Exception):
    pass


class SGFNodeParseError(Exception):
    pass


class SGFGameTreeParseError(Exception):
    pass


class SGFPropertyError(Exception):
    pass


class EmptySGFPropertyValueError(SGFPropertyError):
    pass


class DuplicateSGFPropertyValueError(SGFPropertyError):
    pass


class SGFPropertyValueNotFoundError(SGFPropertyError):
    pass


class SGFNodeError(Exception):
    pass


class DuplicateSGFPropertyError(SGFNodeError):
    pass


class SGFPropertyNotFoundError(SGFNodeError):
    pass


class SGFGameTreeError(Exception):
    pass


class EmptySGFGameTreeError(SGFGameTreeError):
    pass


class SGFGameTreeInsertionError(SGFGameTreeError):
    pass
