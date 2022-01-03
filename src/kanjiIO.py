"""
:file: kanjiIO.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


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
    Determines if the given character is kanji. Note that this program considers "々" to be kanji.

    :param char: The character to be evaluated.
    :return: Boolean representing if the given character is kanji.
    """
    return (19968 <= ord(char) <= 40895) or char == '々'


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
