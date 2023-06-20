import unittest

from aksara.utils.sentence_util import _split_sentence

class TestPreprocessText(unittest.TestCase):
    """Test preprocess function"""

    def test_empty_string_text(self):
        self.assertListEqual([], _split_sentence("   "))

    def test_remove_white_space_only_sentence(self):
        self.assertListEqual(['berjalan.'], _split_sentence('berjalan.        '))

    def test_split_multiple_sentences(self):
        self.assertListEqual(
            ['kalimat 1.', 'kalimat 2?', 'kalimat3!', 'kalimat4'],
            _split_sentence('kalimat 1. kalimat 2? kalimat3! kalimat4          ')
        )

    def test_none_regex_use_default(self):
        self.assertListEqual(
            ['kalimat 1.', 'kalimat 2.'],
            _split_sentence('kalimat 1. kalimat 2.  ', sep_regex=None)
        )
