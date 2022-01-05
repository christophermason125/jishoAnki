"""
:file: parseVocabHTML.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


import requests
import urllib
import re

from bs4 import BeautifulSoup


def tag_is_not_span(tag):
    """
    Determines if the given tag is a span tag.
    :param tag: The tag to examine
    :return: If the tag is span
    """
    return tag.name != "span"


def parse_candidate(candidate):
    """
    Takes a candidate tag and parses it into the front and back Anki flashcard tag.

    :param candidate: The candidate tag
    :return: the front and back Anki flashcard tags as tuple (front, back)
    """
    # Removes the details hyperlink.
    candidate.find("a", class_="light-details_link").decompose()

    # Removes the hyperlinks beneath the entry label.
    status = candidate.div.find("div", class_="concept_light-status")

    not_labels = status.find_all(tag_is_not_span)
    for not_label in not_labels:
        not_label.decompose()

    # Removes the Read more hyperlink
    candidate.find_all()


def get_vocab_html(query, exact=True, limit=10):
    """
    Takes a vocab word and returns the stylized front and back Anki flashcard html by scraping and modifying the html
    from jisho.org/search/{vocab}.

    :param query: The query to search on jisho.org
    :param exact: Whether entries should only be included if they exactly matches the query
    :param limit: The maximum number of entries included in the card
    :return: the stylized html for the front and back of the card as the tuple (front, back)
    """
    url_vocab = urllib.parse.quote(query, safe='')
    html = requests.get(f"https://jisho.org/search/{url_vocab}").text
    soup = BeautifulSoup(html, "html.parser")

    # First I take only the column containing the entries.
    soup = soup.find("div", id="primary", class_="large-8 columns")

    # Then I get rid of the "Words" header.
    soup.find("h4").decompose()

    # If only exact matches are wanted then the other concepts should be removed.
    if exact:
        soup.find("div", class_="concepts").decompose()

    # Then I find all entry tags and remove any beyond the limit specified.
    candidates = soup.find_all("div", class_="concept_light clearfix")
    for idx, candidate in enumerate(candidates):
        if idx >= limit:
            candidate.decompose()

    # We now have all candidates.
