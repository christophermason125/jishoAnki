from collections import OrderedDict
from kanjiIO import *
import kanjiUtil


class FormatException(Exception):
    def __init__(self, path, line_num, line, message):
        self.expression = f'In {path} at line {line_num}:\n"{line}".'
        self.message = message


def get_key_from_value_elem(v, d):
    for k in d:
        if v in d[k]:
            return k
    return None


def get_kanji_groups(path):
    known_kanji_lines = get_file_as_str_list(KNOWN_KANJI_PATH)

    kanji_groups = OrderedDict()
    delim = ":"
    for line in known_kanji_lines:
        split_line = line.split(delim, 1)
        if len(split_line) < 2:
            raise FormatException(KNOWN_KANJI_PATH, known_kanji_lines.index(line), line,
                                  f'Line does not contain deliminer "{delim}".')

        label = split_line[0].strip()
        if label in kanji_groups:
            raise FormatException(KNOWN_KANJI_PATH, known_kanji_lines.index(line), line, f'Label "{label}" already '
                                                                                         f'exists.')

        if len(label) == 0:
            raise FormatException(KNOWN_KANJI_PATH, known_kanji_lines.index(line), line, f'Label "{label}" is blank.')

        line_kanji = kanjiUtil.get_all_kanji(split_line[1])
        if len(line_kanji) == 0:
            raise FormatException(KNOWN_KANJI_PATH, known_kanji_lines.index(line), line, f'Label "{label}" contains '
                                                                                         f'no kanji.')

        kanji_groups[label] = line_kanji

    return kanji_groups


def get_vocab(words_path, known_kanji_path):
    words = get_file_as_str_list(words_path)
    kanji_groups = get_kanji_groups(known_kanji_path)

    vocab = OrderedDict()
    kg_keys = list(kanji_groups.keys())
    for kan in kanji_groups:
        vocab[kan] = list()

    for word in words:
        word_kanji = kanjiUtil.get_all_kanji(word)
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


if __name__ == "__main__":
    vocab = get_vocab(WORDS_PATH, KNOWN_KANJI_PATH)
    for k in vocab:
        count = len(vocab[k])
        print(f"Discovered {count} kanji in group {k}.")
        for v in vocab[k]:
            print("\t" + v)
