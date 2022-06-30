import pytest

from sgflib import SGFParser, SGFCursor
from sgflib.exceptions import SGFCursorError


TEST_SGF = """
(
  ;AB[dd][dp][pp]FF[4]GM[1]KM[6.5]PL[W]SZ[19];W[pd];B[qf]
  (
    ;W[nc];B[rd]
  )
  (
    ;W[qh]
      (
      ;B[qc];W[qd]
    )
      (
      ;B[of]
    )
  )
)
"""


def test_cursor():
    game_tree = SGFParser(TEST_SGF).parse_game_tree()
    cursor = SGFCursor(game_tree)

    assert str(cursor.node) == ";AB[dd][dp][pp]FF[4]GM[1]KM[6.5]PL[W]SZ[19]"

    with pytest.raises(SGFCursorError) as err:
        cursor.previous()

    assert str(err.value) == "Reached start of SGFGameTree."

    cursor.next()
    assert str(cursor.node) == ";W[pd]"

    with pytest.raises(SGFCursorError) as err:
        cursor.next(1)

    assert str(err.value) == "Invalid variation number."

    cursor.previous()
    assert str(cursor.node) == ";AB[dd][dp][pp]FF[4]GM[1]KM[6.5]PL[W]SZ[19]"

    cursor.index = len(cursor.tree.sequence) - 1
    assert str(cursor.node) == ";B[qf]"

    cursor.next(1)
    assert str(cursor.node) == ";W[qh]"

    cursor.previous()
    assert str(cursor.node) == ";B[qf]"
    assert cursor.root_tree == cursor.tree

    with pytest.raises(SGFCursorError) as err:
        cursor.next(2)

    assert str(err.value) == "Invalid variation number."

    cursor.next()
    assert str(cursor.node) == ";W[nc]"
    assert cursor.root_tree != cursor.tree

    cursor.next()
    assert str(cursor.node) == ";B[rd]"
    assert cursor.root_tree != cursor.tree

    with pytest.raises(SGFCursorError) as err:
        cursor.next()

    assert str(err.value) == "Reached end of SGFGameTree."
