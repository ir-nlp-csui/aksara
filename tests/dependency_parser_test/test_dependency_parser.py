from unittest import TestCase
from aksara.dependency_parser import DependencyParser


class DependencyParserTest(TestCase):
    """Test Dependency Parser"""

    def setUp(self) -> None:
        self.all_models = [
            "FR_GSD-ID_CSUI",
            "FR_GSD-ID_GSD",
            "IT_ISDT-ID_CSUI",
            "IT_ISDT-ID_GSD",
            "EN_GUM-ID_CSUI",
            "EN_GUM-ID_GSD"
        ]
        self.dependency_parser = DependencyParser()
        return super().setUp()

    def test_dependency_parse_should_raise_value_error_if_mode_is_not_file_and_text(self):
        with self.assertRaises(ValueError):
            self.dependency_parser.parse("sebuah kalimat", input_mode="unknown_mode")

    def test_dependency_parse_should_raise_value_error_if_model_is_unknown(self):
        with self.assertRaises(ValueError):
            self.dependency_parser.parse("sebuah kalimat", model="unknown_model")

    def test_all_models_is_downloadable(self):
        for model in self.all_models:
            self.dependency_parser.parse("sebuah kalimat", model=model)


class DependencyParserToFileTest(TestCase):
    """
    Test Dependency Parser output to file
    """

    def setUp(self) -> None:
        self.dependency_parser = DependencyParser()
        return super().setUp()

    def test_dependency_parse_to_file_should_raise_value_error_if_mode_is_not_file_and_text(self):
        with self.assertRaises(ValueError):
            self.dependency_parser.parse_to_file(
                "sebuah kalimat", write_path="file_path", input_mode="unknown_mode"
            )

    def test_dependency_parse_to_file_should_raise_value_error_if_model_is_unknown(self):
        with self.assertRaises(ValueError):
            self.dependency_parser.parse_to_file(
                "sebuah kalimat", write_path="file_path", model="unknown_model"
            )
