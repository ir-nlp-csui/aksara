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
            [("Seluruh", []),
             ("pakaian", ["Number=Sing"]),
             ("saya", ["Number=Sing", "Person=1", "PronType=Prs"]),
             ("sudah", []),
             ("kering", []),
             (".", [])],
            [("Kemarin", ["Number=Sing"]),
             ("matahari", ["Number=Sing"]),
             ("bersinar", ["Voice=Act"]),
             ("terang", []),
             (".", [])]
        ]

        return super().setUp()

    def test_input_empty_string_should_return_empty_list(self):
        self.assertEqual(
            self.morphological_feature.get_feature(''), []
        )

    def test_input_text(self):
        result = self.morphological_feature.get_feature(
            "Seluruh pakaian saya sudah kering. Kemarin matahari bersinar terang.")
        self.assertListEqual(self.formal_sentence_result, result)

    def test_whitespace_before_beginning_and_after_end_of_sentences(self):
        result = self.morphological_feature.get_feature(
            "    Seluruh pakaian saya sudah kering. Kemarin matahari bersinar terang.  ")
        self.assertListEqual(self.formal_sentence_result, result)

class MorphologicalFeatureInputITextInformalTest(MorphologicalFeatureInputTextTest):

    def setUp(self) -> None:

        self.informal_sentence_result = [
            [("gw", ["Abbr=Yes", "Number=Sing", "Person=1", "Polite=Infm", "PronType=Prs"]),
             ("gak", ["Abbr=Yes", "Polarity=Neg", "Polite=Infm"]),
             ("lg", ["Abbr=Yes", "Polite=Infm"]),
             ("minum", []),
             (".", [])]
        ]

        return super().setUp()

    def test_input_text(self):
        result = self.morphological_feature.get_feature(
            "gw gak lg minum.", is_informal=True)
        self.assertListEqual(self.informal_sentence_result, result)

    def test_whitespace_before_beginning_and_after_end_of_sentences(self):
        result = self.morphological_feature.get_feature(
            "    gw gak lg minum.  ", is_informal=True)
        self.assertListEqual(self.informal_sentence_result, result)
