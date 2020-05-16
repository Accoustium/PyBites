import pytest
from numbers_to_dec import list_to_decimal


test_values = [
    pytest.param(
        [1, 2, 0, 10, 8, 9], 12010119, marks=pytest.mark.xfail(raises=ValueError, reason="Around Range"),
    ),
    pytest.param(
        [1, 2, 3, 10], 12310, marks=pytest.mark.xfail(raises=ValueError, reason="Above Range"),
    ),
    pytest.param(
        [-2, 5, 6, 8, 4],
        25684,
        marks=pytest.mark.xfail(raises=ValueError, reason="Under Range"),
    ),
    pytest.param(
        [1, 2, 0.0],
        120,
        marks=pytest.mark.xfail(raises=TypeError, reason="Float Value"),
    ),
    pytest.param(
        [True], 1, marks=pytest.mark.xfail(raises=TypeError, reason="Bool Value"),
    ),
    pytest.param(
        ["1", 0, 5, 4, 3, 2],
        105432,
        marks=pytest.mark.xfail(raises=TypeError, reason="String Value"),
    ),
    ([5, 2, 8, 0], 5280),
    ([4, 4, 3, 6], 4436),
    ([1, 9], 19),
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 4, 3, 5], 1234567890987654321012345435),
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 123456789)
]


@pytest.mark.parametrize("pass_test_values, expected", test_values)
def test_to_decimal_parameterized(pass_test_values, expected):
    assert list_to_decimal(pass_test_values) == expected
