from fizzbuzz import fizzbuzz
from random import randint
import pytest


def create_fizz_buzz():
    yield 3 * randint(0, 100) * 5, "Fizz Buzz"


def create_fizz():
    num = None
    while num is None:
        num = 3 * randint(1, 100)
        if num % 5 == 0:
            num = None

    yield num, "Fizz"


def create_buzz():
    num = None
    while num is None:
        num = 5 * randint(1, 100)
        if num % 3 == 0:
            num = None

    yield num, "Buzz"


def create_no_value():
    for val in (1, 2, 4, 7, 8):
        yield val, val


@pytest.mark.parametrize("provided, expected", create_fizz_buzz())
def test_fizz_buzz(provided, expected):
    assert fizzbuzz(provided) == expected


@pytest.mark.parametrize("provided, expected", create_fizz())
def test_fizz(provided, expected):
    assert fizzbuzz(provided) == expected


@pytest.mark.parametrize("provided, expected", create_buzz())
def test_buzz(provided, expected):
    assert fizzbuzz(provided) == expected


@pytest.mark.parametrize("provided, expected", create_no_value())
def test_fizz_buzz_no_value(provided, expected):
    assert fizzbuzz(provided) == expected


@pytest.mark.xfail(raises=TypeError, reason="None Value Provided")
def test_fizz_buzz_with_none_values(provided=None, expected="Fizz Buzz"):
    assert fizzbuzz(provided) == expected


def test_fizz_buzz_with_0():
    assert fizzbuzz(0) == "Fizz Buzz"
