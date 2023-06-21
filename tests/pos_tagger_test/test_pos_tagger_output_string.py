import unittest

from aksara.pos_tagger import POSTagger

class PosTagOneSentenceTest(unittest.TestCase):
    """Test pos tagging with input one sentence"""

    def setUp(self) -> None:
        self.pos_tagger = POSTagger()
        return super().setUp()

    def test_pos_tag_satu_kalimat(self):
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
            (".", "PUNCT"),
        ]
        self.assertEqual(self.pos_tagger._tag_one_sentence(testcase), expected)

    def test_pos_tag_string_kosong(self):
        testcase = ""
        expected = []
        self.assertEqual(self.pos_tagger._tag_one_sentence(testcase), expected)

    def test_pos_tag_satu_kalimat_dengan_dua_kalimat(self):
        testcase = "Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton.\
        Pengeluaran ini bernilai sangat besar."
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
            (".", "PUNCT"),
            ("Pengeluaran", "PROPN"),
            ("ini", "DET"),
            ("bernilai", "VERB"),
            ("sangat", "ADV"),
            ("besar", "ADJ"),
            (".", "PUNCT"),
        ]
        self.assertEqual(self.pos_tagger._tag_one_sentence(testcase), expected)

    def test_pos_tag_satu_kalimat_bukan_kata_benar(self):
        testcase = "abz def ghi."
        expected = [
            ("abz", "X"),
            ("def", "X"),
            ("ghi", "X"),
            (".", "PUNCT"),
        ]
        self.assertEqual(self.pos_tagger._tag_one_sentence(testcase), expected)

    def test_pos_tag_satu_kalimat_input_angka(self):
        testcase = 123.45
        expected = [("123.45", "NUM")]
        self.assertEqual(self.pos_tagger._tag_one_sentence(testcase), expected)

    def test_pos_tag_satu_kalimat_informal_benar(self):
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
        self.assertEqual(
            self.pos_tagger._tag_one_sentence(testcase, True), expected
        )

    def test_pos_tag_satu_kalimat_informal_salah(self):
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
        self.assertEqual(
            self.pos_tagger._tag_one_sentence(testcase, False), expected
        )


class POSTagMultiSentencesTest(unittest.TestCase):
    """Test pos tagging with formal multiple sentences input"""

    def setUp(self) -> None:
        self.pos_tagger = POSTagger()
        return super().setUp()

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual(self.pos_tagger.tag(""), [])

    def test_input_single_sentence(self):
        expected = [[("aku", "PRON"), ("mau", "ADV"), ("makan", "VERB")]]
        self.assertEqual(
            self.pos_tagger.tag("aku mau makan"), expected
        )

    def test_input_multiple_sentences(self):
        expected = [
            [("Ani", "VERB"), ("membaca", "VERB"), ("buku", "NOUN"), (".", "PUNCT")],
            [
                ("Kemudian", "NOUN"),
                (",", "PUNCT"),
                ("buku", "NOUN"),
                ("itu", "DET"),
                ("terbakar", "VERB"),
                ("dengan", "ADP"),
                ("sendirinya", "_"),
                ("sendiri", "ADJ"),
                ("nya", "DET"),
            ],
        ]

        self.assertEqual(
            self.pos_tagger.tag(
                "Ani membaca buku. Kemudian, buku itu terbakar dengan sendirinya"
            ),
            expected,
        )

    def test_whitespace_after_end_of_sentences(self):
        expected = [
            [("aku", "PRON"), ("mau", "ADV"), ("makan", "VERB"), (".", "PUNCT")]
        ]

        self.assertEqual(
            self.pos_tagger.tag("aku mau makan.          "),
            expected,
        )


class POSTagMultiSentencesInformalTest(POSTagMultiSentencesTest):
    """Test pos tagging with informal multiple sentences input"""

    def setUp(self) -> None:
        self.pos_tagger = POSTagger()
        return super().setUp()

    def test_empty_string_input_informal(self):
        self.assertEqual(
            self.pos_tagger.tag("", is_informal=True), []
        )

    def test_input_single_sentence(self):
        expected = [
            [("nilai", "NOUN"), ("ujian", "NOUN"), ("gw", "PRON"), ("jelek", "ADJ")]
        ]
        self.assertEqual(
            self.pos_tagger.tag(
                "nilai ujian gw jelek", is_informal=True
            ),
            expected,
        )

    def test_input_multiple_sentences(self):
        expected = [
            [
                ("Ujiannya", "_"),
                ("Ujian", "NOUN"),
                ("nya", "PRON"),
                ("susah", "ADJ"),
                ("banget", "ADV"),
                (".", "PUNCT"),
            ],
            [
                ("Gaada", "VERB"),
                ("yang", "SCONJ"),
                ("masuk", "VERB"),
                ("yg", "PRON"),
                ("gw", "PRON"),
                ("baca", "VERB"),
            ],
        ]
        self.assertEqual(
            self.pos_tagger.tag(
                "Ujiannya susah banget. Gaada yang masuk yg gw baca", is_informal=True
            ),
            expected,
        )
