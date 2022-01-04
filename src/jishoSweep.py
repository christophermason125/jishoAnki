"""
:file: jishoSweep.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


# Range of common word pages
# https://jisho.org/search/%23common%20%23words?page=1
# https://jisho.org/search/%23common%20%23words?page=1058


import requests
import re


def sweep_jisho(query="%23common%20%23words", min_page=1, max_page=1058):
    """
    Sweeps through all results of the given query on jisho.org between the specified pages.

    :param query: The phrase to be searched on jisho.org as it would appear in a URL.
    :param min_page: The page the sweep is begun on.
    :param max_page: The page the sweep will end on.
    :raise ValueError: If min_page is greater than max_page or if the query is empty.
    :return: A sorted list of unique entries catalogued by the sweep.
    """
    if min_page > max_page:
        raise ValueError(f'Minimum page "{min_pge}" is greater than maximum page "{max_page}".')

    if len(query) == 0:
        raise ValueError("Query is blank.")

    entry_re = re.compile(r'(?s)(?<=<span class="text">).+?(?=</div>)')
    ascii_strip_re = re.compile(r'[\x00-\x7F]')
    entries = set()

    page_param = {"page": min_page}

    url = "https://jisho.org/search/" + query

    for pg_num in range(min_page, max_page + 1):
        page_param["page"] = pg_num
        r = requests.get(url, params=page_param)
        html = r.text
        page_entries = entry_re.findall(html)
        for e in page_entries:
            entries.add(ascii_strip_re.sub("", e))
    return sorted(entries)
