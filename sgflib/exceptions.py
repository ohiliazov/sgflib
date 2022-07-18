class SGFParserError(ValueError):
    def __init__(self, msg: str, data: str, index: int):
        lineno = data.count("\n", 0, index) + 1
        colno = index - data.rfind("\n", 0, index)
        errmsg = f"{msg}: line {lineno} column {colno} (char {index})"

        super().__init__(errmsg)
        self.msg = msg
        self.data = data
        self.index = index
        self.lineno = lineno
        self.colno = colno


class SGFPropertyValueError(Exception):
    pass


class SGFGameTreeError(Exception):
    pass


class SGFSequenceError(Exception):
    pass


class SGFCursorError(Exception):
    pass


class SGFBoardError(Exception):
    pass


class SGFCoordinateError(Exception):
    pass


class SGFPointError(Exception):
    pass
