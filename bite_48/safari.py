import os
import urllib.request

LOG = os.path.join('tmp', 'safari.logs')
PY_BOOK, OTHER_BOOK = '🐍', '.'
urllib.request.urlretrieve('http://bit.ly/2BLsCYc', LOG)


def create_chart():
    import re

    log = open(LOG, "r").read().split("\n")
    date = re.compile(r'\d{2}-\d{2}')
    title = re.compile(r'\d{13} - (.*)')
    command = re.compile(r'- .*')

    prev_date = ""
    prev_title = ""
    lines = ""
    for line in log:
        if line == "":
            print(lines)
            break
        curr_date = re.search(date, line).group()
        if curr_date != prev_date:
            if lines != "" and "." in lines:
                print(lines)
            prev_date = curr_date
            lines = f"{curr_date} "

        try:
            prev_title = re.search(title, line).group()
        except AttributeError:
            curr_command = re.search(command, line).group()
            if "sending to slack" in curr_command:
                if "python" in prev_title.lower():
                    lines += PY_BOOK
                else:
                    lines += OTHER_BOOK
