import unittest
import os

from aksara.utils.conllu_io import read_conllu
from aksara.conllu import ConlluData


class ConlluReaderTest(unittest.TestCase):
    """test aksara.utils.conllu_io.read_conllu method"""
    def setUp(self) -> None:
        self.empty_file_path = os.path.join(
            os.path.dirname(__file__),'sample_reader_input', 'empty_file.txt')

        self.single_conllu_path = os.path.join(
            os.path.dirname(__file__), 'sample_reader_input', 'single_conllu_data.txt')

        self.multiple_conllu_path = os.path.join(
            os.path.dirname(__file__), 'sample_reader_input', 'multiple_conllu_data.txt')

        self.custom_separator_path = os.path.join(
            os.path.dirname(__file__), 'sample_reader_input', 'custom_column_separator.txt')

        self.single_sentence_conllu = [
            [
                ConlluData(
                    '1', form='Andi', lemma='Andi',
                    upos='PROPN', xpos='_', feat='_',
                    head_id='2', deprel='nsubj'
                ),
                ConlluData(
                    '2', form='pergi', lemma='pergi',
                    upos='VERB', xpos='_', feat='_',
                    head_id='0', deprel='root'
                ),
                ConlluData(
                    '3', form='ke', lemma='ke',
                    upos='ADP', xpos='_', feat='_',
                    head_id='4', deprel='case'
                ),
                ConlluData(
                    '4', form='pasar', lemma='pasar',
                    upos='NOUN', xpos='_', feat='Number=Sing',
                    head_id='2', deprel='obl'
                )
            ]
        ]

        self.multiple_sentence_conllu = self.single_sentence_conllu + [
                [
                    ConlluData(
                        '1', form='Kemudian', lemma='kemudi',
                        upos='NOUN', xpos='_', feat='Number=Sing',
                        head_id='4', deprel='obl'
                    ),
                    ConlluData(
                        '2', form=',', lemma=',',
                        upos='PUNCT', xpos='_', feat='_',
                        head_id='4', deprel='punct'
                    ),
                    ConlluData(
                        '3', form='Budi', lemma='Budi',
                        upos='PROPN', xpos='_', feat='_',
                        head_id='4', deprel='nsubj'
                    ),
                    ConlluData(
                        '4', form='tidur', lemma='tidur',
                        upos='VERB', xpos='_', feat='_',
                        head_id='0', deprel='root'
                    )
                ]
            ]

        return super().setUp()

    def test_file_not_found(self):
        non_existent_file = 'unknown_file.txt'
        with self.assertRaises(FileNotFoundError):
            read_conllu(non_existent_file)

    def test_empty_file_should_return_empty_list(self):
        self.assertEqual([], read_conllu(self.empty_file_path))

    def test_single_conllu_data(self):

        self.assertListEqual(self.single_sentence_conllu,
                             read_conllu(self.single_conllu_path))

    def test_multiple_conllu_data(self):
        self.assertListEqual(self.multiple_sentence_conllu,
                             read_conllu(self.multiple_conllu_path))

    def test_reader_custom_separator(self):
        self.assertListEqual(
            self.single_sentence_conllu,
            read_conllu(self.custom_separator_path,
                        separator=r'\?\?')
        )
