import unittest
from collections import OrderedDict

import src.findVocab as findVocab
import src.kanjiIO as kanjiIO


TEST_WORDS = "test-io/test-words.txt"


class FindVocabTest(unittest.TestCase):
    """
    Tests findVocab.py
    """

    def test_get_vocab(self):
        """
        Tests findVocab.get_vocab
        """
        expected = OrderedDict()
        expected["Numbers"] = ['お八つ', '一', '一つ', '一つ一つ', '一二', '七', '七つ', '三', '三つ', '九', '九つ', '九九',
                               '二', '二つ', '五', '五つ', '八', '八つ', '六', '六つ', '十', '十五', '十八', '十四', '四',
                               '四つ']
        expected["Random Sentence"] = ['あくる日', 'すき焼き', '一日', '一昨日', '七七日', '三十日', '二七日', '日', '日ごろ',
                                       '日にち', '日に日に', '日ソ', '日焼け', '日食', '昨日', '焼きそば', '焼く', '焼ける',
                                       '食う', '食べる', '食パン', '１日', '１０日', '１１日', '１２日', '１３日', '１４日',
                                       '１５日', '１６日', '１８日', '１９日', '２日', '２０日', '２１日', '２２日', '２３日',
                                       '２４日', '２５日', '２６日', '２７日', '２８日', '２９日', '３日', '３０日', '３１日',
                                       '４日', '５日', '６日', '７日', '８日', '９日']
        expected["Just One"] = []

        words = kanjiIO.get_file_as_str_list(TEST_WORDS)
        known_kanji_groups = kanjiIO.get_known_kanji_groups("test-io/test-kanji-io-known-kanji-1.txt")
        result = findVocab.get_vocab(words, known_kanji_groups)
        self.assertDictEqual(expected, result)


if __name__ == '__main__':
    unittest.main()