import unittest
from src.aksara.lemmatization import *

# Lemmatization List
class LemmatizationTest(unittest.TestCase):
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

    def lemmatization_one_word_test(self):
        self.assertEqual(get_lemmatization_one_word('Pengeluaran'), 'keluar')
        self.assertEqual(get_lemmatization_one_word('baru'), 'baru')
        self.assertEqual(get_lemmatization_one_word('ini'), 'ini')
        self.assertEqual(get_lemmatization_one_word('dipasok'), 'pasok')
        self.assertEqual(get_lemmatization_one_word('oleh'), 'oleh')
        self.assertEqual(get_lemmatization_one_word('rekening'), 'rekening')
        self.assertEqual(get_lemmatization_one_word('bank'), 'bank')
        self.assertEqual(get_lemmatization_one_word('gemuk'), 'gemuk')
        self.assertEqual(get_lemmatization_one_word('Clinton'), 'Clinton')
        self.assertEqual(get_lemmatization_one_word('.'), '.')
