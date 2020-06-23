import os
import random
import string

import pytest

from movies import MovieDb

salt = ''.join(
    random.choice(string.ascii_lowercase) for i in range(20)
)
DB = os.path.join(os.getenv("TMP", "/tmp"), f'movies_{salt}.db')
# https://www.imdb.com/list/ls055592025/
DATA = [
    ("The Godfather", 1972, 9.2),
    ("The Shawshank Redemption", 1994, 9.3),
    ("Schindler's List", 1993, 8.9),
    ("Raging Bull", 1980, 8.2),
    ("Casablanca", 1942, 8.5),
    ("Citizen Kane", 1941, 8.3),
    ("Gone with the Wind", 1939, 8.1),
    ("The Wizard of Oz", 1939, 8),
    ("One Flew Over the Cuckoo's Nest", 1975, 8.7),
    ("Lawrence of Arabia", 1962, 8.3),
]
TABLE = 'movies'


@pytest.fixture(scope='module')
def db():
    # instantiate MovieDb class using above constants
    # do proper setup / teardown using MovieDb methods
    # https://docs.pytest.org/en/latest/fixture.html (hint: yield)
    try:
        movie = MovieDb(DB, DATA, TABLE)
        movie.init()

        yield movie

        movie.drop_table()
    except Exception:
        pass

from sqlite3 import OperationalError
import sys


def test_teardown():
    err = None
    try:
        new = MovieDb(
            os.path.join(os.getenv("TMP", "/tmp"), f'movies_{salt}_1.db'),
            [('False Hangover', 2020, 0.0)],
            TABLE
        )
        new.init()
        new.drop_table()
        new.query(year=2020)
    except OperationalError:
        err = sys.exc_info()[1]

    assert str(err).split("'")[0] == "no such table: movies"


def test_godfather_is_first(db):
    assert db.query(title='The Godfather') == [(1, 'The Godfather', 1972, 9.2)]


def test_all_of_the(db):
    assert db.query(title='the') == [
        (1, 'The Godfather', 1972, 9.2),
        (2, 'The Shawshank Redemption', 1994, 9.3),
        (7, 'Gone with the Wind', 1939, 8.1),
        (8, 'The Wizard of Oz', 1939, 8.0),
        (9, "One Flew Over the Cuckoo's Nest", 1975, 8.7),
    ]


def test_search_year(db):
    assert db.query(year=1939) == [
        (7, 'Gone with the Wind', 1939, 8.1),
        (8, 'The Wizard of Oz', 1939, 8.0),
    ]


def test_score_better_than_9(db):
    assert db.query(score_gt=9) == [
        (1, "The Godfather", 1972, 9.2),
        (2, "The Shawshank Redemption", 1994, 9.3),
    ]


def test_deleting_first(db):
    db.delete(1)
    assert db.query(title='The Godfather') == []


def test_adding_godfather_again(db):
    assert db.add('The Godfather', 1972, 9.2) == 11
    assert db.query(title='The Godfather') == [(11, 'The Godfather', 1972, 9.2)]
