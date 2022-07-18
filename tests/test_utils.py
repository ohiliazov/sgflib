import pytest
from sgflib.exceptions import SGFCoordinateError, SGFPointError
from sgflib.utils import coord_to_point, point_to_coord


@pytest.mark.parametrize(
    "coord, point",
    [
        ((0, 0), "aa"),
        ((0, 25), "az"),
        ((0, 26), "aA"),
        ((0, 51), "aZ"),
        ((25, 0), "za"),
        ((25, 25), "zz"),
        ((25, 26), "zA"),
        ((25, 51), "zZ"),
        ((26, 0), "Aa"),
        ((26, 25), "Az"),
        ((26, 26), "AA"),
        ((26, 51), "AZ"),
        ((51, 0), "Za"),
        ((51, 25), "Zz"),
        ((51, 26), "ZA"),
        ((51, 51), "ZZ"),
    ],
)
def test_coord_to_point(coord, point):
    assert coord_to_point(coord) == point


@pytest.mark.parametrize(
    "point, coord",
    [
        ("aa", (0, 0)),
        ("az", (0, 25)),
        ("aA", (0, 26)),
        ("aZ", (0, 51)),
        ("za", (25, 0)),
        ("zz", (25, 25)),
        ("zA", (25, 26)),
        ("zZ", (25, 51)),
        ("Za", (51, 0)),
        ("Zz", (51, 25)),
        ("ZA", (51, 26)),
        ("ZZ", (51, 51)),
    ],
)
def test_point_to_coord(point, coord):
    assert point_to_coord(point) == coord


@pytest.mark.parametrize(
    "x, y",
    [
        (-1, -1),
        (-1, 0),
        (-1, 52),
        (0, -1),
        (0, 52),
        (52, -1),
        (52, 0),
        (52, 52),
    ],
)
def test_coord_to_point_error(x, y):
    coord = (x, y)
    with pytest.raises(SGFCoordinateError) as err:
        coord_to_point(coord)
    assert str(err.value) == f"Invalid SGFCoordinate: {coord}."


def test_point_to_coord_error():
    with pytest.raises(SGFPointError) as err:
        point_to_coord("ąa")
    assert str(err.value) == "Invalid SGFPoint: ąa."
