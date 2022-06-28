class SGFPropValueParseError(Exception):
    pass


class SGFPropParseError(Exception):
    pass


class SGFNodeParseError(Exception):
    pass


class SGFTreeParseError(Exception):
    pass


class SGFPropError(Exception):
    pass


class EmptySGFPropValueError(SGFPropError):
    pass


class DuplicateSGFPropValueError(SGFPropError):
    pass


class SGFPropValueNotFoundError(SGFPropError):
    pass


class SGFNodeError(Exception):
    pass


class DuplicateSGFPropError(SGFNodeError):
    pass


class SGFPropNotFoundError(SGFNodeError):
    pass


class SGFTreeError(Exception):
    pass


class EmptySGFTreeError(SGFTreeError):
    pass


class SGFTreeInsertionError(SGFTreeError):
    pass
