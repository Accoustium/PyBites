from unittest.mock import patch

import pytest

from guess import GuessGame, InvalidNumber


# write test code to reach 100% coverage and a 100% mutpy score
import sys
import io


def test_number_passed_in():
    try:
        GuessGame('h')
    except InvalidNumber:
        err_val = sys.exc_info()

    assert str(err_val[1]).split('"')[0] == 'Not a number'


def test_negative_number():
    try:
        GuessGame(-1)
    except InvalidNumber:
        err_val = sys.exc_info()

    assert str(err_val[1]).split('"')[0] == 'Negative number'


def test_accept_0_number():
    GuessGame(0)
    assert True


def test_accept_15_max():
    GuessGame(15)
    assert True


def test_max_number_15():
    try:
        GuessGame(16)
    except InvalidNumber:
        err_val = sys.exc_info()

    assert str(err_val[1]).split('"')[0] == 'Number too high'


def test_correct_number_game(capsys, monkeypatch):
    guess_ = GuessGame(5)
    monkeypatch.setattr('sys.stdin', io.StringIO('5\n'))
    guess_()
    capture = capsys.readouterr()
    assert capture.out.split('\n')[0] == 'Guess a number: '
    assert capture.out.split('\n')[1] == "You guessed it!"


def test_number_too_low(capsys, monkeypatch):
    guess_ = GuessGame(5)
    monkeypatch.setattr('sys.stdin', io.StringIO('4\n'))
    try:
        guess_()
    except EOFError:
        capture = capsys.readouterr()

    assert capture.out.split('\n')[1] == "Too low"


def test_number_too_high(capsys, monkeypatch):
    guess_ = GuessGame(5)
    monkeypatch.setattr('sys.stdin', io.StringIO('6\n'))
    try:
        guess_()
    except EOFError:
        capture = capsys.readouterr()

    assert capture.out.split('\n')[1] == "Too high"


def test_non_number_input(capsys, monkeypatch):
    guess_ = GuessGame(5)
    monkeypatch.setattr('sys.stdin', io.StringIO('h\n'))
    try:
        guess_()
    except EOFError:
        capture = capsys.readouterr()

    assert capture.out.split('\n')[1] == "Enter a number, try again"


def test_max_number_tries_default(capsys, monkeypatch):
    guess_ = GuessGame(10)

    monkeypatch.setattr('sys.stdin', io.StringIO('1\n1\n1\n1\n1\n'))
    guess_()

    capture = capsys.readouterr()
    assert len(capture.out.split('\n')) == 12
    assert capture.out.split('\n')[-2] == 'Sorry, the number was 10'
