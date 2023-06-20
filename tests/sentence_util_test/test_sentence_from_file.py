import unittest
import os

from aksara.utils.sentence_util import _sentences_from_file

class TestSentenceFromFile(unittest.TestCase):
    """Test _sentences_from_file function"""

    def setUp(self) -> None:
        dir_path = os.path.join(
            os.path.dirname(__file__),
            'sample_input'
        )

        self.empty_path = os.path.join(dir_path, 'empty.txt')
        self.sentences_path = os.path.join(dir_path, 'sentences.txt')
        self.ws_only_path = os.path.join(dir_path, 'whitespaceonly.txt')

        self.expected_sentences = [
            'Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton.', 
            'Namun, tidak semua orang menyukai itu.',
            'Uang yang hilang pada tahun itu sangat banyak.'
        ]
        return super().setUp()

    def test_empty_file(self):
        self.assertEqual([], _sentences_from_file(self.empty_path))

    def test_ws_only_file(self):
        self.assertEqual([], _sentences_from_file(self.ws_only_path))

    def test_file_contains_sentences(self):
        self.assertEqual(
            self.expected_sentences,
            _sentences_from_file(self.sentences_path)
        )

    def test_unknown_file(self):
        with self.assertRaises(FileNotFoundError):
            _sentences_from_file('Unknown_file.txt')
