WORDS_PATH = "../io/Jisho Common Words.txt"
KNOWN_KANJI_PATH = "../io/Known Kanji.txt"
TEST_PATH = "../io/Test.txt"


def get_file_as_str_list(path, delim="\n"):
    with open(path, "r", encoding="utf8") as f:
        f_list = f.read().split(delim)
        f.close()
    return f_list


def write_str_list_to_file(path, str_list, delim="\n"):
    with open(path, "w", encoding="utf8") as f:
        f.write(delim.join(str_list))
        f.close()
