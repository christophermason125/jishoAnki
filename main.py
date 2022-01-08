"""
:file: main.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""

import src.kanjiIO as kanjiIO
import src.findVocab as findVocab
import src.parseVocabHTML as parseVocabHTML

WORDS_PATH = "src/io/common-words.txt"
KNOWN_KANJI_PATH = "src/io/known-kanji.txt"
EXPORT_PATH = "src/io/deck.txt"


def clean_card_field(field):
    """
    Formats the given card field to align with Anki format.
    :param field: The field to format
    :return: The formatted card field
    """
    field = field.replace('"', '""')
    field = field.replace('\n', ' ')
    field = field.replace('\t', "    ")
    return '"' + field + '"'


def main():
    """
    Takes the locations of the dictionary and known kanji files and exports a tab separated importable Anki deck
    formatted with jisho.org html entries.
    """
    while True:
        dict_path = input("Enter the path to the word dictionary.\n> ")
        if not dict_path:
            dict_path = WORDS_PATH
            print(f'Using default path "{dict_path}".')
        try:
            words = kanjiIO.get_file_as_str_list(dict_path)
            break
        except OSError:
            print("Invalid Path.")

    while True:
        known_kanji_path = input("Enter the path to the known kanji lists.\n> ")
        if not known_kanji_path:
            known_kanji_path = KNOWN_KANJI_PATH
            print(f'Using default path "{known_kanji_path}".')
        try:
            known_kanji = kanjiIO.get_known_kanji_groups(known_kanji_path)
            vocab = findVocab.get_vocab(words, known_kanji)
            break
        except OSError:
            print("Invalid Path.")

    while True:
        export_path = input("Enter the path to export the Anki deck to.\n> ")
        if not export_path:
            export_path = EXPORT_PATH
            print(f'Using default path "{export_path}".')
        try:
            open(export_path, 'a', encoding="utf8").close()
            break
        except OSError:
            print("Invalid Path.")

    with open(export_path, 'w', encoding="utf8") as file:
        for tag in vocab:
            words = vocab[tag]
            for word in words:
                try:
                    front, back = parseVocabHTML.get_vocab_html(f"{word} #common")
                    file.write(clean_card_field(front))
                    file.write('\t')
                    file.write(clean_card_field(back))
                    file.write('\t')
                    file.write(clean_card_field(tag))
                    file.write('\n')
                except ValueError:
                    file.close()
                    raise


if __name__ == "__main__":
    main()
