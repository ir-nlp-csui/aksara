import unittest
import os

from aksara.morphological_analyzer import MorphologicalAnalyzer

class TestSetUp(unittest.TestCase):
    """
    Set up text test case for Morphological Analyzer output list
    """

    def setUp(self) -> None:
        self.analyzer = MorphologicalAnalyzer()

        self.one_sentence_text = 'Andi akan pergi ke lapangan.'
        self.multi_sentences = self.one_sentence_text + ' Kemudian, Ani tidur di rumah.'
        self.informal_text = 'gw mau tidur'

        self.expected_one_sentence = [
            [
                ('Andi', "Morf=Andi<PROPN>_PROPN"),
                ('akan', "Morf=akan<AUX>_AUX"),
                ('pergi', 'Morf=pergi<VERB>_VERB'),
                ('ke', 'Morf=ke<ADP>_ADP'),
                ('lapangan', 'Morf=lapang<ADJ>+an_NOUN|SpaceAfter=No'),
                ('.', 'Morf=.<PUNCT>_PUNCT')
            ]
        ]

        self.expected_multi_sentences = self.expected_one_sentence + [
            [
                ('Kemudian', 'Morf=kemudi<NOUN>+an_NOUN|SpaceAfter=No'),
                (',', 'Morf=,<PUNCT>_PUNCT'),
                ('Ani', 'Morf=Ani<PROPN>_PROPN'),
                ('tidur', 'Morf=tidur<VERB>_VERB'),
                ('di', 'Morf=di<ADP>_ADP'),
                ('rumah', 'Morf=rumah<NOUN>_NOUN|SpaceAfter=No'),
                ('.', 'Morf=.<PUNCT>_PUNCT')
            ]
        ]

        self.expected_informal = [
            [
                ('gw', 'Morf=gw<PRON>_PRON'),
                ('mau', 'Morf=mau<ADV>_ADV'),
                ('tidur', 'Morf=tidur<VERB>_VERB')
            ]
        ]

        return super().setUp()    

class TestMorphologicalAnalyzerInputStringOutputList(TestSetUp):
    """
    Test morphological analyzer with input string and output List
    """

    def unknown_input_mode(self):
        with self.assertRaises(ValueError):
            self.analyzer.analyze('text', input_mode='unknown')

    def test_empty_string_should_return_empty_list(self):
        self.assertEqual([], self.analyzer.analyze(""))

    def test_whitespace_only_input_return_empty_list(self):
        self.assertEqual([], self.analyzer.analyze('      '))

    def test_one_sentence_input(self):
        self.assertListEqual(self.expected_one_sentence, self.analyzer.analyze(self.one_sentence_text))

    def test_multi_sentence_input(self):
        self.assertListEqual(self.expected_multi_sentences, self.analyzer.analyze(self.multi_sentences))

    def test_informal_mode(self):
        self.assertListEqual(self.expected_informal, self.analyzer.analyze(self.informal_text, is_informal=True))


class TestMorphologicalAnalyzerInputFileOutputList(TestSetUp):
    """
    Test morphological analyzer with input file and output list
    """

    def setUp(self) -> None:

        sample_dir = os.path.join(os.path.dirname(__file__), 'sample_input')
        self.empty_file_path = os.path.join(
            sample_dir, 'empty_file.txt'
        )
        
        self.informal_path = os.path.join(
            sample_dir, 'informal_text.txt'
        )
        
        self.one_sentence_path = os.path.join(
            sample_dir, 'one_sentence.txt'
        )

        self.multiple_sentences_path = os.path.join(
            sample_dir, 'multiple_sentences.txt'
        )

        return super().setUp()

    def test_empty_file_should_return_empty_list(self):
        self.assertEqual(
            [], 
            self.analyzer.analyze(self.empty_file_path, input_mode='f')
        )

    def test_one_sentence_file(self):
        self.assertListEqual(
            self.expected_one_sentence,
            self.analyzer.analyze(self.one_sentence_path, input_mode='f')
        )

    def test_multiple_sentence_file(self):
        self.assertListEqual(
            self.expected_multi_sentences,
            self.analyzer.analyze(self.multiple_sentences_path, input_mode='f')
        )

    def test_informal_sentence_file(self):
        self.assertListEqual(
            self.expected_informal,
            self.analyzer.analyze(self.informal_path, input_mode='f', is_informal=True)
        )

    def test_file_input_not_exits_raise_error(self):
        with self.assertRaises(FileNotFoundError):
            self.analyzer.analyze('not_found.txt', input_mode='f')
