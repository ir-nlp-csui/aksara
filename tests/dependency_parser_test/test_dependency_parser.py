from unittest import TestCase
from unittest.mock import patch, Mock

import aksara.dependency_parser
from aksara.dependency_parser import dependency_parse, InputMode

DEPENDENCY_PARSE_INPUT_TEXT_MODULE_NAME = \
    aksara.dependency_parser.__name__ + '._dependency_parse_input_text'

DEPENDENCY_PARSE_INPUT_FILE_MODULE_NAME = \
    aksara.dependency_parser.__name__ + '._dependency_parse_input_file'


class DependencyParserEnumTest(TestCase):
    """class to test aksara.dependency_parser.InputMode enum class"""

    def setUp(self) -> None:
        self.values = [input_mode.value for input_mode in InputMode]
        return super().setUp()

    def test_enum_only_contains_text_and_file(self):
        expected = ['text', 'file']
        self.assertListEqual(expected, self.values)


class DependencyParserTest(TestCase):
    """class to test aksara.dependency_parser.dependency_parse method"""

    @patch(target=DEPENDENCY_PARSE_INPUT_TEXT_MODULE_NAME)
    def test_should_call_dependency_parse_input_text_if_mode_is_text(self, mock: Mock):
        dependency_parse("sebuah kalimat", InputMode.TEXT)
        self.assertEqual(1, mock.call_count)

    @patch(target=DEPENDENCY_PARSE_INPUT_TEXT_MODULE_NAME)
    def test_dependency_parse_input_text_called_with_correct_args(self, mock: Mock):
        dependency_parse("sebuah kalimat", InputMode.TEXT)

        expected_kwargs = {
            'sentences': 'sebuah kalimat',
            'is_informal': False,
            'sep_regex': None,
            'model': 'FR_GSD-ID_CSUI'
        }

        self.assertEqual(expected_kwargs, mock.call_args.kwargs)

    @patch(target=DEPENDENCY_PARSE_INPUT_FILE_MODULE_NAME)
    def test_should_call_dependency_parse_input_file_if_mode_is_file(self, mock: Mock):
        dependency_parse("filepath", InputMode.FILE)
        self.assertEqual(1, mock.call_count)

    @patch(target=DEPENDENCY_PARSE_INPUT_TEXT_MODULE_NAME)
    def test_dependency_parse_input_file_called_with_correct_args(self, mock: Mock):
        dependency_parse("filepath", InputMode.TEXT)

        expected_kwargs = {
            'sentences': 'filepath',
            'is_informal': False,
            'sep_regex': None,
            'model': 'FR_GSD-ID_CSUI'
        }

        self.assertEqual(expected_kwargs, mock.call_args.kwargs)

    def test_should_raise_value_error_if_mode_is_not_file_and_text(self):
        with self.assertRaises(ValueError):
            dependency_parse("sebuah kalimat", "unknown_mode")

    def test_should_raise_value_error_if_model_is_unknown(self):
        with self.assertRaises(ValueError):
            dependency_parse("sebuah kalimat", InputMode.TEXT, model="unknown_model")
