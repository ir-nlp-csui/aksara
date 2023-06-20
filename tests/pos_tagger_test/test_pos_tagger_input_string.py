import unittest

from aksara.pos_tagger import POSTagger


class PosTagTestString(unittest.TestCase):
    """Pos Tag Test"""

    def setUp(self) -> None:
        self.pos_tagger = POSTagger()
        return super().setUp()

    def test_input_string(self):
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
        ]

        self.assertEqual(
            self.pos_tagger.tag(
                "Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton." +
                " Namun, tidak semua orang menyukai itu."
            ),
            expected,
        )

    def test_incorrect_input_string(self):
        expected = [
            [
                ("Pengeluaran", "NOUN"),
                ("baru", "ADJ"),
                ("ini", "DET"),
                ("dikepresek", "X"),
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
        ]

        self.assertEqual(
            self.pos_tagger.tag(
                "Pengeluaran baru ini dikepresek oleh rekening bank gemuk Clinton." +
                " Namun, tidak semua orang menyukai itu."
            ),
            expected,
        )

    def test_empty_string_should_return_empty_list(self):
        self.assertEqual(self.pos_tagger.tag(""), [])

    def test_input_not_string_should_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.pos_tagger.tag(["Uang"])

    def test_input_file_when_should_be_string_should_raise_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            self.pos_tagger.tag("Uang", "f")

    def test_incorrect_input_type_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.pos_tagger.tag("Uang", "S")


class PosTagTestStringInformal(unittest.TestCase):
    """Pos Tag Test"""

    def setUp(self) -> None:
        self.pos_tagger = POSTagger()
        return super().setUp()

    def test_informal_input_string(self):
        expected = [
            [
                ("Gue", "PRON"),
                ("gak", "PART"),
                ("tau", "VERB"),
                ("maksud", "NOUN"),
                ("lu", "PRON"),
                ("apa", "PRON"),
                (".", "PUNCT"),
            ],
            [
                ("Kenyataannya", "_"),
                ("Kenyataan", "NOUN"),
                ("nya", "PRON"),
                ("gak", "PART"),
                ("begitu", "DET"),
                (".", "PUNCT"),
            ],
        ]

        self.assertEqual(
            self.pos_tagger.tag(
                "Gue gak tau maksud lu apa. Kenyataannya gak begitu.", is_informal=True
            ),
            expected,
        )

    def test_informal_empty_string_should_return_empty_list(self):
        self.assertEqual(self.pos_tagger.tag("", is_informal=True), [])

    def test_informal_input_not_string_should_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.pos_tagger.tag(["duit"], is_informal=True)

    def test_informal_input_file_when_should_be_string_should_raise_file_not_found_error(
        self,
    ):
        with self.assertRaises(FileNotFoundError):
            self.pos_tagger.tag("duit", "f", True)

    def test_informal_incorrect_input_type_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.pos_tagger.tag("duit", "S", True)
