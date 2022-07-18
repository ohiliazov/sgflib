from datetime import date
from sgflib import SGFKifu


def test_new_kifu():
    kifu = SGFKifu()
    today = date.today().isoformat()
    assert (
        kifu.sgf
        == f"(;AP[sgflib:0.1.0]CA[UTF-8]DT[{today}]FF[4]GM[1]KM[6.5]PL[B]RU[Japanese]ST[2]SZ[19])"
    )


def test_kifu_move():
    kifu = SGFKifu(shape=(3, 3))
    kifu.play((1, 2))
    print(kifu.sgf)
    print(kifu.board)
    kifu.previous()
    print(kifu.sgf)
    print(kifu.board)
    kifu.play((1, 2))
    print(kifu.sgf)
    print(kifu.board)
    kifu.play((2, 2))
    print(kifu.sgf)
    print(kifu.board)
