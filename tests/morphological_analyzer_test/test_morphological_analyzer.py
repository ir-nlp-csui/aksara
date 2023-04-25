from unittest import TestCase
from aksara.morphological_analyzer import MorphologicalAnalyzer

class MorphologicalAnalyzerTest(TestCase):

    def setUp(self) -> None:
        self.morphological_analyzer= MorphologicalAnalyzer()
        return super().setUp()

    def test_morphological_analyze_should_raise_value_error_if_mode_is_not_file_and_text(self):
        with self.assertRaises(ValueError):
            self.morphological_analyzer.analyze(
                "teks", input_mode="unknown_mode")

class MorphologicalAnalyzerToFileTest(TestCase):

    def setUp(self) -> None:
        self.morphological_analyzer= MorphologicalAnalyzer()
        return super().setUp()

    def test_morphological_analyze_to_file_should_raise_value_error_if_mode_is_not_f_or_s(self):
        with self.assertRaises(ValueError):
            self.morphological_analyzer.analyze_to_file(
                "teks", write_path="write_path", input_mode="unknown_mode"
            )

    def test_output_file_unknown_write_mode(self):

        with self.assertRaises(ValueError):
            self.morphological_analyzer.analyze_to_file(
                "teks", write_path="write_path", write_mode="unknown_mode"
            )