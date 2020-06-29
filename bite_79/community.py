import csv
from collections import Counter

import requests

CSV_URL = 'https://bites-data.s3.us-east-2.amazonaws.com/community.csv'


def get_csv():
    """Use requests to download the csv and return the
       decoded content"""
    response = requests.get(CSV_URL)
    csv_data = response.text.split('\r\n')
    cnt = Counter()
    for line in csv_data[:-1]:
        cnt[line.split(",")[2]]+= 1

    return cnt


def create_user_bar_chart(content):
    """Receives csv file (decoded) content and print a table of timezones
       and their corresponding member counts in pluses to standard output
    """
    time_zones = list(content)
    time_zones.sort()

    for tz in time_zones[:-1]:
        print(f"{tz:<20} | {'+' * content[tz]}")
