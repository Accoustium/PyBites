from collections import Counter
import os
from urllib.request import urlretrieve

from dateutil.parser import parse

commits = os.path.join('tmp', 'commits')
urlretrieve('https://bit.ly/2H1EuZQ', commits)

# you can use this constant as key to the yyyymm:count dict
YEAR_MONTH = '{y}-{m:02d}'


def get_min_max_amount_of_commits(commit_log: str = commits,
                                  year: int = None) -> (str, str):
    """
    Calculate the amount of inserts / deletes per month from the
    provided commit log.

    Takes optional year arg, if provided only look at lines for
    that year, if not, use the entire file.

    Returns a tuple of (least_active_month, most_active_month)
    """
    import re
    from datetime import datetime
    dates = Counter()

    date = re.compile(r'Date:   (.*?) \|')
    insert = re.compile(r'(\d*) insertion')
    delete = re.compile(r'(\d*) deletion')

    commit_data = open(commit_log, "r").read().split("\n")[:-1]

    for line in commit_data:
        date_time = re.search(date, line).groups()[0]
        insertion = re.search(insert, line)
        if insertion:
            insertion = insertion.groups()[0]
        else:
            insertion = 0
        deletion = re.search(delete, line)
        if deletion:
            deletion = deletion.groups()[0]
        else:
            deletion = 0
        if date_time:
            date_obj = datetime.strptime(date_time[4:-6], "%b %d %H:%M:%S %Y")
            if year:
                if year.__str__() == date_obj.strftime("%Y"):
                    dates[
                        date_obj.strftime("%Y-%m").__str__()
                    ] += int(insertion) + int(deletion)
            else:
                dates[
                    date_obj.strftime("%Y-%m").__str__()
                ] += int(insertion) + int(deletion)

    return (dates.most_common()[-1][0], dates.most_common()[0][0])
