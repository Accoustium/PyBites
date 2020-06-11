from fizzbuzz import fizzbuzz
import pytest


def create_no_value():
    for val in (1, 2, 4, 7, 8):
        yield val, val


def test_fizz_buzz():
    assert fizzbuzz(15) == 'Fizz Buzz'


def test_fizz():
    assert fizzbuzz(3) == 'Fizz'


def test_buzz():
    assert fizzbuzz(5) == 'Buzz'


@pytest.mark.parametrize("provided, expected", create_no_value())
def test_fizz_buzz_no_value(provided, expected):
    assert fizzbuzz(provided) == expected


@pytest.mark.xfail(raises=TypeError, reason="None Value Provided")
def test_fizz_buzz_with_none_values(provided=None, expected="Fizz Buzz"):
    assert fizzbuzz(provided) == expected


def test_fizz_buzz_with_0():
    assert fizzbuzz(0) == "Fizz Buzz"
