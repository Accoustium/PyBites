import glob
import json
import os
from urllib.request import urlretrieve

BASE_URL = 'http://projects.bobbelderbos.com/pcc/omdb/'
MOVIES = ('bladerunner2049 fightclub glengary '
          'horrible-bosses terminator').split()
TMP = 'tmp'

# little bit of prework (yes working on pip installables ...)
for movie in MOVIES:
    fname = f'{movie}.json'
    remote = os.path.join(BASE_URL, fname)
    local = os.path.join(TMP, fname)
    urlretrieve(remote, local)

files = glob.glob(os.path.join(TMP, '*json'))


def get_movie_data(files=files):
    movies = []
    for file in files:
        data = json.load(open(file))
        movies.append(data)

    return movies


def get_single_comedy(movies):
    for movie in movies:
        if "Comedy" in movie['Genre']:
            return movie['Title']


def get_movie_most_nominations(movies):
    title = {}
    for movie in movies:
        awards = movie['Awards'].split()
        noms = int(awards[awards.index('nominations.') - 1])
        if title == {}:
            title.update({movie['Title']: noms})
        else:
            for key, value in title.items():
                if noms > value:
                    title.update({movie['Title']: noms})
                    title.pop(key)
                break

    for titl in title.keys():
        return titl


def get_movie_longest_runtime(movies):
    title = {}
    for movie in movies:
        run_time = int(movie['Runtime'].split()[0])
        if title == {}:
            title.update({movie['Title']: run_time})
        else:
            for key, value in title.items():
                if run_time > value:
                    title.update({movie['Title']: run_time})
                    title.pop(key)
                break

    for titl in title.keys():
        return titl
