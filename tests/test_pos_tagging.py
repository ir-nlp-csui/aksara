import unittest
from aksara.pos_tagging import pos_tagging


class POSTaggingTest(unittest.TestCase):
    # POS Tagging Satu Kata
    # TODO

    # POS Tagging Satu Kalimat
    # TODO

    # POS Tagging Multi-Kalimat
    # TODO

    # POS Tagging File
    # TODO

    def test_pos_tagging_file(self):
        testcase = "Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton. Uang yang hilang pada tahun itu sangat banyak."
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
