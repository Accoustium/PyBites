from collections import defaultdict
import os
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

# prep data
holidays_page = os.path.join('tmp', 'us_holidays.php')
urlretrieve('https://bit.ly/2LG098I', holidays_page)

with open(holidays_page) as f:
    content = f.read()

holidays = defaultdict(list)


def get_us_bank_holidays(content=content):
    """Receive scraped html output, make a BS object, parse the bank
       holiday table (css class = list-table), and return a dict of
       keys -> months and values -> list of bank holidays"""


    soup = BeautifulSoup(content, "html.parser")
    table = soup.find("table", class_="list-table")

    rows = table.find_all("tr")
    headers = [x.getText().strip() for x in rows[0].find_all("th")]

    table_data = []
    for row in rows[1:]:
        table_data.append(
            [
            x.getText().strip()
            for x in row.find_all("td")
            ]
        )

    for row in table_data:
        month = ""
        holiday = ""
        for col, data in enumerate(row):
            if headers[col] == "Date":
                month = data.split("-")[1]
            if headers[col] == "Holiday":
                holiday = data
        holidays[month].append(holiday)

    return holidays