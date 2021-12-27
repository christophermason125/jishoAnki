# Range of common word pages
# https://jisho.org/search/%23common%20%23words?page=1
# https://jisho.org/search/%23common%20%23words?page=1058

import requests
import re
from kanjiIO import *


def sweep_jisho(query="%23common%20%23words", min_page=1, max_page=1058):
    entry_re = re.compile(r'(?s)(?<=<span class="text">).+?(?=</div>)')
    ascii_strip_re = re.compile(r'[\x00-\x7F]')
    entries = set()

    page_param = {"page": min_page}

    url = "https://jisho.org/search/" + query

    try:
        for pg_num in range(min_page, max_page + 1):
            page_param["page"] = pg_num
            r = requests.get(url, params=page_param)
            html = r.text
            page_entries = entry_re.findall(html)
            for e in page_entries:
                entries.add(ascii_strip_re.sub("", e))

    finally:
        return sorted(entries), pg_num


if __name__ == "__main__":
    words, pgNum = sweep_jisho(max_page=10)

    length = len(words)
    write_str_list_to_file(TEST_PATH, words)
    print(f"Swept through {pgNum} pages and wrote {length} entries to {TEST_PATH}.")
