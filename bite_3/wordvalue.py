import os
import urllib.request

# PREWORK
DICTIONARY = os.path.join('tmp', 'dictionary.txt')
urllib.request.urlretrieve('http://bit.ly/2iQ3dlZ', DICTIONARY)
scrabble_scores = [(1, "E A O I N R T L S U"), (2, "D G"), (3, "B C M P"),
                   (4, "F H V W Y"), (5, "K"), (8, "J X"), (10, "Q Z")]
LETTER_SCORES = {letter: score for score, letters in scrabble_scores
                 for letter in letters.split()}


# start coding

def load_words():
    """load the words dictionary (DICTIONARY constant) into a list and return it"""
    with open(DICTIONARY, "r") as file:
        words = file.read().strip().split("\n")

    return list(words)


def calc_word_value(word):
    """given a word calculate its value using LETTER_SCORES"""
    total = 0
    for letter in word:
        try:
            total += LETTER_SCORES.get(letter.upper())
        except TypeError:
            total += 0

    return total


def max_word_value(words=None):
    """given a list of words return the word with the maximum word value"""
    __max = ""
    if len(words) == 0:
        raise (ValueError)
    try:
        for word in words:
            if calc_word_value(word) > calc_word_value(__max):
                __max = word

    except TypeError:
        raise (ValueError)

    return __max
