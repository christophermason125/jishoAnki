"""
:file: kanjiIOTest.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


from collections import OrderedDict

import src.kanjiIO as kanjiIO
import unittest


TEST_INPUT_PATH = "test-io/test-kanji-io-input.txt"
TEST_OUTPUT_PATH = "test-io/test-kanji-io-output.txt"
TEST_KK_1 = "test-io/test-kanji-io-known-kanji-1.txt"
TEST_KK_2 = "test-io/test-kanji-io-known-kanji-2.txt"
TEST_KK_3 = "test-io/test-kanji-io-known-kanji-3.txt"
TEST_KK_4 = "test-io/test-kanji-io-known-kanji-4.txt"
TEST_KK_5 = "test-io/test-kanji-io-known-kanji-5.txt"
TEST_KK_6 = "test-io/test-kanji-io-known-kanji-6.txt"


class KanjiIOTest(unittest.TestCase):
    """
    Tests kanjiIO.py
    """

    def test_get_file_as_str_list(self):
        """
        Tests kanjiIO.get_file_as_str_list
        """
        result = kanjiIO.get_file_as_str_list(TEST_INPUT_PATH)
        self.assertListEqual(result, ["1,2,3", "4,5,6", "7,8,9"])
        result = kanjiIO.get_file_as_str_list(TEST_INPUT_PATH, delim=',')
        self.assertListEqual(result, ["1", "2", "3\n4", "5", "6\n7", "8", "9"])

    def test_write_str_list_to_file(self):
        """
        Tests kanjiIO.write_str_list_to_file
        """
        kanjiIO.write_str_list_to_file(TEST_OUTPUT_PATH, ["1", "2", "3"])
        with open(TEST_OUTPUT_PATH, "r") as f:
            self.assertEqual(f.read(), "1\n2\n3")
            f.close()

        kanjiIO.write_str_list_to_file(TEST_OUTPUT_PATH, ["1", "2", "3"], delim=",")
        with open(TEST_OUTPUT_PATH, "r") as f:
            self.assertEqual(f.read(), "1,2,3")
            f.close()

    def test_is_kanji(self):
        """
        Tests kanjiIO.is_kanji
        """
        self.assertFalse(kanjiIO.is_kanji('䷿'))  # 0x4DFF
        self.assertTrue(kanjiIO.is_kanji('一'))  # 0x4E00
        self.assertTrue(kanjiIO.is_kanji('丁'))  # 0x4E01

        self.assertTrue(kanjiIO.is_kanji('\u9ffe'))  # 0x9FFE
        self.assertTrue(kanjiIO.is_kanji('\u9fff'))  # 0x9FFF
        self.assertFalse(kanjiIO.is_kanji('ꀀ'))  # 0xA000

        self.assertTrue(kanjiIO.is_kanji('々'))

    def test_get_all_kanji(self):
        """
        Tests kanjiIO.get_all_kanji
        """
        self.assertListEqual(kanjiIO.get_all_kanji("Some text ䷿45丁foo一\u9fffbar\u9ffespam ꀀ egg 々"),
                             ['々', '一', '丁', '\u9ffe', '\u9fff'])
        self.assertListEqual(kanjiIO.get_all_kanji("昨日ジョンさんとすき焼きを食べました"), ['日', '昨', '焼', '食'])

    def test_get_known_kanji_groups(self):
        """
        Tests kanjiIO.get_known_kanji_groups
        """
        expected = OrderedDict()
        expected["Numbers"] = ['一', '七', '三', '九', '二', '五', '八', '六', '十', '四']
        expected["Random Sentence"] = ['日', '昨', '焼', '食']
        expected["Just One"] = ['一']
        result = kanjiIO.get_known_kanji_groups(TEST_KK_1)
        self.assertDictEqual(result, expected)

        result = kanjiIO.get_known_kanji_groups(TEST_KK_2, delim='~')
        self.assertDictEqual(result, expected)

        with self.assertRaises(ValueError):
            kanjiIO.get_known_kanji_groups(TEST_KK_3)

        with self.assertRaises(ValueError):
            kanjiIO.get_known_kanji_groups(TEST_KK_4)

        with self.assertRaises(ValueError):
            kanjiIO.get_known_kanji_groups(TEST_KK_5)

        with self.assertRaises(ValueError):
            kanjiIO.get_known_kanji_groups(TEST_KK_6)


if __name__ == '__main__':
    unittest.main()
