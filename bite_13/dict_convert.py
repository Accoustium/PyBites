from collections import namedtuple
from datetime import datetime
import json


blog = dict(name='PyBites',
            founders=('Julian', 'Bob'),
            started=datetime(year=2016, month=12, day=19),
            tags=['Python', 'Code Challenges', 'Learn by Doing'],
            location='Spain/Australia',
            site='https://pybit.es')

# define namedtuple here
Convert = namedtuple("Convert", "name founders started tags location site")

def dict2nt(dict_):
    return Convert(
        dict_['name'],
        dict_['founders'],
        dict_['started'],
        dict_['tags'],
        dict_['location'],
        dict_['site']
    )


def nt2json(nt):
    __dict = {
        'name': nt.name,
        'founders': nt.founders,
        'started': str(nt.started),
        'tags': nt.tags,
        'location': nt.location,
        'site': nt.site
    }
    return json.dumps(__dict)