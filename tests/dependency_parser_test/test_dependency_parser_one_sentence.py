from unittest import TestCase
from unittest.mock import patch, Mock
import aksara.dependency_parser
from aksara.dependency_parser import DependencyParser
from aksara.conllu import ConlluData

ANALYZE_SENTENCE_MODULE_NAME = aksara.dependency_parser.__name__ + \
                               '.analyze_sentence'


class DependencyParserOneSentenceTest(TestCase):
    """class to test aksara.dependency_parser.DependencyParser._parse_one_sentence"""

    def setUp(self) -> None:
        self.dependency_parser = DependencyParser()
        return super().setUp()

    @patch(target=ANALYZE_SENTENCE_MODULE_NAME)
    def test_should_call_analyze_sentence_method(self, mock: Mock):
        self.dependency_parser._parse_one_sentence("sebuah kalimat")
        self.assertEqual(1, mock.call_count)


# for the following tests, only model FR_GSD-ID_CSUI is used
# reason:   each model may return different result (idx, form, lemma, upos
#           xpos, feat, head_id, and deprel). The purpose of this test is to
#           verify the output is in the correct format, regardless of the
#           model used.

class DependencyParserOneSentenceFormalTest(DependencyParserOneSentenceTest):
    """Test dependency parser one sentence formal text"""

    def setUp(self) -> None:
        self.question_formal_conllu = [
            ConlluData(
                idx="1", form="Besok", lemma="besok",
                upos="NOUN", xpos="_", feat="Number=Sing",
                head_id="0", deprel="root"
            ),
            ConlluData(
                idx="2", form="apa", lemma="apa",
                upos="PRON", xpos="_", feat="_",
                head_id="5", deprel="nsubj"
            ),
            ConlluData(
                idx="3", form="yang", lemma="yang",
                upos="SCONJ", xpos="_", feat="_",
                head_id="5", deprel="mark"
            ),
            ConlluData(
                idx="4", form="akan", lemma="akan",
                upos="AUX", xpos="_", feat="_",
                head_id="5", deprel="aux"
            ),
            ConlluData(
                idx="5", form="terjadi", lemma="jadi",
                upos="VERB", xpos="_", feat="Voice=Pass",
                head_id="0", deprel="root"
            ),
            ConlluData(
                idx="6", form="?", lemma="?",
                upos="PUNCT", xpos="_", feat="_",
                head_id="5", deprel="punct"
            )
        ]

        return super().setUp()

    def test_input_single_sentence(self):
        result = self.dependency_parser._parse_one_sentence("Besok apa yang akan terjadi?")
        self.assertListEqual(self.question_formal_conllu, result)

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual([], self.dependency_parser._parse_one_sentence(""))

    def test_whitespace_before_beginning_and_after_end_of_sentence(self):
        result = self.dependency_parser._parse_one_sentence("    Besok apa yang akan terjadi?   ")
        self.assertListEqual(self.question_formal_conllu, result)

    # test typo
    def test_unknown_word_should_return_x(self):
        expected = self.question_formal_conllu.copy()
        expected[1] = ConlluData(
            idx="2", form="apa", lemma="apa",
            upos="PRON", xpos="_", feat="_",
            head_id="5", deprel="obj"
        )

        expected[2] = ConlluData(
            idx="3", form="yanjg", lemma="yanjg",
            upos="X", xpos="_", feat="Foreign=Yes",
            head_id="5", deprel="nsubj"
        )

        result = self.dependency_parser._parse_one_sentence("Besok apa yanjg akan terjadi?")

        self.assertListEqual(expected, result)

    # test invalid characters
    def test_invalid_character_should_return_sym(self):
        expected = self.question_formal_conllu.copy()
        expected[1] = ConlluData(
            idx="2", form="apa", lemma="apa",
            upos="PRON", xpos="_", feat="_",
            head_id="5", deprel="obj"
        )
        expected[2] = ConlluData(
            idx="3", form="*", lemma="*",
            upos="SYM", xpos="_", feat="_",
            head_id="5",  deprel="nsubj"
        )
        result = self.dependency_parser._parse_one_sentence("Besok apa * akan terjadi?")
        self.assertListEqual(expected, result)

    def test_multiple_sentences_should_return_one_list(self):
        expected = self.question_formal_conllu.copy()
        expected[0] = ConlluData(
            idx="1", form="Besok", lemma="besok",
            upos="NOUN", xpos="_", feat="Number=Sing",
            head_id="9", deprel="nsubj"
        )
        expected[1] = ConlluData(
            idx="2", form="apa", lemma="apa",
            upos="PRON", xpos="_", feat="_",
            head_id="5", deprel="obl"
        )
        expected[4] = ConlluData(
            idx="5", form="terjadi", lemma="jadi",
            upos="VERB", xpos="_", feat="Voice=Pass",
            head_id="1", deprel="acl"
        )
        expected[5] = ConlluData(
            idx="6", form="?", lemma="?",
            upos="PUNCT", xpos="_", feat="_",
            head_id="9", deprel="punct"
        )
        expected += [
            ConlluData(
                idx="7", form="Aku", lemma="Aku",
                upos="PROPN", xpos="_", feat="_",
                head_id="5", deprel="nsubj"
            ),
            ConlluData(
                idx="8", form="tidak", lemma="tidak",
                upos="PART", xpos="_", feat="Polarity=Neg",
                head_id="5", deprel="advmod"
            ),
            ConlluData(
                idx="9", form="tahu", lemma="tahu",
                upos="VERB", xpos="_", feat="_",
                head_id="0", deprel="root"
            ),
            ConlluData(
                idx="10", form=".", lemma=".",
                upos="PUNCT", xpos="_", feat="_",
                head_id="9", deprel="punct"
            )
        ]

        result = self.dependency_parser._parse_one_sentence(
            "Besok apa yang akan terjadi? Aku tidak tahu."
        )

        self.assertListEqual(expected, result)


