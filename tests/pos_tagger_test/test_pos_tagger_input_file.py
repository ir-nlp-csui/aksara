import unittest
import os

from aksara.pos_tagger import POSTagger


class PosTagTestFile(unittest.TestCase):
    """Pos Tag Test"""

    def setUp(self) -> None:
        self.pos_tagger = POSTagger()
        return super().setUp()

    def test_input_file(self):
        path = os.path.join(
            os.path.dirname(__file__), "sample_input", "testinput_postag.txt"
        )
        expected = [
            [
                ("Pengeluaran", "NOUN"),
                ("baru", "ADJ"),
                ("ini", "DET"),
                ("dipasok", "VERB"),
                ("oleh", "ADP"),
                ("rekening", "NOUN"),
                ("bank", "NOUN"),
                ("gemuk", "ADJ"),
                ("Clinton", "PROPN"),
                (".", "PUNCT"),
            ],
            [
                ("Namun", "CCONJ"),
                (",", "PUNCT"),
                ("tidak", "PART"),
                ("semua", "DET"),
                ("orang", "NOUN"),
                ("menyukai", "VERB"),
                ("itu", "DET"),
                (".", "PUNCT"),
            ],
            [
                ("Uang", "NOUN"),
                ("yang", "SCONJ"),
                ("hilang", "ADJ"),
                ("pada", "ADP"),
                ("tahun", "NOUN"),
                ("itu", "DET"),
                ("sangat", "ADV"),
                ("banyak", "DET"),
                (".", "PUNCT"),
            ],
        ]

        self.assertEqual(self.pos_tagger.tag(path, "f"), expected)

    def test_empty_file(self):
        path = os.path.join(
            os.path.dirname(__file__), "sample_input", "testinput_empty.txt"
        )

        self.assertEqual([], self.pos_tagger.tag(path, "f"))

    def test_invalid_file_should_raise_file_not_found_error(self):
        path = os.path.join(os.path.dirname(__file__), "invalid.txt")

        with self.assertRaises(FileNotFoundError):
            self.pos_tagger.tag(path, "f")
