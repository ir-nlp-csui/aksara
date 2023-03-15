import unittest
from src.aksara.lemmatization import *

class LemmatizationTest(unittest.TestCase):
    def lemmatization_one_word_test(self):
        self.assertEqual(get_lemmatization_one_word('Pengeluaran'), 'keluar')
        self.assertEqual(get_lemmatization_one_word('baru'), 'baru')
        self.assertEqual(get_lemmatization_one_word('ini'), 'ini')
        self.assertEqual(get_lemmatization_one_word('dipasok'), 'pasok')
        self.assertEqual(get_lemmatization_one_word('oleh'), 'oleh')
        self.assertEqual(get_lemmatization_one_word('rekening'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('bank'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('gemuk'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('Clinton'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('.'), '.')