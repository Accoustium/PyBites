from csv import DictReader
from os import path
from urllib.request import urlretrieve

DATA = path.join('tmp', 'bite_output_log.txt')
if not path.isfile(DATA):
    urlretrieve('https://bit.ly/2HoFZBd', DATA)


class BiteStats:

    def _load_data(self, data) -> list:
        row_list = []
        reader = DictReader(open(data, newline=""))
        for row in reader:
            row_list.append(row)

        return row_list

    def __init__(self, data=DATA):
        self.rows = self._load_data(data)

    def __get_unique_item(self, item):
        from collections import Counter
        items = Counter()

        for row in self.rows:
            items[row[item]] += 1

        return items

    def __get_unique_completed_item(self, item):
        from collections import Counter
        resolved = Counter()

        for row in self.rows:
            if row['completed'] == "True":
                resolved[row[item]] += 1

        return resolved

    @property
    def number_bites_accessed(self) -> int:
        """Get the number of unique Bites accessed"""
        return len(self.__get_unique_item('bite'))

    @property
    def number_bites_resolved(self) -> int:
        """Get the number of unique Bites resolved (completed=True)"""
        return len(self.__get_unique_completed_item('bite'))

    @property
    def number_users_active(self) -> int:
        """Get the number of unique users in the data set"""
        return len(self.__get_unique_item('user'))

    @property
    def number_users_solving_bites(self) -> int:
        """Get the number of unique users that resolved
           one or more Bites"""
        return len(self.__get_unique_completed_item('user'))

    @property
    def top_bite_by_number_of_clicks(self) -> str:
        """Get the Bite that got accessed the most
           (= in most rows)"""
        return self.__get_unique_item('bite').most_common()[0][0]

    @property
    def top_user_by_bites_completed(self) -> str:
        """Get the user that completed the most Bites"""
        return self.__get_unique_completed_item('user').most_common()[0][0]