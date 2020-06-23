from datetime import datetime
import json
import os
from pathlib import Path
from urllib.request import urlretrieve

import pytest

from zodiac import (get_signs, get_sign_with_most_famous_people,
                    signs_are_mutually_compatible, get_sign_by_date)

# original source: https://zodiacal.herokuapp.com/api
URL = "https://bites-data.s3.us-east-2.amazonaws.com/zodiac.json"
TMP = os.getenv("TMP", "/tmp")
PATH = Path(TMP, "zodiac.json")


@pytest.fixture(scope='module')
def signs():
    if not PATH.exists():
        urlretrieve(URL, PATH)
    with open(PATH, encoding='utf-8') as f:
        data = json.loads(f.read())
    return get_signs(data)


def test_twelve_sings(signs):
    assert len(signs) == 12


def test_get_list_of_signs(signs):
    sign = str(type(signs[0]))
    assert sign.split("'")[1] == 'zodiac.Sign'


def test_famous_signs(signs):
    famous = get_sign_with_most_famous_people(signs)
    assert famous == ('Scorpio', 35)


def test_sign_compatibility(signs):
    assert signs_are_mutually_compatible(signs, 'Aries', 'Leo')
    assert not signs_are_mutually_compatible(signs, 'Aries', 'Pisces')
    assert signs_are_mutually_compatible(signs, 'Pisces', 'Taurus')


def test_months(signs):
    taurus_date = datetime.fromisoformat('2020-05-05')
    assert get_sign_by_date(signs, taurus_date) == "Taurus"

    pisces_date = datetime.fromisoformat('2020-03-09')
    assert get_sign_by_date(signs, pisces_date) == "Pisces"

    aries_date = datetime.fromisoformat('2020-03-21')
    assert get_sign_by_date(signs, aries_date) == "Aries"

    aries_date = datetime.fromisoformat('2020-04-19')
    assert get_sign_by_date(signs, aries_date) == "Aries"
