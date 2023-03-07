import unittest
from src.aksara.lemmatization import *

class LemmatizationTest(unittest.TestCase):
    def lemmatization_one_word_test(self):
        self.assertEqual(get_lemmatization_one_word('Pengeluaran'), 'VERB')
        self.assertEqual(get_lemmatization_one_word('baru'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('ini'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('dipasok'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('oleh'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')