from copy import deepcopy
from enum import IntEnum
from typing import Tuple, Set, List

from sgflib.exceptions import SGFBoardError


class Location(IntEnum):
    EMPTY = 0
    BLACK = 1
    WHITE = -1

    def __neg__(self) -> "Location":
        if self is Location.BLACK:
            return Location.WHITE
        if self is Location.WHITE:
            return Location.BLACK

    def empty(self) -> bool:
        return self is Location.EMPTY


Coordinate = Tuple[int, int]


class SGFBoard:
    def __init__(
        self,
        shape: Tuple[int, int],
        turn: int,
        data: List[List[int]] = None,
        allow_super_ko: bool = True,
        allow_suicide: bool = False,
    ):
        rows, cols = shape

        self.shape = shape
        self.turn = Location(turn)
        self.data = [[Location.EMPTY for _ in range(cols)] for _ in range(rows)]
        self.captured = {
            Location.BLACK: 0,
            Location.WHITE: 0,
        }
        self.history = []
        self.allow_super_ko = allow_super_ko
        self.allow_suicide = allow_suicide

        if not (0 < rows <= 52 and 0 < cols <= 52):
            raise SGFBoardError("Board dimensions should be between 1 and 52.")

        if self.turn.empty():
            raise SGFBoardError("Turn should not be Location.EMPTY.")

        if data:
            if len(data) != rows or any(len(row) != cols for row in data):
                raise SGFBoardError(f"Data should be of shape {shape}")
            self.data = [[Location(point) for point in row] for row in data]

    def _push_history(self):
        """Save position to history"""
        state = deepcopy(self.data), self.turn, self.captured.copy()
        self.history.append(state)

    def _pop_history(self):
        """Load previous position"""
        self.data, self.turn, self.captured = self.history.pop()

    def _is_valid_coord(self, coord: Coordinate) -> bool:
        x, y = coord
        rows, cols = self.shape
        return 0 <= x < rows and 0 <= y < cols

    def _get_coord(self, coord: Coordinate) -> Location:
        if self._is_valid_coord(coord):
            x, y = coord
            return self.data[x][y]
        raise SGFBoardError("Wrong coordinate")

    def _set_coord(self, coord: Coordinate, color: Location):
        if self._is_valid_coord(coord):
            x, y = coord
            self.data[x][y] = color

    def _get_adjacent(self, coord: Coordinate) -> List[Coordinate]:
        x, y = coord
        for adjacent in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if self._is_valid_coord(adjacent):
                yield adjacent

    def _get_group(self, coord: Coordinate) -> Set[Coordinate]:
        color = self._get_coord(coord)

        unexplored = {coord}
        group = set()
        while unexplored:
            coord = unexplored.pop()
            group.add(coord)

            for coord in self._get_adjacent(coord):
                if coord not in group and self._get_coord(coord) == color:
                    unexplored.add(coord)

        return group

    def _is_alive(self, group: Set[Coordinate]) -> bool:
        return any(
            self._get_coord(coord).empty()
            for stone in group
            for coord in self._get_adjacent(stone)
        )

    def _kill_group(self, coord: Coordinate, color: Location) -> int:
        if self._get_coord(coord) != color:
            return 0

        group = self._get_group(coord)

        if self._is_alive(group):
            return 0

        for coord in group:
            self._set_coord(coord, Location.EMPTY)

        return len(group)

    def _capture_stones(self, coord: Coordinate):
        for adjacent in self._get_adjacent(coord):
            self.captured[self.turn] += self._kill_group(adjacent, -self.turn)

    def _check_point(self, point: Coordinate):
        if not self._get_coord(point).empty():
            raise SGFBoardError("Not empty")

    def _check_suicide(self, coord: Coordinate):
        group = self._get_group(coord)
        if not self._is_alive(group):
            raise SGFBoardError("Suicide")

    def _check_ko(self):
        if len(self.history) > 1 and self.history[-2][0] == self.data:
            raise SGFBoardError("Ko")

    def _check_super_ko(self):
        if any(data == self.data for data, *_ in self.history[-3::-1]):
            raise SGFBoardError("Super-Ko")

    def _move(self, coord: Coordinate):
        self._check_point(coord)
        self._set_coord(coord, self.turn)
        self._capture_stones(coord)

        if self.allow_suicide:
            self.captured[-self.turn] += self._kill_group(coord, self.turn)
        else:
            self._check_suicide(coord)

        if self.allow_super_ko:
            self._check_ko()
        else:
            self._check_super_ko()

        self.turn = -self.turn

    def move(self, point: Coordinate):
        self._push_history()
        try:
            self._move(point)
        except SGFBoardError as err:
            self._pop_history()
            raise SGFBoardError(f"Illegal move: {err}.") from err
