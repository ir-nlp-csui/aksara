from unittest import TestCase
from aksara.dependency_parser import DependencyParser
from aksara.conllu import ConlluData


class DependencyParserInputTextTest(TestCase):
    """class to test aksara.dependency_parser.DependencyParser.parse from string"""

    def setUp(self) -> None:
        self.dependency_parser = DependencyParser()
        return super().setUp()


# for the following tests, only model FR_GSD-ID_CSUI is used
# reason:   each model may return different result (idx, form, lemma, upos
#           xpos, feat, head_id, and deprel). The purpose of this test is to
#           verify the output is in the correct format, regardless of the
#           model used.

class DependencyParserInputTextFormalTest(DependencyParserInputTextTest):

    def setUp(self) -> None:
        self.question_formal_conllu = [
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

        self.sentence_formal_conllu = [
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

        return super().setUp()

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual(
            self.dependency_parser.parse(''), []
        )

    def test_input_single_sentence(self):
        result = self.dependency_parser.parse("Saya ingin makan.")
        self.assertListEqual(self.sentence_formal_conllu, result)

    def test_whitespace_before_beginning_and_after_end_of_sentences(self):
        result = self.dependency_parser.parse("    Saya ingin makan.        ")
        self.assertListEqual(self.sentence_formal_conllu, result)

    def test_input_multiple_sentences(self):
        expected = self.question_formal_conllu + self.sentence_formal_conllu
        result = self.dependency_parser.parse("Apa yang kamu inginkan? Saya ingin makan.")
        self.assertListEqual(expected, result)

    def test_multiword_input(self):
        expected = [
            [
                ConlluData(idx='1-2', form='biarlah'),
                ConlluData(idx='1', form='biar', lemma='biar',
                           upos='VERB', head_id='0', deprel='root'),
                ConlluData(idx='2', form='lah', lemma='lah',
                           upos='PART', head_id='1', deprel='advmod')
            ]
        ]

        self.assertListEqual(expected, self.dependency_parser.parse("biarlah"))


class DependencyParserInputTextInformalTest(DependencyParserInputTextTest):

    def setUp(self) -> None:
        self.question_informal_conllu = [
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

        self.sentence_informal_conllu = [
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

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual(self.dependency_parser.parse('', is_informal=True), [])

    def test_input_single_sentence(self):
        result = self.dependency_parser.parse("Gw laper.", is_informal=True)
        self.assertListEqual(self.sentence_informal_conllu, result)

    def test_whitespace_before_beginning_and_after_end_of_sentences(self):
        result = self.dependency_parser.parse(
            "    Gw laper.        ", is_informal=True
        )
        self.assertListEqual(self.sentence_informal_conllu, result)

    def test_input_multiple_sentences(self):
        expected = self.question_informal_conllu + self.sentence_informal_conllu
        result = self.dependency_parser.parse(
            "Apa yg lo mau? Gw laper.", is_informal=True
        )

        self.assertListEqual(expected, result)
