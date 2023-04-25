import os
from unittest import TestCase
from aksara.morphological_analyzer import MorphologicalAnalyzer

class MorphologicalAnalyzerInputFileTest(TestCase):
    """ class to test Morphological Analyzer input file"""

    def setUp(self) -> None:
        self.morphological_analyzer = MorphologicalAnalyzer()
        self.formal_filepath = os.path.join(
            os.path.dirname(__file__), "sample_input", "test_morphological.txt"
        )
        self.informal_filepath = os.path.join(
            os.path.dirname(__file__), "sample_input", "test_morphological_informal.txt"
        )
        return super().setUp()

class MorphologicalAnalyzerInputIFileFormalTest(MorphologicalAnalyzerInputFileTest):

    def setUp(self) -> None:

        self.formal_sentence_result = [
            [("Seluruh", []),
             ("pakaian", ["Number=Sing"]),
             ("saya", ["Number=Sing", "Person=1", "PronType=Prs"]),
             ("sudah", []),
             ("kering", []),
             (".", [])],
            [("Kemarin", ["Number=Sing"]),
             ("matahari", ["Number=Sing"]),
             ("bersinar", ["Voice=Act"]),
             ("terang", []),
             (".", [])]
        ]

        return super().setUp()

    def test_input_file(self):
        result = self.morphological_analyzer.analyze(
            self.formal_filepath, input_mode="f"
        )
        self.assertEqual(self.formal_sentence_result, result)

    def test_incorrect_filepath(self):
        filepath = os.path.join(
            os.path.dirname(
                __file__), "sample_input", "file_doesnt_exist.txt"
        )

        with self.assertRaises(FileNotFoundError):
            self.morphological_analyzer.analyze(
                filepath, input_mode="f"
            )

class MorphologicalAnalyzerInputIFileInformalTest(MorphologicalAnalyzerInputFileTest):

    def setUp(self) -> None:

        self.informal_sentence_result = [
            [("gw", ["Abbr=Yes", "Number=Sing", "Person=1", "Polite=Infm", "PronType=Prs"]),
             ("gak", ["Abbr=Yes", "Polarity=Neg", "Polite=Infm"]),
             ("lg", ["Abbr=Yes", "Polite=Infm"]),
             ("minum", []),
             (".", [])]
        ]

        return super().setUp()

    def test_input_file(self):
        result = self.morphological_analyzer.analyze(
            self.informal_filepath, input_mode="f", is_informal=True
        )
        self.assertEqual(self.informal_sentence_result, result)
