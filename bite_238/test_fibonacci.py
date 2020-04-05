from fibonacci import fib
import pytest

# write one or more pytest functions below, they need to start with test_
def test_fibonacci_positive():
    assert fib(6) == 8

def test_fibonacci_one_or_zero():
    assert fib(0) == 0
    assert fib(1) == 1

@pytest.mark.xfail(raises=ValueError)
def test_fibonacci_negative():
    fib(-1)
