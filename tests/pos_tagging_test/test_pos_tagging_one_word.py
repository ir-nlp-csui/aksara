import unittest
from aksara.pos_tagging import pos_tagging_one_word

class PosTagOneWordTest(unittest.TestCase):
    """Test pos tagging with one word input"""

    def test_valid_word_should_return_pos_tag(self):
        self.assertEqual(pos_tagging_one_word('makan'), 'VERB')
        self.assertEqual(pos_tagging_one_word('minum'), 'VERB')

    def test_unknown_indo_word_should_return_x(self):
        self.assertEqual(pos_tagging_one_word('eat'), 'X')
        self.assertEqual(pos_tagging_one_word('drink'), 'X')

    def test_empty_string_should_return_empty_string(self):
        self.assertEqual(pos_tagging_one_word(""), "")

    def test_should_treat_multi_words_input_as_one_word(self):
        multi_word_inp = "aku mau makan nasi goreng"
        self.assertEqual(pos_tagging_one_word(multi_word_inp), "X")

    def test_multi_word_uncommon_separator(self):
        words = "aku.mau.makan"
        self.assertEqual(pos_tagging_one_word(words), "X")

    def test_should_give_warning_when_input_is_multi_words(self):

        with self.assertWarns(UserWarning):
            pos_tagging_one_word("aku mau makan")

    def test_informal_input(self):
        self.assertEqual(pos_tagging_one_word("gw", is_informal=True), "PRON")
