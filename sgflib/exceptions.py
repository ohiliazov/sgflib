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


class SGFNodeDuplicatePropError(SGFNodeError):
    pass


class SGFNodePropNotFoundError(SGFNodeError):
    pass
