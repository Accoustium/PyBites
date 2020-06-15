from account import Account


import pytest
import sys


TRANSACTIONS = [4, 5, 10, 43]


@pytest.fixture(scope='module')
def base_account():
    acc = Account('Tim')
    yield acc


def test_covering_bases(base_account):
    assert isinstance(base_account, Account)
    assert repr(base_account) == "Account('Tim', 0)"
    assert str(base_account) == 'Account of Tim with starting amount: 0'


@pytest.mark.xfail(raises=ValueError)
def test_does_not_add_float(base_account):
    try:
        base_account.add_transaction(0.0)
    except ValueError:
        err = sys.exc_info()
        if err[1].args[0] == 'please use int for amount':
            raise ValueError('please use int for amount')
        else:
            raise TypeError


@pytest.mark.parametrize("trans", TRANSACTIONS)
def test_adds_int_transaction(base_account, trans):
    base_account.add_transaction(trans)


def test_account_balance(base_account):
    assert base_account.balance == sum(TRANSACTIONS)


@pytest.mark.xfail(raises=AttributeError)
def test_balance_is_property(base_account):
    base_account.balance.__code__


def test_transaction_value(base_account):
    assert base_account[0] == 4
    assert base_account[3] == 43


def test_less_than(base_account):
    assert base_account < Account("Frank", 1_000_000)
    assert (base_account < Account("Frank", 62)) is False


def test_greater_than(base_account):
    assert base_account > Account("Steve", 0)
    assert (base_account < Account("Steve", 62)) is False


def test_equal(base_account):
    assert base_account == Account("Sally", sum(TRANSACTIONS))


def test_account_addition(base_account):
    value = base_account + Account("Glenn", 15)

    assert value == Account("Tim&Glenn", 77)
    assert value.owner == "Tim&Glenn"
