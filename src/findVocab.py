"""
:file: findVocab.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""

import src.kanjiIO
from kanjiIO import *
from src.kanjiIO import get_known_kanji_groups


def get_key_from_value_elem(e, d):
    """
    Gets the first key of and ordered dictionary d that's mapped to an iterable containing the element e.

    :param e: The element
    :param d: The ordered dictionary.
    :return: The found key, or None.
    """
    for k in d:
        if e in d[k]:
            return k


def get_vocab(words_path, known_kanji_path, words_delim="\n", known_kanji_delim=":"):
    """
    Creates an ordered dictionary containing all group names found in known_kanji_path as keys. These keys are mapped
    to all words found in words_path that contain at least one kanji and only contain kanji found in their group or
    any earlier group. All words are unique both within and between groups.

    :param words_path: The path to the list of words.
    :param known_kanji_path: The path to the groups of known kanji.
    :param words_delim: The delimiter used for the words file.
    :param known_kanji_delim: The delimiter used for the known kanji file.
    :return: An ordered list of kanji groups and their vocabulary words.
    """
    words = get_file_as_str_list(words_path, words_delim)
    kanji_groups = get_known_kanji_groups(known_kanji_path, known_kanji_delim)

    vocab = OrderedDict()
    kg_keys = list(kanji_groups.keys())
    for kan in kanji_groups:
        vocab[kan] = list()

    for word in words:
        word_kanji = src.kanjiIO.get_all_kanji(word)
        rank = None

        for kan in word_kanji:
            kan_rank = get_key_from_value_elem(kan, kanji_groups)
            if kan_rank is None:
                rank = None
                break
            elif rank is None or kg_keys.index(kan_rank) > kg_keys.index(rank):
                rank = kan_rank

        if rank in vocab and get_key_from_value_elem(word, vocab) is None:
            vocab[rank].append(word)

    for kan in vocab:
        vocab[kan].sort()
    return vocab
