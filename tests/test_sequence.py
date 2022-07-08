import pytest

from sgflib import SGFSequence


@pytest.mark.parametrize(
    "nodes, expected",
    [
        ([{}], ";"),
        ([{"B": {"dd"}}, {"W": ["pp"]}], ";B[dd];W[pp]"),
        (
            [
                {"B": {"dd"}, "C": ["John Doe [3d] \\UA\\"]},
                {"W": ["pp"]},
            ],
            ";B[dd]C[John Doe [3d\\] \\\\UA\\\\];W[pp]",
        ),
    ],
)
def test_print_sequence(nodes, expected):
    sequence = SGFSequence(nodes)
    assert sequence.sgf == expected
    assert repr(sequence) == f"SGFSequence({expected})"
