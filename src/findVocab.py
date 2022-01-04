"""
:file: findVocab.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""
from collections import OrderedDict

import src.kanjiIO


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


def get_vocab(words, known_kanji_groups):
    """
    Creates an ordered dictionary containing all group names found in known_kanji_path as keys. These keys are mapped
    to a list of all words that contain at least one kanji and only contain kanji found in their group or
    any earlier group. All vocabulary words are unique both within and between groups.

    :param words: A list of words to search through.
    :param known_kanji_groups: An ordered dictionary of labels mapped to a list of kanji.
    :return: An ordered list of kanji groups and their vocabulary words.
    """

    vocab = OrderedDict()
    kg_keys = list(known_kanji_groups.keys())
    for kan in known_kanji_groups:
        vocab[kan] = list()

    for word in words:
        word_kanji = src.kanjiIO.get_all_kanji(word)
        rank = None

        for kan in word_kanji:
            kan_rank = get_key_from_value_elem(kan, known_kanji_groups)
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
