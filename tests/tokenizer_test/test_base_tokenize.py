from unittest.mock import patch, Mock

from tests.tokenizer_test.tokenizer_test_setup import TokenizerTestSetUp

import aksara.tokenizer as _internal_tokenizer
from aksara.tokenizers import BaseTokenizer

class BaseTokenizerTest(TokenizerTestSetUp):
    """Test BaseTokenizer class

    """

    def setUp(self) -> None:
        super().setUp()
        self.tokenizer = BaseTokenizer()

    @patch.object(_internal_tokenizer.BaseTokenizer, 'tokenize')
    def test_basetokenizer_class_method_called_once(self, tokenizer_mock: Mock):
        tokenizer_mock.return_value = ["sebuah", "string"], [False, False]
        self.tokenizer.tokenize("sebuah string")
        tokenizer_mock.assert_called_once_with("sebuah string")

    def test_base_tokenize_should_return_word_list(self):
        expected = ["saya", "makan"]
        self.assertListEqual(expected, self.tokenizer.tokenize("saya makan"))

    def test_empty_string_input(self):
        self.assertEqual([], self.tokenizer.tokenize(""))

    def test_input_that_contains_whitespace_only(self):
        self.assertEqual([], self.tokenizer.tokenize("    "))

    def test_one_sentence_tokenizer(self):
        result = self.tokenizer.tokenize(self.one_sentence)
        self.assertEqual(self.expected_one_sentence, result)

    def test_multiple_sentence_tokenizer(self):
        result = self.tokenizer.tokenize(self.multiple_sentence)
        self.assertEqual(self.expected_multiple_sentence, result)

    def test_input_contains_multiword_token(self):
        expected_multiword_input = ["biarlah", "saja"]
        result = self.tokenizer.tokenize(self.multiword_input)
        self.assertEqual(expected_multiword_input, result)
