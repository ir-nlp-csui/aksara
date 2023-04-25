import unittest
from src.aksara.lemmatizer import Lemmatizer


class LemmatizationTest(unittest.TestCase):
    """This class contains unit testcases for the lemmatization feature"""

    def setUp(self) -> None:
        self.lemmatizer = Lemmatizer()
        return super().setUp()

    # Sentence lemmatization
    def test_sentence_lemmatization(self):
        testcase = ["saya", "batuk"]
        expected = [("saya", "saya"), ("batuk", "batuk")]

        self.assertEqual(self.lemmatizer.lemmatize_batch(testcase), expected)

    def test_sentence_lemmatization_informal(self):
        testcase = ["lg", "udh", "ngajakin"]
        expected = [("lg", "lagi"), ("udh", "sudah"), ("ngajakin", "ajak")]

        self.assertEqual(self.lemmatizer.lemmatize_batch(testcase, True), expected)

    def test_sentence_lemmatization_informal_false(self):
        testcase = ["lg", "udh", "ngajakin"]
        expected = [("lg", "lg"), ("udh", "udh"), ("ngajakin", "ngajakin")]

        self.assertEqual(self.lemmatizer.lemmatize_batch(testcase, False), expected)

    def test_affix_sentence_lemmatization(self):
        testcase = ["airnya", "menguning"]
        expected = [
            ("airnya", "_"),
            ("air", "air"),
            ("nya", "nya"),
            ("menguning", "kuning"),
        ]

        self.assertEqual(self.lemmatizer.lemmatize_batch(testcase), expected)

    def test_empty_sentence_lemmatization(self):
        testcase = []
        expected = []

        self.assertEqual(self.lemmatizer.lemmatize_batch(testcase, True), expected)

    def test_lemmatization_empty_string(self):
        testcase = ["belajar", ""]
        expected = [("belajar", "ajar")]

        self.assertEqual(self.lemmatizer.lemmatize_batch(testcase, True), expected)

    # Word lemmatization
    def test_word_lemmatization_with_affix(self):
        testcase = "Pengeluaran"
        expected = "keluar"

        self.assertEqual(self.lemmatizer.lemmatize(testcase), expected)

    def test_word_lemmatization_without_affix(self):
        testcase = "gemuk"
        expected = "gemuk"

        self.assertEqual(self.lemmatizer.lemmatize(testcase), expected)

    def test_symbol_lemmatization(self):
        testcase = "."
        expected = "."

        self.assertEqual(self.lemmatizer.lemmatize(testcase), expected)

    def test_word_lemmatization_whitespace(self):
        testcase = ""
        expected = ""

        self.assertEqual(self.lemmatizer.lemmatize(testcase), expected)

    def test_certain_affix_word_lemmatization(self):
        testcase = "Airnya"
        expected = [("Airnya", "_"), ("Air", "air"), ("nya", "nya")]

        self.assertEqual(self.lemmatizer.lemmatize(testcase), expected)
