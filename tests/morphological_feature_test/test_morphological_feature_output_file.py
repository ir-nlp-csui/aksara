import os
from unittest import TestCase
from aksara.morphological_feature import MorphologicalFeature

class MorphologicalFeatureOutputFileTest(TestCase):
    """ class to test Morphological Feature output file"""

    def setUp(self) -> None:
        self.morphological_feature = MorphologicalFeature()
        self.input_filepath = os.path.join(
            os.path.dirname(__file__), "sample_input", "test_morphological.txt"
        )
        self.output_exist_filepath = os.path.join(
            os.path.dirname(__file__), "test_already_exist.txt"
        )
        self.output_filepath = os.path.join(os.path.dirname(
            __file__), "new_morph.txt")

        with open(self.output_exist_filepath, 'x', encoding="utf-8") as output_file:
            output_file.writelines("exist")

        return super().setUp()

    def tearDown(self) -> None:
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

        if os.path.exists(self.output_exist_filepath):
            os.remove(self.output_exist_filepath)
        return super().tearDown()

    def test_should_return_output_filepath(self):

        result = self.morphological_feature.get_feature_to_file(
            "aku makan. kamu minum.", self.output_filepath)

        self.assertEqual(result, self.output_filepath)

    def test_output_file_x_mode_already_exist(self):

        self.assertRaises(
            FileExistsError,
            lambda: self.morphological_feature.get_feature_to_file(
                "sudah ada.", self.output_exist_filepath , write_mode='x')
        )

    def test_output_file_a_mode_already_exist(self):

        str_before = ""
        str_after = ""

        with open(self.output_exist_filepath, 'r', encoding='utf-8') as file:
            str_before = file.read()

        result = self.morphological_feature.get_feature_to_file("kamu minum.",
                                                          self.output_exist_filepath,
                                                          write_mode='a')

        with open(self.output_exist_filepath, 'r', encoding='utf-8') as file:
            str_after = file.read()

        self.assertTrue(str_before in str_after)
        self.assertNotEqual(str_before, str_after)
        self.assertEqual(result, self.output_exist_filepath)

    def test_input_file_output_file(self):

        result = self.morphological_feature.get_feature_to_file(self.input_filepath,
                                                                           self.output_filepath,
                                                                           input_mode='f')

        self.assertEqual(result, self.output_filepath)
