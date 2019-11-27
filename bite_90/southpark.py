from collections import Counter, defaultdict
import csv

import requests

CSV_URL = 'https://raw.githubusercontent.com/pybites/SouthParkData/master/by-season/Season-{}.csv'  # noqa E501


def get_season_csv_file(season):
    """Receives a season int, and downloads loads in its
       corresponding CSV_URL"""
    with requests.Session() as s:
        download = s.get(CSV_URL.format(season))
        return download.content.decode('utf-8')


def get_num_words_spoken_by_character_per_episode(content):
    """Receives loaded csv content (str) and returns a dict of
       keys=characters and values=Counter object,
       which is a mapping of episode=>words spoken"""
    characters = defaultdict(Counter)
    import re
    season = re.search(r'\n{1}(\d+),', content).groups()[0]
    content = re.sub(r'(\n){1}\d+,', f'^{season},', content)
    for line in content.split("^"):
        line = line.split(",")
        if len(line) > 1:
            if line[0] != "Season":
                line[3] = ",".join(line[3:]).replace('"', '').strip()
                characters[line[2]][line[1]] += len(line[3].split())

    return characters
