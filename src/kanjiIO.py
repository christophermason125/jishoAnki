"""
:file: kanjiIO.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""
from collections import OrderedDict

WORDS_PATH = "io/common-words.txt"
KNOWN_KANJI_PATH = "io/known-kanji.txt"


def get_file_as_str_list(path, delim="\n"):
    """
    Reads the given file as a list of strings, where each element is separated at the given delimiter.

    :param path: The path to the file to be read.
    :param delim: The delimiter to separate elements by.
    :return: A list of strings contained in the file.
    """
    with open(path, "r", encoding="utf8") as f:
        f_list = f.read().split(delim)
        f.close()
    return f_list


def write_str_list_to_file(path, str_list, delim="\n"):
    """
    Writes the given list to a file, placing the given delimiter between elements.

    :param path: The path to the file to be written to.
    :param str_list: A list of strings to be written.
    :param delim: The delimiter to separate elements by.
    """
    with open(path, "w", encoding="utf8") as f:
        f.write(delim.join(str_list))
        f.close()


def is_kanji(char):
    """
    Determines if the given character is kanji. For this program, kanji is defined as any unicode character part of
    the CJK Unified Ideographs (4E00-9FFF) and noma (々).


    :param char: The character to be evaluated.
    :return: Boolean representing if the given character is kanji.
    """
    return (0x4E00 <= ord(char) <= 0x9FFF) or char == '々'


def get_all_kanji(line):
    """
    Extracts all the unique kanji from the given string and sorts them into a list.

    :param line: The string containing kanji.
    :return: A sorted list of unique kanji contained in the given line.
    """
    line_kanji = set()
    for c in line:
        if is_kanji(c):
            line_kanji.add(c)
    return sorted(line_kanji)


def get_known_kanji_groups(known_kanji_path, delim=":"):
    """
    Parses the given known kanji file into an ordered dictionary with label:[kanji_one, kanji_two, ...] key:value pairs.

    :param known_kanji_path: The path to the known kanji file
    :param delim: The delimiter between the label and the list of kanji.
    :raise ValueError: If a lines does not contain the delimiter, if there are repeat/empty labels, or if there are
                       labels with no kanji.
    :return: The ordered dictionary
    """
    known_kanji_lines = get_file_as_str_list(known_kanji_path)

    kanji_groups = OrderedDict()
    for line_num, line in enumerate(known_kanji_lines):
        split_line = line.split(delim, 1)
        if len(split_line) < 2:
            raise ValueError(f'In {known_kanji_path} at line {line_num}:\n\t"{line}"\n\t'
                             f"Line does not contain delimiter '{delim}'.")

        label = split_line[0].strip()
        if label in kanji_groups:
            raise ValueError(f'In {known_kanji_path} at line {line_num}:\n\t"{line}"\n\t'
                             f'Label "{label}" already exists.')

        if len(label) == 0:
            raise ValueError(f'In {known_kanji_path} at line {line_num}:\n\t"{line}"\n\t'
                             f'Label "{label}" is blank.')

        line_kanji = get_all_kanji(split_line[1])
        if len(line_kanji) == 0:
            raise ValueError(f'In {known_kanji_path} at line {line_num}:\n"\t{line}"\n\t'
                             f'Label "{label}" contains no kanji.')

        kanji_groups[label] = line_kanji

    return kanji_groups
