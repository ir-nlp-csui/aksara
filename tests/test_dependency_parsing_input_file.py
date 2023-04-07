import unittest
from aksara.dependency_parser_input_file import *
from aksara.conllu import ConlluData

class DependencyParsingInputFileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.apa = ConlluData(idx='1', form="Apa", lemma="apa",
                              upos="PRON", xpos="_", feat="_",
                              head_id='0', deprel="root")
        self.yang = ConlluData(idx='2', form="yang", lemma="yang",
                               upos="SCONJ", xpos="_", feat="_",
                               head_id='4', deprel="mark")
        self.kamu = ConlluData(idx='3', form="kamu", lemma="kamu",
                               upos="PRON", xpos="_", feat="Number=Sing|Person=2|PronType=Prs",
                               head_id='4', deprel="nsubj")
        self.inginkan = ConlluData(idx='4', form="inginkan", lemma="ingin",
                                   upos="VERB", xpos="_", feat="Voice=Act",
                                   head_id='1', deprel="acl")
        self.question_mark = ConlluData(idx='5', form="?", lemma="?",
                                        upos="PUNCT", xpos="_", feat="_",
                                        head_id='4', deprel="punct")
        self.saya = ConlluData(idx='1', form="Saya", lemma="saya",
                               upos="PRON", xpos="_", feat="Number=Sing|Person=1|PronType=Prs",
                               head_id='2', deprel="nsubj")
        self.ingin = ConlluData(idx='2', form="ingin", lemma="ingin",
                                upos="VERB", xpos="_", feat="_",
                                head_id='0', deprel="root")
        self.makan = ConlluData(idx='3', form="makan", lemma="makan",
                                upos="VERB", xpos="_", feat="_",
                                head_id='2', deprel="xcomp")
        self.dot = ConlluData(idx='4', form=".", lemma=".",
                              upos="PUNCT", xpos="_", feat="_",
                              head_id='3', deprel="punct")

        self.saya_2 = ConlluData(idx='1', form="Saya", lemma="saya",
                               upos="PRON", xpos="_", feat="Number=Sing|Person=1|PronType=Prs",
                               head_id='2', deprel="nsubj")
        self.ingin_2 = ConlluData(idx='2', form="ingin", lemma="ingin",
                                upos="VERB", xpos="_", feat="_",
                                head_id='0', deprel="root")
        self.tidur = ConlluData(idx='3', form="tidur", lemma="tidur",
                                upos="VERB", xpos="_", feat="_",
                                head_id='2', deprel="xcomp")
        self.dot_2 = ConlluData(idx='4', form=".", lemma=".",
                              upos="PUNCT", xpos="_", feat="_",
                              head_id='3', deprel="punct")
        
        
    def test_input_file(self):
        expected = [[self.apa, self.yang, self.kamu, self.inginkan, self.question_mark],
                    [self.saya, self.ingin, self.makan, self.dot],
                    [self.saya_2, self.ingin_2, self.tidur, self.dot_2]]

        filepath = os.path.join(os.path.dirname(__file__), "test_dependency.txt")
        result = dependency_parsing_input_file(filepath)

        self.assertTrue(
            all([
                expected[i][j] == result[i][j]
                for i in range(len(expected))
                for j in range(len(expected[i]))
            ])
        )



    def test__incorrect_filepath(self):
        filepath = os.path.join(os.path.dirname(__file__), "file_doesnt_exist.txt")

        with self.assertRaises(FileNotFoundError):
            dependency_parsing_input_file(filepath)

class DependencyParsingInputFileInformalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.apa = ConlluData(idx='1', form="Apa", lemma="apa",
                              upos="PRON", xpos="_", feat="_",
                              head_id='0', deprel="root")
        self.yg = ConlluData(idx='2', form="yg", lemma="yang",
                             upos="PRON", xpos="_", feat="Abbr=Yes|Polite=Infm|PronType=Rel",
                             head_id='1', deprel="nmod")
        self.lo = ConlluData(idx='3', form="lo", lemma="lo",
                             upos="PRON", xpos="_",
                             feat="Number=Sing|Person=2|Polite=Infm|PronType=Prs",
                             head_id='1', deprel="nmod")
        self.mau = ConlluData(idx='4', form="mau", lemma="mau",
                              upos="ADV", xpos="_", feat="_",
                              head_id='1', deprel="advmod")
        self.question_mark = ConlluData(idx='5', form="?", lemma="?",
                                        upos="PUNCT", xpos="_", feat="_",
                                        head_id='1', deprel="punct")
        self.gw = ConlluData(idx='1', form="Gw", lemma="gw",
                             upos="PRON", xpos="_",
                             feat="Abbr=Yes|Number=Sing|Person=1|Polite=Infm|PronType=Prs",
                             head_id='0', deprel="root")
        self.laper = ConlluData(idx='2', form="laper", lemma="lapar",
                               upos="ADJ", xpos="_", feat="Polite=Infm",
                               head_id='1', deprel="amod")
        self.dot = ConlluData(idx='3', form=".", lemma=".",
                              upos="PUNCT", xpos="_", feat="_",
                              head_id='2', deprel="punct")

    def test_input_file_informal(self):
        expected = [[self.apa, self.yg, self.lo, self.mau, self.question_mark],
                    [self.gw, self.laper, self.dot]]
        filepath = os.path.join(os.path.dirname(__file__), "test_dependency_informal.txt")
        result = dependency_parsing_input_file(filepath, is_informal=True)

        self.assertTrue(
            all([
                expected[i][j] == result[i][j]
                for i in range(len(expected))
                for j in range(len(expected[i]))
            ])
        )
