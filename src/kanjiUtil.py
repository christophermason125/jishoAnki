def is_kanji(char):
    return (19968 <= ord(char) <= 40895) or char == '々'


def get_all_kanji(line):
    line_kanji = set()
    for c in line:
        if is_kanji(c):
            line_kanji.add(c)
    return sorted(line_kanji)
