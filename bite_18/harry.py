import os
from collections import Counter
import urllib.request

# data provided
stopwords_file = os.path.join('tmp', 'stopwords')
harry_text = os.path.join('tmp', 'harry')
urllib.request.urlretrieve('http://bit.ly/2EuvyHB', stopwords_file)
urllib.request.urlretrieve('http://bit.ly/2C6RzuR', harry_text)


def get_harry_most_common_word():
    with open(harry_text, "r", encoding="utf-8") as file:
        harry = file.read()

    __harry = ""
    for letter in harry:
        if letter.isalnum() or letter == " " or letter == "\n":
            if letter == "\n":
                __harry += " "
            else:
                __harry += letter

    print(__harry)

    harry = __harry.split(" ")

    with open(stopwords_file, "r", encoding="utf-8") as file:
        stop = file.read().split("\n")

    __harry = []
    for word in harry:
        if word.lower() in stop:
            pass
        else:
            __harry.append(word.lower())

    cnt = Counter(__harry)

    return cnt.most_common()[0]
