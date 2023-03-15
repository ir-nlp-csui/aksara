import unittest
from src.aksara.lemmatization import *

class LemmatizationTest(unittest.TestCase):
    def lemmatization_one_word_test(self):
        self.assertEqual(get_lemmatization_one_word('makan'), 'VERB')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
        self.assertEqual(get_lemmatization_one_word('minum'), 'NOUN')
    
    def test_unknown_indo_word_should_return_X(self):
        self.assertEqual(get_pos_tag('eat'), 'X')
        self.assertEqual(get_pos_tag('drink'), 'X')
    
    def test_empty_string_should_return_the_same(self):
        self.assertEqual(get_pos_tag(), "")

if __name__ == '__main__':
    unittest.main()


    def lemmatization_1_kata(self):
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

