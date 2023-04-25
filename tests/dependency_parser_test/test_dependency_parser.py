from unittest import TestCase
from aksara.dependency_parser import DependencyParser


class DependencyParserTest(TestCase):

    def setUp(self) -> None:
        self.dependency_parser = DependencyParser()
        return super().setUp()

    def test_dependency_parse_should_raise_value_error_if_mode_is_not_file_and_text(self):
        with self.assertRaises(ValueError):
            self.dependency_parser.parse("sebuah kalimat", input_mode="unknown_mode")

    def test_dependency_parse_should_raise_value_error_if_model_is_unknown(self):
        with self.assertRaises(ValueError):
            self.dependency_parser.parse("sebuah kalimat", model="unknown_model")


class DependencyParserToFileTest(TestCase):

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
