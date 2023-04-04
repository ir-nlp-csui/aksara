import unittest
from aksara.dependency_parsing_1_kalimat import *
from aksara.conllu import ConlluData


class DependencyParsingOneSentenceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.Besok = ConlluData(
            idx="1",
            form="Besok",
            lemma="besok",
            upos="NOUN",
            xpos="_",
            feat="Number=Sing",
            head_id="0",
            deprel="root",
        )
        self.apa = ConlluData(
            idx="2",
            form="apa",
            lemma="apa",
            upos="PRON",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="nsubj",
        )
        self.yang = ConlluData(
            idx="3",
            form="yang",
            lemma="yang",
            upos="SCONJ",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="mark",
        )
        self.akan = ConlluData(
            idx="4",
            form="akan",
            lemma="akan",
            upos="AUX",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="aux",
        )
        self.terjadi = ConlluData(
            idx="5",
            form="terjadi",
            lemma="jadi",
            upos="VERB",
            xpos="_",
            feat="Voice=Pass",
            head_id="0",
            deprel="root",
        )
        self.question_mark = ConlluData(
            idx="6",
            form="?",
            lemma="?",
            upos="PUNCT",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="punct",
        )
        self.yanjg = ConlluData(
            idx="3",
            form="yanjg",
            lemma="yanjg",
            upos="X",
            xpos="_",
            feat="Foreign=Yes",
            head_id="5",
            deprel="nsubj",
        )
        self.star = ConlluData(
            idx="3",
            form="*",
            lemma="*",
            upos="SYM",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="nsubj",
        )
        self.Aku = ConlluData(
            idx="7",
            form="Aku",
            lemma="Aku",
            upos="PROPN",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="nsubj",
        )
        self.tidak = ConlluData(
            idx="8",
            form="tidak",
            lemma="tidak",
            upos="PART",
            xpos="_",
            feat="Polarity=Neg",
            head_id="5",
            deprel="advmod",
        )
        self.tahu = ConlluData(
            idx="9",
            form="tahu",
            lemma="tahu",
            upos="VERB",
            xpos="_",
            feat="_",
            head_id="0",
            deprel="root",
        )
        self.dot = ConlluData(
            idx="10",
            form=".",
            lemma=".",
            upos="PUNCT",
            xpos="_",
            feat="_",
            head_id="9",
            deprel="punct",
        )

    def test_input_single_sentence(self):
        expected = [
            self.Besok,
            self.apa,
            self.yang,
            self.akan,
            self.terjadi,
            self.question_mark,
        ]
        result = dependency_parsing_one_sentence("Besok apa yang akan terjadi?")

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual(dependency_parsing_one_sentence(""), [])

    def test_whitespace_before_beginning_and_after_end_of_sentence(self):
        expected = [
            self.Besok,
            self.apa,
            self.yang,
            self.akan,
            self.terjadi,
            self.question_mark,
        ]
        result = dependency_parsing_one_sentence("    Besok apa yang akan terjadi?   ")

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))

    # test typo
    def test_unknown_word_should_return_X(self):
        self.apa = ConlluData(
            idx="2",
            form="apa",
            lemma="apa",
            upos="PRON",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="obj",
        )
        expected = [
            self.Besok,
            self.apa,
            self.yanjg,
            self.akan,
            self.terjadi,
            self.question_mark,
        ]
        result = dependency_parsing_one_sentence("Besok apa yanjg akan terjadi?")

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))

    # test invalid characters
    def test_invalid_character_should_return_SYM(self):
        self.apa = ConlluData(
            idx="2",
            form="apa",
            lemma="apa",
            upos="PRON",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="obj",
        )
        expected = [
            self.Besok,
            self.apa,
            self.star,
            self.akan,
            self.terjadi,
            self.question_mark,
        ]
        result = dependency_parsing_one_sentence("Besok apa * akan terjadi?")

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))

    def test_multiple_sentences_should_return_one_list(self):
        self.Besok = ConlluData(
            idx="1",
            form="Besok",
            lemma="besok",
            upos="NOUN",
            xpos="_",
            feat="Number=Sing",
            head_id="9",
            deprel="nsubj",
        )
        self.apa = ConlluData(
            idx="2",
            form="apa",
            lemma="apa",
            upos="PRON",
            xpos="_",
            feat="_",
            head_id="5",
            deprel="obl",
        )
        self.terjadi = ConlluData(
            idx="5",
            form="terjadi",
            lemma="jadi",
            upos="VERB",
            xpos="_",
            feat="Voice=Pass",
            head_id="1",
            deprel="acl",
        )
        self.question_mark = ConlluData(
            idx="6",
            form="?",
            lemma="?",
            upos="PUNCT",
            xpos="_",
            feat="_",
            head_id="9",
            deprel="punct",
        )
        expected = [
            self.Besok,
            self.apa,
            self.yang,
            self.akan,
            self.terjadi,
            self.question_mark,
            self.Aku,
            self.tidak,
            self.tahu,
            self.dot,
        ]

        result = dependency_parsing_one_sentence(
            "Besok apa yang akan terjadi? Aku tidak tahu."
        )

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))


class DependencyParsingOneSentenceInformalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.Besok = ConlluData(
            idx="1",
            form="Besok",
            lemma="besok",
            upos="NOUN",
            xpos="_",
            feat="Number=Sing",
            head_id="4",
            deprel="nsubj",
        )
        self.lu = ConlluData(
            idx="2",
            form="lu",
            lemma="lu",
            upos="PRON",
            xpos="_",
            feat="Number=Sing|Person=2|Polite=Infm|PronType=Prs",
            head_id="1",
            deprel="nmod",
        )
        self.pada = ConlluData(
            idx="3",
            form="pada",
            lemma="pada",
            upos="ADP",
            xpos="_",
            feat="_",
            head_id="4",
            deprel="mark",
        )
        self.ngomel = ConlluData(
            idx="4",
            form="ngomel",
            lemma="omel",
            upos="VERB",
            xpos="_",
            feat="Polite=Infm|Voice=Act",
            head_id="0",
            deprel="root",
        )
        self.lagi = ConlluData(
            idx="5",
            form="lagi",
            lemma="lagi",
            upos="ADV",
            xpos="_",
            feat="_",
            head_id="4",
            deprel="advmod",
        )
        self.question_mark = ConlluData(
            idx="6",
            form="?",
            lemma="?",
            upos="PUNCT",
            xpos="_",
            feat="_",
            head_id="4",
            deprel="punct",
        )
        self.star = ConlluData(
            idx="3",
            form="*",
            lemma="*",
            upos="SYM",
            xpos="_",
            feat="_",
            head_id="4",
            deprel="obl",
        )
        self.Gue = ConlluData(
            idx="7",
            form="Gue",
            lemma="Gue",
            upos="PROPN",
            xpos="_",
            feat="_",
            head_id="0",
            deprel="root",
        )
        self.gak = ConlluData(
            idx="8",
            form="gak",
            lemma="enggak",
            upos="PART",
            xpos="_",
            feat="Abbr=Yes|Polarity=Neg|Polite=Infm",
            head_id="7",
            deprel="advmod",
        )
        self.dot = ConlluData(
            idx="9",
            form=".",
            lemma=".",
            upos="PUNCT",
            xpos="_",
            feat="_",
            head_id="7",
            deprel="punct",
        )

    def test_input_single_sentence_informal(self):
        expected = [
            self.Besok,
            self.lu,
            self.pada,
            self.ngomel,
            self.lagi,
            self.question_mark,
        ]
        result = dependency_parsing_one_sentence("Besok lu pada ngomel lagi?", True)

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))

    def test_input_single_sentence_invalid(self):
        self.Besok = ConlluData(
            idx="1",
            form="Besok",
            lemma="besok",
            upos="NOUN",
            xpos="_",
            feat="Number=Sing",
            head_id="0",
            deprel="root",
        )
        self.lu = ConlluData(
            idx="2",
            form="lu",
            lemma="lu",
            upos="X",
            xpos="_",
            feat="Foreign=Yes",
            head_id="1",
            deprel="nmod",
        )
        self.pada = ConlluData(
            idx="3",
            form="pada",
            lemma="pada",
            upos="ADP",
            xpos="_",
            feat="_",
            head_id="4",
            deprel="case",
        )
        self.ngomel = ConlluData(
            idx="4",
            form="ngomel",
            lemma="ngomel",
            upos="X",
            xpos="_",
            feat="Foreign=Yes",
            head_id="1",
            deprel="nmod",
        )
        self.lagi = ConlluData(
            idx="5",
            form="lagi",
            lemma="lagi",
            upos="ADV",
            xpos="_",
            feat="_",
            head_id="4",
            deprel="advmod",
        )
        self.question_mark = ConlluData(
            idx="6",
            form="?",
            lemma="?",
            upos="PUNCT",
            xpos="_",
            feat="_",
            head_id="1",
            deprel="punct",
        )
        expected = [
            self.Besok,
            self.lu,
            self.pada,
            self.ngomel,
            self.lagi,
            self.question_mark,
        ]
        result = dependency_parsing_one_sentence("Besok lu pada ngomel lagi?")

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))

    def test_input_empty_string_should_return_empty_list_informal(self):
        self.assertEqual(dependency_parsing_one_sentence("", True), [])

    def test_whitespace_before_beginning_and_after_end_of_sentence_informal(self):
        expected = [
            self.Besok,
            self.lu,
            self.pada,
            self.ngomel,
            self.lagi,
            self.question_mark,
        ]
        result = dependency_parsing_one_sentence(
            "     Besok lu pada ngomel lagi?      ", True
        )

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))

    # test invalid characters
    def test_invalid_character_should_return_SYM(self):
        self.Besok = ConlluData(
            idx="1",
            form="Besok",
            lemma="besok",
            upos="NOUN",
            xpos="_",
            feat="Number=Sing",
            head_id="0",
            deprel="root",
        )
        expected = [
            self.Besok,
            self.lu,
            self.star,
            self.ngomel,
            self.lagi,
            self.question_mark,
        ]
        result = dependency_parsing_one_sentence("Besok lu * ngomel lagi?", True)

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))

    def test_multiple_sentences_should_return_one_list_informal(self):
        self.question_mark = ConlluData(
            idx="6",
            form="?",
            lemma="?",
            upos="PUNCT",
            xpos="_",
            feat="_",
            head_id="7",
            deprel="punct",
        )
        expected = [
            self.Besok,
            self.lu,
            self.pada,
            self.ngomel,
            self.lagi,
            self.question_mark,
            self.Gue,
            self.gak,
            self.dot,
        ]
        result = dependency_parsing_one_sentence(
            "Besok lu pada ngomel lagi? Gue gak.", True
        )
        for i in range(len(expected)):
            print("compare")
            print(expected[i])
            print(result[i])

        self.assertTrue(all([expected[i] == result[i] for i in range(len(expected))]))
