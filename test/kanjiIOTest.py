"""
:file: kanjiIOTest.py
:author: Christopher Mason
:email: christophermason125@gmail.com
"""


import src.kanjiIO as kanjiIO
import unittest


TEST_INPUT_PATH = "test-io/test-input.txt"
TEST_OUTPUT_PATH = "test-io/test-output.txt"


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
        result = kanjiIO.get_file_as_str_list(TEST_INPUT_PATH, delim=",")
        self.assertListEqual(result, ["1", "2", "3\n4", "5", "6\n7", "8", "9"])

    def test_write_str_list_to_file(self):
        """
        Tests kanjiIO.write_str_list_to_file
        """


if __name__ == '__main__':
    unittest.main()
