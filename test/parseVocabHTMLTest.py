"""
:file: parseVocabHTMLTest.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""

import unittest
import src.parseVocabHTML as parseVocabHTML

TOSHI_FRONT_PATH = "test-io/test-parse-toshi-front.html"
TOSHI_BACK_PATH = "test-io/test-parse-toshi-back.html"


class ParseVocabHTMLTest(unittest.TestCase):
    """
    Tests parseVocabHTML.py
    """

    def test_get_vocab_html(self):
        """
        Tests parseVocabHTML.get_vocab_html
        """
        toshi_front, toshi_back = parseVocabHTML.get_vocab_html("年 #common")

        with open(TOSHI_FRONT_PATH, 'r', encoding="utf8") as f:
            self.assertEqual(f.read(), toshi_front)
            f.close()
        with open(TOSHI_BACK_PATH, 'r', encoding="utf8") as f:
            self.assertEqual(f.read(), toshi_back)
            f.close()


if __name__ == '__main__':
    unittest.main()
