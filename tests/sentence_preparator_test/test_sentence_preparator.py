import unittest

from aksara.utils.sentence_preparator import _preprocess_text

class TestPreprocessText(unittest.TestCase):
    """Test preprocess function"""

    def test_empty_string_text(self):
        self.assertListEqual([], _preprocess_text("   ", ssplit=True))

    def test_remove_white_space_only_sentence(self):
        self.assertListEqual(['berjalan.'], _preprocess_text('berjalan.        '))

    def test_split_multiple_sentences(self):
        self.assertListEqual(
            ['kalimat 1.', 'kalimat 2?', 'kalimat3!', 'kalimat4'],
            _preprocess_text('kalimat 1. kalimat 2? kalimat3! kalimat4          ')
        )

    def test_no_mutli_sentences_splitting(self):
        self.assertListEqual(
            ['kalimat 1. kalimat 2.'],
            _preprocess_text('kalimat 1. kalimat 2.  ', ssplit=False)
        )
