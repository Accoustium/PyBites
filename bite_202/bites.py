import csv
from pathlib import Path
from urllib.request import urlretrieve

tmp = Path('tmp')
stats = tmp / 'bites.csv'

if not stats.exists():
    urlretrieve('https://bit.ly/2MQyqXQ', stats)


def get_most_complex_bites(N=10, stats=stats):
    """Parse the bites.csv file (= stats variable passed in), see example
       output in the Bite description.
       Return a list of Bite IDs (int or str values are fine) of the N
       most complex Bites.
    """
    import re
    from collections import Counter
    bites = Counter()

    bite = re.compile(r'^Bite (\d*)')
    reader = csv.reader(open(stats), delimiter=";")
    for first, second in reader:
        try:
            bites[
                re.search(bite, first).groups()[0]
            ] += float(second)
        except AttributeError:
            pass
        except ValueError:
            bites[
                re.search(bite, first).groups()[0]
            ] = 0

    return [x[0] for x in bites.most_common(N)]


if __name__ == '__main__':
    res = get_most_complex_bites()
    print(res)
