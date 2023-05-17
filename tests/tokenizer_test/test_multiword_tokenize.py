from functools import reduce
from unittest.mock import patch, Mock
from tests.tokenizer_test.tokenizer_test_setup import TokenizerTestSetUp

import aksara.tokenizers
from aksara.core import analyze_sentence
from aksara.tokenizers import MultiwordTokenizer


class MultiWordTokenizerTest(TokenizerTestSetUp):
    """unittest for aksara.tokenizers.multiword_tokenize (tokenizer that handle multiword token)"""

    def setUp(self) -> None:
        super().setUp()
        self.expected_multiword_input = [["biar", "lah", "saja"]]
        self.tokenizer = MultiwordTokenizer()

    @patch(
        target= aksara.tokenizers.multiword_tokenizer.__name__ + "." + analyze_sentence.__name__
    )
    def test_must_not_call_analyze_sentence_for_empty_input(self, mock: Mock):
        word_list = self.tokenizer.tokenize("")

        mock.assert_not_called()
        self.assertEqual([], word_list)

    @patch(
        target= aksara.tokenizers.multiword_tokenizer.__name__ + "." + analyze_sentence.__name__
    )
    def test_must_not_call_analyze_sentence_for_whitespace_only_input(self, mock: Mock):
        word_list = self.tokenizer.tokenize(" ")

        mock.assert_not_called()
        self.assertEqual([], word_list)

    @patch(
        target= aksara.tokenizers.multiword_tokenizer.__name__ + "." + analyze_sentence.__name__
    )
    def test_should_call_analyze_sentence_when_input_contains_words(self, mock: Mock):
        self.tokenizer.tokenize("sebuah kata")

        mock.assert_called_once()

    def test_one_sentence_tokenizer(self):
        result = self.tokenizer.tokenize(self.one_sentence)
        self.assertEqual(self.expected_one_sentence, result)

    def test_multiple_sentence_tokenizer(self):
        result = self.tokenizer.tokenize(self.multiple_sentence)
        self.assertEqual(self.expected_multiple_sentence, result)

    def test_multiple_sentence_tokenizer_no_sentence_split(self):
        result = self.tokenizer.tokenize(self.multiple_sentence, ssplit=False)
        
        reduced_list = [token for tokens in self.expected_multiple_sentence for token in tokens]
        self.assertEqual([reduced_list], result)

    def test_input_contains_multiword_token(self):
        result = self.tokenizer.tokenize(self.multiword_input)
        self.assertEqual(self.expected_multiword_input, result)
