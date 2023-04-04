from unittest.mock import patch, Mock
from tests.tokenizer_test.tokenizer_test_setup import TokenizerTestSetUp

import aksara.tokenizers
from aksara.core import analyze_sentence
from aksara.tokenizers import multiword_tokenize


class MultiWordTokenizerTest(TokenizerTestSetUp):
    """unittest for aksara.tokenizers.multiword_tokenize (tokenizer that handle multiword token)"""

    def setUp(self) -> None:
        super().setUp()
        self.expected_multiword_input = ["biar", "lah", "saja"]

    @patch(
        target= aksara.tokenizers.__name__ + "." + analyze_sentence.__name__
    )
    def test_must_not_call_analyze_sentence_for_empty_input(self, mock: Mock):
        word_list = multiword_tokenize("")

        mock.assert_not_called()
        self.assertEqual([], word_list)

    @patch(
        target= aksara.tokenizers.__name__ + "." + analyze_sentence.__name__
    )
    def test_must_not_call_analyze_sentence_for_whitespace_only_input(self, mock: Mock):
        word_list = multiword_tokenize(" ")

        mock.assert_not_called()
        self.assertEqual([], word_list)

    @patch(
        target= aksara.tokenizers.__name__ + "." + analyze_sentence.__name__
    )
    def test_should_call_analyze_sentence_when_input_contains_words(self, mock: Mock):
        multiword_tokenize("sebuah kata")

        mock.assert_called_once()


    # for the following tests, the real analyze_sentence is used
    # reason:   we are not able to create unit test for analyze_sentence
    #           and there is no guarantee that the return format of
    #           analyze_sentence won't be change. We want to prevent unit_test
    #           report False positive because we stub the return value of
    #           analyze_sentence

    def test_one_sentence_tokenizer(self):
        result = multiword_tokenize(self.one_sentence)
        self.assertEqual(self.expected_one_sentence, result)

    def test_multiple_sentence_tokenizer(self):
        result = multiword_tokenize(self.multiple_sentence)
        self.assertEqual(self.expected_multiple_sentence, result)

    def test_input_contains_multiword_token(self):
        result = multiword_tokenize(self.multiword_input)
        self.assertEqual(self.expected_multiword_input, result)
