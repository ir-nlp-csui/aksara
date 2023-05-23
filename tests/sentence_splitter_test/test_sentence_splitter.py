import unittest

from aksara.core import split_sentence

class TestPreprocessText(unittest.TestCase):
    """Test preprocess function"""

    def test_empty_string_text(self):
        self.assertListEqual([], split_sentence("   "))

    def test_remove_white_space_only_sentence(self):
        self.assertListEqual(['berjalan.'], split_sentence('berjalan.        '))

    def test_split_multiple_sentences(self):
        self.assertListEqual(
            ['kalimat 1.', 'kalimat 2?', 'kalimat3!', 'kalimat4'],
            split_sentence('kalimat 1. kalimat 2? kalimat3! kalimat4          ')
        )

    def test_none_regex_use_default(self):
        self.assertListEqual(
            ['kalimat 1.', 'kalimat 2.'],
            split_sentence('kalimat 1. kalimat 2.  ', sep_regex=None)
        )
