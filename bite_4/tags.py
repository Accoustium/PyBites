import re
import os
from collections import Counter
import urllib.request

# prep
tempfile = os.path.join('tmp', 'feed')
urllib.request.urlretrieve('http://bit.ly/2zD8d8b', tempfile)

with open(tempfile) as f:
    content = f.read().lower()


# start coding

def get_pybites_top_tags(n=10):
    """use Counter to get the top 10 PyBites tags from the feed
       data already loaded into the content variable"""
    cnt = Counter()
    for tag in re.findall(r'((?<=<category>).*?(?=</category>))', content):
        cnt[tag] += 1

    return cnt.most_common(n)
