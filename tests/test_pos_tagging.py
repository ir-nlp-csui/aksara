import unittest
from aksara.pos_tagging import *

# POS Tagging Satu Kata
# TODO

# POS Tagging Satu Kalimat
# TODO

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
# TODO
