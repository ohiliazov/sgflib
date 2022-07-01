import pytest

from sgflib import SGFCollection, SGFGameTree


@pytest.mark.parametrize(
    "trees, expected, expected_pretty",
    [
        ([SGFGameTree([{}])], "(;)", "(\n  ;\n)"),
        (
            [
                SGFGameTree(
                    [
                        {"AB": ["dd", "pp"]},
                        {"W": ["pd"]},
                    ]
                )
            ],
            "(;AB[dd][pp];W[pd])",
            "(\n  ;AB[dd][pp];W[pd]\n)",
        ),
        (
            [
                SGFGameTree(
                    [
                        {"AB": ["dd", "pp"]},
                        {"W": ["pd"]},
                    ]
                ),
                SGFGameTree(
                    [
                        {"AW": ["dd", "pp"]},
                        {"B": ["pd"]},
                    ]
                ),
            ],
            "(;AB[dd][pp];W[pd])\n\n(;AW[dd][pp];B[pd])",
            "(\n  ;AB[dd][pp];W[pd]\n)\n\n(\n  ;AW[dd][pp];B[pd]\n)",
        ),
    ],
)
def test_print_collection(trees, expected, expected_pretty):
    collection = SGFCollection(trees)
    assert str(collection) == expected
    assert repr(collection) == f"SGFCollection({expected})"
    assert collection.pretty() == expected_pretty
