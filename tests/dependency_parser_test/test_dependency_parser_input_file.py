import os
from unittest import TestCase
from unittest.mock import patch, Mock
import aksara.dependency_parser
from aksara.dependency_parser import _dependency_parse_input_file
from aksara.conllu import ConlluData

ONE_SENTENCE_MODULE_NAME = aksara.dependency_parser.__name__ + \
                           '._dependency_parse_one_sentence'


class DependencyParserInputFileTest(TestCase):
    """ class to test aksara.dependency_parser._dependency_parse_input_file method"""

    def setUp(self) -> None:
        self.formal_filepath = os.path.join(
            os.path.dirname(__file__), "sample_reader_input", "test_dependency.txt"
        )
        self.informal_filepath = os.path.join(
            os.path.dirname(__file__), "sample_reader_input", "test_dependency_informal.txt"
        )
        self.one_sentence_filepath = os.path.join(
            os.path.dirname(__file__), "sample_reader_input", "test_dependency_one_sentence.txt"
        )
        return super().setUp()

    @patch(target=ONE_SENTENCE_MODULE_NAME)
    def test_should_call_one_sentence_parser_method(self, mock: Mock):
        _dependency_parse_input_file(self.formal_filepath)
        self.assertTrue(mock.call_count > 0)

    @patch(target=ONE_SENTENCE_MODULE_NAME)
    def test_one_sentence_parser_called_with_correct_args(self, mock: Mock):
        _dependency_parse_input_file(self.one_sentence_filepath)

        expected_args = ('Sebuah kalimat',)
        expected_kwargs = {'is_informal': False, 'model': 'FR_GSD-ID_CSUI'}

        self.assertEqual(expected_args, mock.call_args.args)
        self.assertEqual(expected_kwargs, mock.call_args.kwargs)


# for the following tests, only model FR_GSD-ID_CSUI is used
# reason:   each model may return different result (idx, form, lemma, upos
#           xpos, feat, head_id, and deprel). The purpose of this test is to
#           verify the output is in the correct format, regardless of the
#           model used.

class DependencyParsingInputFileFormalTest(DependencyParserInputFileTest):
    """ class to test aksara.dependency_parser._dependency_parse_input_file formal method"""

    def setUp(self) -> None:
        self.first_sentence = [
            [
                ConlluData(
                    idx='1', form="Apa", lemma="apa",
                    upos="PRON", xpos="_", feat="_",
                    head_id='0', deprel="root"
                ),
                ConlluData(
                    idx='2', form="yang", lemma="yang",
                    upos="SCONJ", xpos="_", feat="_",
                    head_id='4', deprel="mark"
                ),
                ConlluData(
                    idx='3', form="kamu", lemma="kamu",
                    upos="PRON", xpos="_", feat="Number=Sing|Person=2|PronType=Prs",
                    head_id='4', deprel="nsubj"
                ),
                ConlluData(
                    idx='4', form="inginkan", lemma="ingin",
                    upos="VERB", xpos="_", feat="Voice=Act",
                    head_id='1', deprel="acl"
                ),
                ConlluData(
                    idx='5', form="?", lemma="?",
                    upos="PUNCT", xpos="_", feat="_",
                    head_id='4', deprel="punct"
                )
            ]
        ]

        self.second_sentence = [
            [
                ConlluData(
                    idx='1', form="Saya", lemma="saya",
                    upos="PRON", xpos="_", feat="Number=Sing|Person=1|PronType=Prs",
                    head_id='2', deprel="nsubj"
                ),
                ConlluData(
                    idx='2', form="ingin", lemma="ingin",
                    upos="VERB", xpos="_", feat="_",
                    head_id='0', deprel="root"
                ),
                ConlluData(
                    idx='3', form="makan", lemma="makan",
                    upos="VERB", xpos="_", feat="_",
                    head_id='2', deprel="xcomp"
                ),
                ConlluData(
                    idx='4', form=".", lemma=".",
                    upos="PUNCT", xpos="_", feat="_",
                    head_id='3', deprel="punct"
                )
            ]
        ]

        self.third_sentence = [
            [
                ConlluData(
                    idx='1', form="Saya", lemma="saya",
                    upos="PRON", xpos="_", feat="Number=Sing|Person=1|PronType=Prs",
                    head_id='2', deprel="nsubj"
                ),
                ConlluData(
                    idx='2', form="ingin", lemma="ingin",
                    upos="VERB", xpos="_", feat="_",
                    head_id='0', deprel="root"
                ),
                ConlluData(
                    idx='3', form="tidur", lemma="tidur",
                    upos="VERB", xpos="_", feat="_",
                    head_id='2', deprel="xcomp"
                ),
                ConlluData(
                    idx='4', form=".", lemma=".",
                    upos="PUNCT", xpos="_", feat="_",
                    head_id='3', deprel="punct"
                )
            ]
        ]

        return super().setUp()

    def test_input_file(self):
        expected = self.first_sentence + self.second_sentence + self.third_sentence
        result = _dependency_parse_input_file(self.formal_filepath)

        self.assertEqual(expected, result)

    def test_incorrect_filepath(self):
        filepath = os.path.join(
            os.path.dirname(__file__), "sample_reader_input", "file_doesnt_exist.txt"
        )

        with self.assertRaises(FileNotFoundError):
            _dependency_parse_input_file(filepath)


class DependencyParsingInputFileInformalTest(DependencyParserInputFileTest):
    """ class to test aksara.dependency_parser._dependency_parse_input_file informal method"""

    def setUp(self) -> None:
        self.first_sentence_conllu = [
            [
                ConlluData(
                    idx='1', form="Apa", lemma="apa",
                    upos="PRON", xpos="_", feat="_",
                    head_id='0', deprel="root"
                ),
                ConlluData(
                    idx='2', form="yg", lemma="yang",
                    upos="PRON", xpos="_", feat="Abbr=Yes|Polite=Infm|PronType=Rel",
                    head_id='1', deprel="nmod"
                ),
                ConlluData(
                    idx='3', form="lo", lemma="lo",
                    upos="PRON", xpos="_",
                    feat="Number=Sing|Person=2|Polite=Infm|PronType=Prs",
                    head_id='1', deprel="nmod"
                ),
                ConlluData(
                    idx='4', form="mau", lemma="mau",
                    upos="ADV", xpos="_", feat="_",
                    head_id='1', deprel="advmod"
                ),
                ConlluData(
                    idx='5', form="?", lemma="?",
                    upos="PUNCT", xpos="_", feat="_",
                    head_id='1', deprel="punct"
                )
            ]
        ]

        self.second_sentence_conllu = [
            [
                ConlluData(
                    idx='1', form="Gw", lemma="gw",
                    upos="PRON", xpos="_",
                    feat="Abbr=Yes|Number=Sing|Person=1|Polite=Infm|PronType=Prs",
                    head_id='0', deprel="root"
                ),
                ConlluData(
                    idx='2', form="laper", lemma="lapar",
                    upos="ADJ", xpos="_", feat="Polite=Infm",
                    head_id='1', deprel="amod"
                ),
                ConlluData(
                    idx='3', form=".", lemma=".",
                    upos="PUNCT", xpos="_", feat="_",
                    head_id='2', deprel="punct"
                )
            ]
        ]

        return super().setUp()

    def test_input_file_informal(self):
        expected = self.first_sentence_conllu + self.second_sentence_conllu
        result = _dependency_parse_input_file(self.informal_filepath, is_informal=True)

        self.assertEqual(expected, result)
