import unittest
import os

from aksara.utils.sentence_util import _get_sentence_list

class TestGetSentenceList(unittest.TestCase):
    """Test _get_sentence_list function"""

    def test_unknown_input_mode(self):
        with self.assertRaises(ValueError):
            _get_sentence_list('abc', input_mode='unknown')

    def test_input_is_str(self):
        self.assertEqual(['abc.', 'def'], _get_sentence_list('abc. def'))

    def test_input_is_file(self):
        file_path = os.path.join(
            os.path.dirname(__file__),
            'sample_input',
            'empty.txt'
        )

        self.assertEqual([], _get_sentence_list(file_path, input_mode='f'))
