from unittest import TestCase
from aksara.morphological_analyzer import MorphologicalAnalyzer

class MorphologicalAnalyzerInputTextTest(TestCase):
    """ class to test Morphological Analyzer input text"""

    def setUp(self) -> None:
        self.morphological_analyzer = MorphologicalAnalyzer()
        return super().setUp()

class MorphologicalAnalyzerInputITextFormalTest(MorphologicalAnalyzerInputTextTest):

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

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual(
            self.morphological_analyzer.analyze(''), []
        )

    def test_input_text(self):
        result = self.morphological_analyzer.analyze(
            "Seluruh pakaian saya sudah kering. Kemarin matahari bersinar terang.")
        self.assertListEqual(self.formal_sentence_result, result)

    def test_whitespace_before_beginning_and_after_end_of_sentences(self):
        result = self.morphological_analyzer.analyze(
            "    Seluruh pakaian saya sudah kering. Kemarin matahari bersinar terang.  ")
        self.assertListEqual(self.formal_sentence_result, result)

class MorphologicalAnalyzerInputITextInformalTest(MorphologicalAnalyzerInputTextTest):

    def setUp(self) -> None:

        self.informal_sentence_result = [
            [("gw", ["Abbr=Yes", "Number=Sing", "Person=1", "Polite=Infm", "PronType=Prs"]),
             ("gak", ["Abbr=Yes", "Polarity=Neg", "Polite=Infm"]),
             ("lg", ["Abbr=Yes", "Polite=Infm"]),
             ("minum", []),
             (".", [])]
        ]

        return super().setUp()

    def test_input_text(self):
        result = self.morphological_analyzer.analyze(
            "gw gak lg minum.", is_informal=True)
        self.assertListEqual(self.informal_sentence_result, result)

    def test_whitespace_before_beginning_and_after_end_of_sentences(self):
        result = self.morphological_analyzer.analyze(
            "    gw gak lg minum.  ", is_informal=True)
        self.assertListEqual(self.informal_sentence_result, result)
