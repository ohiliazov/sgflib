import pytest

from sgflib import SGFCollection


@pytest.mark.parametrize(
    "trees, expected, expected_pretty",
    [
        ([([{}], [])], "(;)", "(\n  ;\n)"),
        (
            [
                (
                    [
                        {"AB": ["dd", "pp"]},
                        {"W": ["pd"]},
                    ],
                )
            ],
            "(;AB[dd][pp];W[pd])",
            "(\n  ;AB[dd][pp];W[pd]\n)",
        ),
        (
            [
                (
                    [
                        {"AB": ["dd", "pp"]},
                        {"W": ["pd"]},
                    ],
                ),
                (
                    [
                        {"AW": ["dd", "pp"]},
                        {"B": ["pd"]},
                    ],
                ),
            ],
            "(;AB[dd][pp];W[pd])\n\n(;AW[dd][pp];B[pd])",
            "(\n  ;AB[dd][pp];W[pd]\n)\n\n(\n  ;AW[dd][pp];B[pd]\n)",
        ),
    ],
)
def test_print_collection(trees, expected, expected_pretty):
    collection = SGFCollection(trees)
    assert collection.sgf == expected
    assert repr(collection) == f"SGFCollection({expected})"
    assert collection.pretty() == expected_pretty
