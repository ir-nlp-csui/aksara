import unittest
import os
from src.aksara.pos_tagging import *


class POSTaggingTest(unittest.TestCase):
    # POS Tagging Satu Kata
    # TODO

    # POS Tagging Satu Kalimat
    # TODO

    # POS Tagging Multi-Kalimat
    # TODO

    # POS Tagging File

    def test_pos_tagging_file(self):
        dirpath, _ = os.path.split(os.path.realpath(__file__))
        testcase = os.path.join(dirpath, "testinput.txt")
        expected = [
            [
                ["Pengeluaran", "NOUN"],
                ["baru", "ADJ"],
                ["ini", "DET"],
                ["dipasok", "VERB"],
                ["oleh", "ADP"],
                ["rekening", "NOUN"],
                ["bank", "NOUN"],
                ["gemuk", "ADJ"],
                ["Clinton", "PROPN"],
                [".", "PUNCT"],
            ],
            [
                ["Uang", "NOUN"],
                ["yang", "SCONJ"],
                ["hilang", "ADJ"],
                ["pada", "ADP"],
                ["tahun", "NOUN"],
                ["itu", "DET"],
                ["sangat", "ADV"],
                ["banyak", "DET"],
                [".", "PUNCT"],
            ],
        ]

        self.assertEqual(
            pos_tagging(testcase, "f"),
            expected,
        )
