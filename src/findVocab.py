"""
:file: findVocab.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


from collections import OrderedDict

import src.kanjiIO
from kanjiIO import *


class FormatException(Exception):
    """
    Exception thrown for an incorrectly formatted known kanji file.
    """
    def __init__(self, path, line_num, line, message):
        """
        Initializes the instance with an expression describing the location in the known kanji list where the error
        occurred. The message describes the format error at that location.

        :param path: The path to the known kanji file.
        :param line_num: The line number in the known kanji file that the error occurred at.
        :param line: The contents of the line in the known kanji file that the error occurred in.
        :param message: A description of the format error that occurred.
        """
        self.expression = f'In {path} at line {line_num}:\n"{line}".'
        self.message = message


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


def get_kanji_groups(known_kanji_path, delim=":"):
    """
    Parses the given known kanji path into an ordered dictionary with group_name:[all, kanji] key:value pairs.

    :param known_kanji_path: The path to the known kanji file
    :param delim: The delimiter between the group name and the list of kanji.
    :return: The ordered dictionary
    """
    known_kanji_lines = get_file_as_str_list(known_kanji_path)

    kanji_groups = OrderedDict()
    for line in known_kanji_lines:
        split_line = line.split(delim, 1)
        if len(split_line) < 2:
            raise FormatException(KNOWN_KANJI_PATH, known_kanji_lines.index(line), line,
                                  f'Line does not contain delimiter "{delim}".')

        label = split_line[0].strip()
        if label in kanji_groups:
            raise FormatException(KNOWN_KANJI_PATH, known_kanji_lines.index(line), line, f'Label "{label}" already '
                                                                                         f'exists.')

        if len(label) == 0:
            raise FormatException(KNOWN_KANJI_PATH, known_kanji_lines.index(line), line, f'Label "{label}" is blank.')

        line_kanji = src.kanjiIO.get_all_kanji(split_line[1])
        if len(line_kanji) == 0:
            raise FormatException(KNOWN_KANJI_PATH, known_kanji_lines.index(line), line, f'Label "{label}" contains '
                                                                                         f'no kanji.')

        kanji_groups[label] = line_kanji

    return kanji_groups


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
    kanji_groups = get_kanji_groups(known_kanji_path, known_kanji_delim)

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
