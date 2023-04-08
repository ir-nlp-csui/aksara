import unittest
from src.aksara.lemmatization import lemmatization_list, lemmatization_one_word

class LemmatizationTest(unittest.TestCase):
    """This class contains unit testcases for the lemmatization feature"""

    #Lemmatization list
    def test_lemmatization_list(self):
        testcase = ["saya", "batuk"]
        expected = [("saya", "saya"),
                    ("batuk", "batuk")]

        self.assertEqual(lemmatization_list(testcase), expected)

    def test_lemmatization_list_informal(self):
        testcase = ["lg", "udh", "ngajakin"]
        expected = [("lg", "lagi"),
                    ("udh", "sudah"),
                    ("ngajakin", "ajak")]

        self.assertEqual(lemmatization_list(testcase, True), expected)

    def test_lemmatization_list_informal_false(self):
        testcase = ["lg", "udh", "ngajakin"]
        expected = [("lg", "lg"),
                    ("udh", "udh"),
                    ("ngajakin", "ngajakin")]

        self.assertEqual(lemmatization_list(testcase, False), expected)

    def test_lemmatization_list_imbuhan(self):
        testcase = ["airnya", "menguning"]
        expected = [("airnya", "_"),
                    ("air", "air"),
                    ("nya", "nya"),
                    ("menguning", "kuning")]

        self.assertEqual(lemmatization_list(testcase), expected)

    def test_lemmatization_empty_list(self):
        testcase = []
        expected = []

        self.assertEqual(lemmatization_list(testcase, True), expected)

    def test_lemmatization_empty_string(self):
        testcase = ["belajar", ""]
        expected = [("belajar", "ajar")]

        self.assertEqual(lemmatization_list(testcase, True), expected)

    #Lemmatization one word
    def test_lemmatization_one_word_dengan_affix(self):
        testcase = "Pengeluaran"
        expected = "keluar"

        self.assertEqual(lemmatization_one_word(testcase), expected)

    def test_lemmatization_one_word_tanpa_affix(self):
        testcase = "gemuk"
        expected = "gemuk"

        self.assertEqual(lemmatization_one_word(testcase), expected)

    def test_lemmatization_one_word_symbol(self):
        testcase = "."
        expected = "."

        self.assertEqual(lemmatization_one_word(testcase), expected)

    def test_lemmatization_one_word_whitespace(self):
        testcase = ""
        expected = ""

        self.assertEqual(lemmatization_one_word(testcase), expected)

    def test_lemmatization_one_word_imbuhan(self):
        testcase = "Airnya"
        expected = [("Airnya", "_"), ("Air", "air"), ("nya", "nya")]

        self.assertEqual(lemmatization_one_word(testcase), expected)
