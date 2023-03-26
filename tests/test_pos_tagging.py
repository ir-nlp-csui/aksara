import unittest

from src.aksara.pos_tagging import *


# # POS Tagging Satu Kata
# # TODO

# POS Tagging Satu Kalimat

class PosTagOneSentenceTest(unittest.TestCase):
    def test_pos_tagging_satu_kalimat(self):
        testcase = "Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton."
        expected = [
            ("Pengeluaran", "NOUN"),
            ("baru", "ADJ"),
            ("ini", "DET"),
            ("dipasok", "VERB"),
            ("oleh", "ADP"),
            ("rekening", "NOUN"),
            ("bank", "NOUN"),
            ("gemuk", "ADJ"),
            ("Clinton", "PROPN"),
            (".", "PUNCT")
        ]
        self.assertEqual(pos_tagging_one_sentence(testcase), expected)

    def test_pos_tagging_string_kosong(self):
        testcase = ""
        expected = []
        self.assertEqual(pos_tagging_one_sentence(testcase), expected)

    def test_pos_tagging_satu_kalimat_dengan_dua_kalimat(self):
        testcase = "Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton.\
        Pengeluaran ini bernilai sangat besar."
        expected = [
            ('Pengeluaran', 'NOUN'),
            ('baru', 'ADJ'),
            ('ini', 'DET'),
            ('dipasok', 'VERB'),
            ('oleh', 'ADP'),
            ('rekening', 'NOUN'),
            ('bank', 'NOUN'),
            ('gemuk', 'ADJ'),
            ('Clinton', 'PROPN'),
            ('.', 'PUNCT'),
            ('Pengeluaran', 'PROPN'),
            ('ini', 'DET'),
            ('bernilai', 'VERB'),
            ('sangat', 'ADV'),
            ('besar', 'ADJ'),
            ('.', 'PUNCT'),
        ]
        self.assertEqual(pos_tagging_one_sentence(testcase), expected)

    def test_pos_tagging_satu_kalimat_bukan_kata_benar(self):
        testcase = "abz def ghi."
        expected = [
            ("abz", "X"),
            ("def", "X"),
            ("ghi", "X"),
            (".", "PUNCT"),
        ]
        self.assertEqual(pos_tagging_one_sentence(testcase), expected)

    def test_pos_tagging_satu_kalimat_input_angka(self):
        testcase = 123.45
        expected = [("123.45", "NUM")]
        self.assertEqual(pos_tagging_one_sentence(testcase), expected)

    def test_pos_tagging_satu_kalimat_informal_benar(self):
        testcase = "Sering ngikutin gayanya lg nyanyi."
        expected = [
            ("Sering", "ADV"),
            ("ngikutin", "VERB"),
            ("gayanya", "_"),
            ("gaya", "NOUN"),
            ("nya", "PRON"),
            ("lg", "ADV"),
            ("nyanyi", "VERB"),
            (".", "PUNCT"),
        ]
        self.assertEqual(pos_tagging_one_sentence(testcase, True), expected)

    def test_pos_tagging_satu_kalimat_informal_salah(self):
        testcase = "Sering ngikutin gayanya lg nyanyi."
        expected = [
            ("Sering", "ADV"),
            ("ngikutin", "X"),
            ("gayanya", "_"),
            ("gaya", "NOUN"),
            ("nya", "PRON"),
            ("lg", "X"),
            ("nyanyi", "VERB"),
            (".", "PUNCT"),
        ]
        self.assertEqual(pos_tagging_one_sentence(testcase, False), expected)


# POS Tagging Multi-Kalimat
class POSTagMultiSentencesTest(unittest.TestCase):

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual(tag_multi_sentences(''), [])

    def test_input_single_sentence(self):
        expected = [
            [
                ('aku', 'PRON'),
                ('mau', 'ADV'),
                ('makan', 'VERB')
            ]
        ]
        self.assertEqual(tag_multi_sentences('aku mau makan'), expected)

    def test_input_multiple_sentences(self):
        expected = [
            [
                ('Ani', 'VERB'),
                ('membaca', 'VERB'),
                ('buku', 'NOUN'),
                ('.', 'PUNCT')
            ],
            [
                ('Kemudian', 'NOUN'),
                (',', 'PUNCT'),
                ('buku', 'NOUN'),
                ('itu', 'DET'),
                ('terbakar', 'VERB'),
                ('dengan', 'ADP'),
                ('sendirinya', '_'),
                ('sendiri', 'ADJ'),
                ('nya', 'DET')
            ]
        ]

        self.assertEqual(tag_multi_sentences('Ani membaca buku. Kemudian, buku itu terbakar dengan sendirinya'),
                         expected)

    def test_whitespace_after_end_of_sentences(self):
        expected = [
            [
                ('aku', 'PRON'),
                ('mau', 'ADV'),
                ('makan', 'VERB'),
                ('.', 'PUNCT')
            ]
        ]

        self.assertEqual(tag_multi_sentences('aku mau makan.          '), expected)


class POSTagMultiSentencesInformalTest(POSTagMultiSentencesTest):

    def test_empty_string_input_informal(self):
        self.assertEqual(tag_multi_sentences('', is_informal=True), [])

    def test_input_single_sentence(self):
        expected = [
            [
                ('nilai', 'NOUN'),
                ('ujian', 'NOUN'),
                ('gw', 'PRON'),
                ('jelek', 'ADJ')
            ]
        ]
        self.assertEqual(tag_multi_sentences('nilai ujian gw jelek', is_informal=True), expected)

    def test_input_multiple_sentences(self):
        expected = [
            [
                ('Ujiannya', '_'),
                ('Ujian', 'NOUN'),
                ('nya', 'PRON'),
                ('susah', 'ADJ'),
                ('banget', 'ADV'),
                ('.', 'PUNCT')
            ],
            [
                ('Gaada', 'PROPN'),
                ('yang', 'SCONJ'),
                ('masuk', 'VERB'),
                ('yg', 'PRON'),
                ('gw', 'PRON'),
                ('baca', 'VERB')
            ]
        ]
        self.assertEqual(tag_multi_sentences("Ujiannya susah banget. Gaada yang masuk yg gw baca", is_informal=True),
                         expected)


# POS Tagging File
class TestPOSTaggingFile(unittest.TestCase):

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
                ("Saya", "PRON"),
                ("pun", "PART"),
                ("tidak", "PART"),
                ("setuju", "VERB"),
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
