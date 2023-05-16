from unittest import TestCase
from aksara.morphological_feature import MorphologicalFeature


class MorphologicalFeatureInputTextTest(TestCase):
    """ class to test Morphological Feature input text"""

    def setUp(self) -> None:
        self.morphological_feature = MorphologicalFeature()
        return super().setUp()


class MorphologicalFeatureInputITextFormalTest(MorphologicalFeatureInputTextTest):

    def setUp(self) -> None:

        self.formal_sentence_result = [
            ("Seluruh", []),
            ("pakaian", ["Number=Sing"]),
            ("saya", ["Number=Sing", "Person=1", "PronType=Prs"]),
            ("sudah", []),
            ("kering", []),
            (".", [])
        ]

        return super().setUp()

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual(
            self.morphological_feature._get_feature_one_sentence(""), []
        )

    def test_unknown_word_should_return_foreign(self):
        expected = [
            ("klopi", ["Foreign=Yes"]),
            ("ssu", ["Foreign=Yes"])
        ]
        result = self.morphological_feature._get_feature_one_sentence(
            "klopi ssu")
        self.assertListEqual(expected, result)

    def test_symbol_should_return_empty_list(self):
        expected = [
            ("tidak", ["Polarity=Neg"]),
            ("***", [])
        ]
        result = self.morphological_feature._get_feature_one_sentence(
            "tidak ***")
        self.assertListEqual(expected, result)

    def test_input_single_sentence(self):
        result = self.morphological_feature._get_feature_one_sentence(
            "Seluruh pakaian saya sudah kering.")
        self.assertListEqual(self.formal_sentence_result, result)

    def test_whitespace_before_beginning_and_after_end_of_sentences(self):
        result = self.morphological_feature._get_feature_one_sentence(
            "    Seluruh pakaian saya sudah kering.  ")
        self.assertListEqual(self.formal_sentence_result, result)


class MorphologicalFeatureInputITextInformalTest(MorphologicalFeatureInputTextTest):

    def setUp(self) -> None:

        self.informal_sentence_result = [
            ("gw", ["Abbr=Yes", "Number=Sing", "Person=1", "Polite=Infm", "PronType=Prs"]),
            ("gak", ["Abbr=Yes", "Polarity=Neg", "Polite=Infm"]),
            ("lg", ["Abbr=Yes", "Polite=Infm"]),
            ("minum", []),
            (".", [])
        ]

        return super().setUp()

    def test_input_single_sentence(self):
        result = self.morphological_feature._get_feature_one_sentence(
            "gw gak lg minum.", is_informal=True)
        self.assertListEqual(self.informal_sentence_result, result)

    def test_unknown_word_should_return_foreign(self):
        expected = [
            ("klopi", ["Foreign=Yes"]),
            ("ssu", ["Foreign=Yes"])
        ]
        result = self.morphological_feature._get_feature_one_sentence(
            "klopi ssu", is_informal=True)
        self.assertListEqual(expected, result)

    def test_symbol_should_return_empty_list(self):
        expected = [
            ("gak", ["Abbr=Yes", "Polarity=Neg", "Polite=Infm"]),
            ("***", [])
        ]
        result = self.morphological_feature._get_feature_one_sentence(
            "gak ***", is_informal=True)
        self.assertListEqual(expected, result)

    def test_input_single_sentence_invalid(self):
        expected = [
            ("gw", ["Foreign=Yes"]),
            ("gak", ["Foreign=Yes"]),
            ("lg", ["Foreign=Yes"]),
            ("minum", []),
            (".", [])
        ]

        result = self.morphological_feature._get_feature_one_sentence(
            "gw gak lg minum.")
        self.assertListEqual(expected, result)

    def test_whitespace_before_beginning_and_after_end_of_sentences(self):
        result = self.morphological_feature._get_feature_one_sentence(
            "    gw gak lg minum.  ", is_informal=True)
        self.assertListEqual(self.informal_sentence_result, result)
