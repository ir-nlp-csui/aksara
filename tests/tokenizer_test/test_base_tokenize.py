from unittest.mock import patch, Mock

from tests.tokenizer_test.tokenizer_test_setup import TokenizerTestSetUp

from aksara.tokenizer import BaseTokenizer
from aksara.tokenizers import base_tokenize

class BaseTokenizerTest(TokenizerTestSetUp):
    """unittest for aksara.tokenizers.base_tokenize (tokenizer that ignore multiword token)"""

    def setUp(self) -> None:
        super().setUp()
        self.expected_multiword_input = ["biarlah", "saja"]

    @patch.object(BaseTokenizer, 'tokenize')
    def test_basetokenizer_class_method_called_once(self, tokenizer_mock: Mock):
        tokenizer_mock.return_value = ["sebuah", "string"], [False, False]
        base_tokenize("sebuah string")
        tokenizer_mock.assert_called_once_with("sebuah string")

    # for the following tests, the real analyze_sentence is used
    # reason:   we are not able to create unit test for aksara.tokenizer.BaseTokenize
    #           and there is no guarantee that the return format of
    #           BaseTokenize.tokenize won't be change. We want to prevent unit_test
    #           report False positive because we stub the return value of
    #           BaseTokenize.tokenize

    def test_base_tokenize_should_return_word_list(self):
        expected = ["saya", "makan"]
        self.assertListEqual(expected, base_tokenize("saya makan"))

    def test_empty_string_input(self):
        self.assertEqual([], base_tokenize(""))

    def test_input_that_contains_whitespace_only(self):
        self.assertEqual([], base_tokenize("    "))

    def test_one_sentence_tokenizer(self):
        result = base_tokenize(self.one_sentence)
        self.assertEqual(self.expected_one_sentence, result)

    def test_multiple_sentence_tokenizer(self):
        result = base_tokenize(self.multiple_sentence)
        self.assertEqual(self.expected_multiple_sentence, result)

    def test_input_contains_multiword_token(self):
        result = base_tokenize(self.multiword_input)
        self.assertEqual(self.expected_multiword_input, result)
