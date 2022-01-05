"""
:file: parseVocabHTMLTest.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""

import unittest
import src.parseVocabHTML as parseVocabHTML

NEKO_HTML_PATH = "test-io/test-parse-neko.html"


class ParseVocabHTMLTest(unittest.TestCase):

    def test_get_vocab_html(self):
        with open(NEKO_HTML_PATH, 'r', encoding="utf8") as file:
            expected = file.read()
            file.close()
        toru_front, toru_back = parseVocabHTML.get_vocab_html("取る #common")

        print(toru_front)
        print(toru_back)


if __name__ == '__main__':
    unittest.main()
