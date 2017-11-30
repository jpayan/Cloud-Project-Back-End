import re

_words = None


def get_words():
    global _words
    if not _words:
        load_words()


def contains_profanity(input_text):
    global _words
    get_words()
    curse_word = None
    for word in _words:
        curse_word = re.compile(r'(?<![a-zA-Z0-9])' + re.escape(word) + r'(?![a-zA-Z0-9])', re.IGNORECASE)
        if curse_word.search(input_text):
            break
    return True if curse_word.search(input_text) else False


def load_words(word_list=None):
    global _words
    if not word_list:
        filename = 'word_list.txt'
        f = open(filename)
        word_list = f.readlines()
        word_list = [w.strip() for w in word_list if w]
    _words = word_list
