"""
:file: jishoSweep.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


# Range of common word pages
# https://jisho.org/search/%23common%20%23words?page=1
# https://jisho.org/search/%23common%20%23words?page=1058
import urllib

import requests
from bs4 import BeautifulSoup


def is_search_entry_tag(tag):
    """
    Selector for html tags containing jisho entries. All jisho entries are in the tag <span class="txt">
    :param tag: The tag that may contain a jisho entry
    :return: True if the tag contains a jisho entry, otherwise False.
    """
    return tag.name == "span" and tag.has_attr("class") and tag["class"] == ["text"] and not tag.has_attr("id")


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
        raise ValueError(f'Minimum page "{min_page}" is greater than maximum page "{max_page}".')

    if len(query) == 0:
        raise ValueError("Query is blank.")

    entries = set()

    page_param = {"page": min_page}

    url = "https://jisho.org/search/" + urllib.parse.quote(query, safe='')

    for pg_num in range(min_page, max_page + 1):
        page_param["page"] = pg_num
        html = requests.get(url, params=page_param).text
        soup = BeautifulSoup(html, "html.parser")
        results = soup.find_all(is_search_entry_tag)
        for result in results:
            word = ""
            for chunk in result.stripped_strings:
                word += chunk
            entries.add(word)

    return sorted(entries)