class DependencyParserOneSentenceInformalTest(DependencyParserOneSentenceTest):
    """class to test aksara.dependency_parser._parse_one_sentence formal method"""

    def setUp(self) -> None:
        self.question_informal_conllu = [
            ConlluData(
                idx="1", form="Besok", lemma="besok",
                upos="NOUN", xpos="_", feat="Number=Sing",
                head_id="4", deprel="nsubj"
            ),
            ConlluData(
                idx="2", form="lu", lemma="lu",
                upos="PRON", xpos="_",
                feat="Number=Sing|Person=2|Polite=Infm|PronType=Prs",
                head_id="1", deprel="nmod"
            ),
            ConlluData(
                idx="3", form="pada", lemma="pada",
                upos="ADP", xpos="_", feat="_",
                head_id="4", deprel="mark"
            ),
            ConlluData(
                idx="4", form="ngomel", lemma="omel",
                upos="VERB", xpos="_", feat="Polite=Infm|Voice=Act",
                head_id="0", deprel="root"
            ),
            ConlluData(
                idx="5", form="lagi", lemma="lagi",
                upos="ADV", xpos="_", feat="_",
                head_id="4", deprel="advmod"
            ),
            ConlluData(
                idx="6", form="?", lemma="?",
                upos="PUNCT", xpos="_", feat="_",
                head_id="4", deprel="punct"
            )
        ]
        return super().setUp()

    def test_input_single_sentence_informal(self):
        result = self.dependency_parser._parse_one_sentence("Besok lu pada ngomel lagi?", True)
        self.assertListEqual(self.question_informal_conllu, result)

    def test_input_single_sentence_invalid(self):
        expected = [
            ConlluData(
                idx="1", form="Besok", lemma="besok",
                upos="NOUN", xpos="_", feat="Number=Sing",
                head_id="0", deprel="root"
            ),
            ConlluData(
                idx="2", form="lu", lemma="lu",
                upos="X", xpos="_", feat="Foreign=Yes",
                head_id="1", deprel="nmod"
            ),
            ConlluData(
                idx="3", form="pada", lemma="pada",
                upos="ADP", xpos="_", feat="_",
                head_id="4", deprel="case"
            ),
            ConlluData(
                idx="4", form="ngomel", lemma="ngomel",
                upos="X", xpos="_", feat="Foreign=Yes",
                head_id="1", deprel="nmod"
            ),
            ConlluData(
                idx="5", form="lagi", lemma="lagi",
                upos="ADV", xpos="_", feat="_",
                head_id="4", deprel="advmod"
            ),
            ConlluData(
                idx="6", form="?", lemma="?",
                upos="PUNCT", xpos="_", feat="_",
                head_id="1", deprel="punct"
            )
        ]

        result = self.dependency_parser._parse_one_sentence("Besok lu pada ngomel lagi?")
        self.assertListEqual(expected, result)

    def test_input_empty_string_should_return_empty_list_informal(self):
        self.assertEqual([], self.dependency_parser._parse_one_sentence("", True))

    def test_whitespace_before_beginning_and_after_end_of_sentence_informal(self):
        result = self.dependency_parser._parse_one_sentence(
            "     Besok lu pada ngomel lagi?      ", True
        )

        self.assertListEqual(self.question_informal_conllu, result)

    # test invalid characters
    def test_invalid_character_should_return_sym(self):
        expected = self.question_informal_conllu.copy()
        expected[0] = ConlluData(
            idx="1", form="Besok", lemma="besok",
            upos="NOUN", xpos="_", feat="Number=Sing",
            head_id="0", deprel="root"
        )
        expected[2] = ConlluData(
            idx="3", form="*", lemma="*",
            upos="SYM", xpos="_", feat="_",
            head_id="4", deprel="obl"
        )
        result = self.dependency_parser._parse_one_sentence("Besok lu * ngomel lagi?", True)

        self.assertListEqual(expected, result)

    def test_multiple_sentences_should_return_one_list_informal(self):
        expected = self.question_informal_conllu.copy()
        expected[5] = ConlluData(
            idx="6", form="?", lemma="?",
            upos="PUNCT", xpos="_", feat="_",
            head_id="7", deprel="punct",
        )
        expected += [
            ConlluData(
                idx="7", form="Gue", lemma="Gue",
                upos="PROPN", xpos="_", feat="_",
                head_id="0", deprel="root"
            ),
            ConlluData(
                idx="8", form="gak", lemma="enggak",
                upos="PART", xpos="_",
                feat="Abbr=Yes|Polarity=Neg|Polite=Infm",
                head_id="7", deprel="advmod"
            ),
            ConlluData(
                idx="9", form=".", lemma=".",
                upos="PUNCT", xpos="_", feat="_",
                head_id="7", deprel="punct"
            )
        ]
        result = self.dependency_parser._parse_one_sentence(
            "Besok lu pada ngomel lagi? Gue gak.", True
        )
        self.assertListEqual(expected, result)
