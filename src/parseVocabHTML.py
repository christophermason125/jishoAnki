"""
:file: parseVocabHTML.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


import requests
import urllib
import re
from copy import copy

import bs4


def prune_candidate(candidate):
    """
    Takes a candidate tag and modifies/decomposes sections in order to prepare it for the Anki card back html.

    :param candidate: The candidate tag
    """

    # Removes the hyperlinks beneath the entry labels.
    status = candidate.find("div", class_=re.compile(r"^concept_light-status"))

    # We cannot use the generator status.children because this loop removes children as it iterates.
    # This means we have to traverse the children backwards.
    for child in status.contents[::-1]:
        if isinstance(child, bs4.element.Tag) and child.name != "span":
            child.decompose()

    # Removes any other hyperlinks that don't actually redirect.
    stagnant_links = candidate.find_all("a", href="#")

    for stagnant_link in stagnant_links:
        stagnant_link.decompose()

    # Modifies the remaining hyperlinks to include the full url.
    need_https = candidate.find_all("a", href=re.compile(r"^//"))

    for short_link in need_https:
        short_link["href"] = "https:" + short_link["href"]

    need_jisho_dot_org = candidate.find_all("a", href=re.compile(r"^/search"))

    for short_link in need_jisho_dot_org:
        short_link["href"] = "https://jisho.org" + short_link["href"]


def get_vocab_html(query, exact=True, limit=10):
    """
    Takes a vocab word and returns the stylized front and back Anki flashcard html by scraping and modifying the html
    from jisho.org/search/{vocab}.

    :param query: The query to search on jisho.org
    :param exact: Whether entries should only be included if they exactly matches the query
    :param limit: The maximum number of entries included in the card
    :return: The stylized html for the front and back of the card as the tuple (front, back).
             Will return (None, None) if the limit is zero or less or the query has no results.
    """

    if limit <= 0:
        return None, None

    url_vocab = urllib.parse.quote(query, safe='')
    html = requests.get(f"https://jisho.org/search/{url_vocab}").text
    soup = bs4.BeautifulSoup(html, "html.parser")

    # First we take only the main results containing the entries.
    back_soup = soup.find("div", id="main_results")

    # We just need the primary column
    row = back_soup.find("div", class_="row")

    # Traversing backwards without generator because tags are removed mid-traversal
    for child in row.contents[::-1]:
        if isinstance(child, bs4.element.Tag) and (not child.has_attr("id") or child["id"] != "primary"):
            child.decompose()

    # Then we get rid of the "Words" header.
    back_soup.find("h4").decompose()

    # If only exact matches are wanted then the other concepts should be removed.
    if exact:
        back_soup.find("div", class_="concepts").decompose()

    # Then we find all entry tags and prune the relevant entries. We aso remove any beyond the limit specified.
    candidates = back_soup.find_all("div", class_="concept_light clearfix")

    if len(candidates) == 0:
        return None, None

    for idx, candidate in enumerate(candidates):
        if idx < limit:
            prune_candidate(candidate)
        else:
            candidate.decompose()

    # The back is finished. The front will now be pruned further.
    front_soup = copy(back_soup)

    # This is a separate tree so the candidates need to be found again
    front_candidates = front_soup.find_all(class_="concept_light clearfix")

    # We just need the first entry

    for candidate in front_candidates[1:]:
        candidate.decompose()

    # We will remove the definition. It wouldn't be a very good flashcard otherwise.
    front_soup.find("div", class_="concept_light-meanings medium-9 columns").decompose()

    # And the details link which is in a separate block
    front_soup.find("a", class_="light-details_link").decompose()

    # Now we remove the labels
    front_soup.find("div", class_=re.compile(r"^concept_light-status\b")).decompose()

    # We want to hide the readings without removing the padding, so we will delete the text instead.
    furigana = front_soup.find("span", class_="furigana")
    for span in furigana.children:
        if span.string is not None:
            span.string.replace_with("")

    # Cannot return prettified html because that adds newlines between kanji spans
    return str(front_soup), str(back_soup)
