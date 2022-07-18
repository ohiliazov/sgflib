from copy import deepcopy
from typing import TYPE_CHECKING, Set, List, Union

from .enums import Player, Location
from .exceptions import SGFBoardError

if TYPE_CHECKING:
    from .types import SGFCoordinateType


class SGFBoard:
    def __init__(
        self,
        shape: "SGFCoordinateType",
        player: Union[str, Player],
        data: List[List[int]] = None,
        allow_super_ko: bool = True,
        allow_suicide: bool = False,
    ):
        rows, cols = shape

        self.shape = shape
        self.player = Player(player)
        self.captured = {Player.BLACK: 0, Player.WHITE: 0}
        self.history = []
        self.allow_super_ko = allow_super_ko
        self.allow_suicide = allow_suicide

        if not (0 < rows <= 52 and 0 < cols <= 52):
            raise SGFBoardError("Board dimensions should be between 1 and 52.")

        if data:
            if len(data) != rows or any(len(row) != cols for row in data):
                raise SGFBoardError(f"Data should be of shape {shape}.")
            self.data = [[Location(point) for point in row] for row in data]
        else:
            self.data = [[Location.EMPTY for _ in range(cols)] for _ in range(rows)]

    def __str__(self, spaces: int = 1):
        width, height = self.shape
        s = ""
        for x in range(height):
            for y in range(width):
                s += self.data[y][x].pretty() + " " * spaces
            s += "\n"
        return s

    def __repr__(self):
        return f"SGFBoard({self})"

    def push(self):
        """Save position to history"""
        state = deepcopy(self.data), self.player, self.captured.copy()
        self.history.append(state)

    def undo(self):
        """Load previous position"""
        self.data, self.player, self.captured = self.history.pop()

    def _is_valid_coord(self, coord: "SGFCoordinateType") -> bool:
        x, y = coord
        rows, cols = self.shape
        return 0 <= x < rows and 0 <= y < cols

    def _get_loc(self, coord: "SGFCoordinateType") -> Location:
        if self._is_valid_coord(coord):
            x, y = coord
            return self.data[x][y]
        raise SGFBoardError("Wrong coordinate")

    def _set_coord(self, coord: "SGFCoordinateType", color: Location):
        if self._is_valid_coord(coord):
            x, y = coord
            self.data[x][y] = color

    def _get_adjacent(self, coord: "SGFCoordinateType") -> List["SGFCoordinateType"]:
        x, y = coord
        for adjacent in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if self._is_valid_coord(adjacent):
                yield adjacent

    def _get_group(self, coord: "SGFCoordinateType") -> Set["SGFCoordinateType"]:
        loc = self._get_loc(coord)

        unexplored = {coord}
        group = set()
        while unexplored:
            coord = unexplored.pop()
            group.add(coord)

            for coord in self._get_adjacent(coord):
                if coord not in group and self._get_loc(coord) is loc:
                    unexplored.add(coord)

        return group

    def _is_alive(self, group: Set["SGFCoordinateType"]) -> bool:
        return any(
            self._get_loc(coord) is Location.EMPTY
            for stone in group
            for coord in self._get_adjacent(stone)
        )

    def _kill_group(self, coord: "SGFCoordinateType", player: Player) -> int:
        if self._get_loc(coord) != player.loc():
            return 0

        group = self._get_group(coord)

        if self._is_alive(group):
            return 0

        for coord in group:
            self._set_coord(coord, Location.EMPTY)

        return len(group)

    def _capture_stones(self, coord: "SGFCoordinateType"):
        for adjacent in self._get_adjacent(coord):
            self.captured[self.player] += self._kill_group(adjacent, -self.player)

    def _check_point(self, coord: "SGFCoordinateType"):
        if self._get_loc(coord) is not Location.EMPTY:
            raise SGFBoardError("Not empty")

    def _check_suicide(self, coord: "SGFCoordinateType"):
        group = self._get_group(coord)
        if not self._is_alive(group):
            raise SGFBoardError("Suicide")

    def _check_ko(self):
        if len(self.history) > 1 and self.history[-2][0] == self.data:
            raise SGFBoardError("Ko")

    def _check_super_ko(self):
        if any(data == self.data for data, *_ in self.history[-3::-1]):
            raise SGFBoardError("Super-Ko")

    def _move(self, coord: "SGFCoordinateType"):
        if not coord:
            return

        self._check_point(coord)
        self._set_coord(coord, self.player.loc())
        self._capture_stones(coord)

        if self.allow_suicide:
            self.captured[-self.player] += self._kill_group(coord, self.player)
        else:
            self._check_suicide(coord)

        if self.allow_super_ko:
            self._check_ko()
        else:
            self._check_super_ko()

        self.player = -self.player

    def move(self, coord: "SGFCoordinateType" = None):
        self.push()
        try:
            self._move(coord)
        except SGFBoardError as err:
            self.undo()
            raise SGFBoardError(f"Illegal move: {err}.") from err
