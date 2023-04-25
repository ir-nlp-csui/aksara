from unittest import TestCase
from unittest.mock import patch, Mock

import aksara.dependency_parser
from aksara.dependency_parser import DependencyParser
from aksara.conllu import ConlluData

MULTI_SENTENCE_MODULE_NAME = aksara.dependency_parser.__name__ + \
                             '.DependencyParser.parse'


# index 1 (mocks[1])
@patch(target=MULTI_SENTENCE_MODULE_NAME)
# index 0 (mocks[0])
@patch(target=aksara.dependency_parser.__name__ + '.write_conllu',
       side_effect=None)
class DependencyParserOutputFileTest(TestCase):
    """class to test aksara.dependency_parser.parse_to_file method"""

    def setUp(self) -> None:
        self.dependency_parser = DependencyParser()
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
                ),
                ConlluData(
                    '5', form='.', lemma='.',
                    upos='PUNCT', xpos='_', feat='_',
                    head_id='4', deprel='punct'
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
                    '3', form='tidur', lemma='tidur',
                    upos='VERB', xpos='_', feat='_',
                    head_id='0', deprel='root'
                )
            ]
        ]
        return super().setUp()

    def test_should_call_multi_sentences_parser_method(self, *mocks: Mock):
        self.dependency_parser.parse_to_file('sebuah kalimat', 'file1.txt')
        self.assertEqual(1, mocks[1].call_count)

    def test_should_call_write_conllu(self, *mocks: Mock):
        # mock main parser
        mocks[1].return_value = self.multiple_sentence_conllu
        self.dependency_parser.parse_to_file('sebuah kalimat', 'file1.txt')
        self.assertEqual(1, mocks[0].call_count)

    def test_multi_sentences_parser_called_with_correct_args(self, *mocks: Mock):
        self.dependency_parser.parse_to_file('sebuah kalimat', 'file1.txt', is_informal=True,
                                                        sep_regex=r'\?')

        expected_args = ('sebuah kalimat',)
        expected_kwargs = {'input_mode': "s", 'is_informal': True, 'sep_regex': r'\?',
                           'model': 'FR_GSD-ID_CSUI'}

        self.assertEqual(expected_args, mocks[1].call_args.args)
        self.assertEqual(expected_kwargs, mocks[1].call_args.kwargs)

    def test_write_conllu_called_with_correct_args(self, *mocks: Mock):
        mocks[1].return_value = self.multiple_sentence_conllu

        self.dependency_parser.parse_to_file('Sebuah kalimat', 'file1.txt',
                                                        write_mode='w', sep_column=r'\?\?')

        expected_args = (self.multiple_sentence_conllu, 'file1.txt',)
        expected_kwargs = {'write_mode': 'w', 'separator': r'\?\?'}

        self.assertListEqual(expected_args[0], mocks[0].call_args.args[0])
        self.assertEqual(expected_args[1], mocks[0].call_args.args[1])
        self.assertDictEqual(expected_kwargs, mocks[0].call_args.kwargs)
