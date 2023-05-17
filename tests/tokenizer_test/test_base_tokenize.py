from functools import reduce
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

    def test_base_tokenize_should_return_word_list(self):
        expected = [["saya", "makan"]]
        self.assertListEqual(expected, self.tokenizer.tokenize("saya makan"))

    def test_empty_string_input(self):
        self.assertListEqual([], self.tokenizer.tokenize(""))

    def test_input_that_contains_whitespace_only(self):
        self.assertListEqual([], self.tokenizer.tokenize("    "))

    def test_one_sentence_tokenizer(self):
        result = self.tokenizer.tokenize(self.one_sentence)
        self.assertListEqual(self.expected_one_sentence, result)

    def test_multiple_sentence_tokenizer(self):
        result = self.tokenizer.tokenize(self.multiple_sentence)
        self.assertListEqual(self.expected_multiple_sentence, result)

    def test_multiple_sentence_tokenizer_no_sentence_split(self):
        result = self.tokenizer.tokenize(self.multiple_sentence, ssplit=False)
        
        reduced_list = [[token for tokens in self.expected_multiple_sentence for token in tokens]]
        self.assertListEqual(reduced_list, result)

    def test_input_contains_multiword_token(self):
        expected_multiword_input = [["biarlah", "saja"]]
        result = self.tokenizer.tokenize(self.multiword_input)
        self.assertListEqual(expected_multiword_input, result)
