import pytest

from day_01.solution import part_1, part_2


@pytest.mark.parametrize(
    "input, expected",
    [
        ("12", 2),
        ("14", 2),
        ("1969", 654),
        ("100756", 33583),
    ],
)
def test_part_1(input, expected):
    assert part_1(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ("14", 2),
        ("1969", 966),
        ("100756", 50346),
    ],
)
def test_part_2(input, expected):
    assert part_2(input) == expected
