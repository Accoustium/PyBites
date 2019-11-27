import csv
from operator import attrgetter
from collections import defaultdict, namedtuple
import os
from urllib.request import urlretrieve

BASE_URL = 'http://projects.bobbelderbos.com/pcc/movies/'
TMP = 'tmp'

fname = 'movie_metadata.csv'
remote = os.path.join(BASE_URL, fname)
local = os.path.join(TMP, fname)
urlretrieve(remote, local)

MOVIE_DATA = local
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')


def get_movies_by_director():
    """Extracts all movies from csv and stores them in a dict,
    where keys are directors, and values are a list of movies,
    use the defined Movie namedtuple"""
    directors = defaultdict(list)
    with open(MOVIE_DATA, newline="", encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        try:
            for row in reader:
                directors[row.get('director_name')].append(
                    Movie(
                        row.get('movie_title'),
                        row.get('title_year'),
                        row.get('imdb_score')
                    )
                )
        except UnicodeDecodeError:
            print(row)

    return directors


def calc_mean_score(movies):
    """Helper method to calculate mean of list of Movie namedtuples,
       round the mean to 1 decimal place"""
    total = 0
    scores = 0
    for movie in movies:
        scores += float(movie.score)
        total += 1

    return round(scores / total, 1)


def get_average_scores(directors):
    """Iterate through the directors dict (returned by get_movies_by_director),
       return a list of tuples (director, average_score) ordered by highest
       score in descending order. Only take directors into account
       with >= MIN_MOVIES"""
    average = []
    Average = namedtuple("Average", "director score")
    for director, movies in directors.items():
        if director != '':
            if len(movies) >= MIN_MOVIES:
                average.append(Average(director, calc_mean_score(movies)))

    average = sorted(average, key=attrgetter('score'), reverse=True)
    return average
