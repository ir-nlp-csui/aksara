import unittest
import os
from unittest.mock import Mock
from src.aksara.pos_tagging import *


class TestPOSTaggingFile(unittest.TestCase):
    # mock = Mock()

    # POS Tagging File

    def test_pos_tagging_file(self):
        testcase = os.path.join(os.path.dirname(__file__), "testinput.txt")

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

        # Correct Input
        self.assertEqual(pos_tagging_file(testcase), expected)

        # Correct Input with Informal
        self.assertEqual(pos_tagging_file(testcase, True), expected)

    def test_pos_tagging_file_informal(self):
        testcase = os.path.join(os.path.dirname(__file__), "testinput_informal.txt")
        expected = [
            [
                ("Gue", "PRON"),
                ("gatau", "X"),
                ("maksud", "NOUN"),
                ("lu", "PRON"),
                ("apa", "PRON"),
                (",", "PUNCT"),
                ("tapi", "CCONJ"),
                ("kenyataannya", "_"),
                ("kenyataan", "NOUN"),
                ("nya", "PRON"),
                ("ngga", "X"),
                ("begitu", "DET"),
                (".", "PUNCT"),
            ],
            [
                ("Cuma", "NOUN"),
                ("dia", "PRON"),
                ("doang", "ADV"),
                ("yang", "SCONJ"),
                ("ga", "PART"),
                ("tau", "VERB"),
                ("itu", "DET"),
                ("apaan", "X"),
                (".", "PUNCT"),
            ],
        ]

        # Correct Informal
        self.assertEqual(pos_tagging_file(testcase, True), expected)

        # Correct Formal
        self.assertEqual(
            pos_tagging_file(testcase),
            [
                [
                    ("Gue", "PROPN"),
                    ("gatau", "X"),
                    ("maksud", "NOUN"),
                    ("lu", "X"),
                    ("apa", "PRON"),
                    (",", "PUNCT"),
                    ("tapi", "CCONJ"),
                    ("kenyataannya", "_"),
                    ("kenyataan", "NOUN"),
                    ("nya", "PRON"),
                    ("ngga", "X"),
                    ("begitu", "DET"),
                    (".", "PUNCT"),
                ],
                [
                    ("Cuma", "NOUN"),
                    ("dia", "PRON"),
                    ("doang", "X"),
                    ("yang", "SCONJ"),
                    ("ga", "X"),
                    ("tau", "VERB"),
                    ("itu", "DET"),
                    ("apaan", "X"),
                    (".", "PUNCT"),
                ],
            ],
        )

    def test_pos_tagging_file_incorrect_url(self):
        testcase = os.path.join(os.path.dirname(__file__), "file_doesnt_exist.txt")

        with self.assertRaises(FileNotFoundError):
            pos_tagging_file(testcase)
