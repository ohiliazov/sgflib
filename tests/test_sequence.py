import pytest

from sgflib import SGFSequence, SGFNode


@pytest.mark.parametrize(
    "nodes, expected",
    [
        ([SGFNode()], ";"),
        ([SGFNode({"B": {"dd"}}), SGFNode({"W": ["pp"]})], ";B[dd];W[pp]"),
        (
            [
                SGFNode(
                    {
                        "B": {"dd"},
                        "C": ["John Doe [3d] \\UA\\"],
                    }
                ),
                SGFNode({"W": ["pp"]}),
            ],
            ";B[dd]C[John Doe [3d\\] \\\\UA\\\\];W[pp]",
        ),
    ],
)
def test_print_sequence(nodes, expected):
    sequence = SGFSequence(nodes)
    assert str(sequence) == expected
    assert repr(sequence) == f"SGFSequence({expected})"
