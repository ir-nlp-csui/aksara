import unittest

from aksara.morphological_analyzer import *


class MorphologicalAnalyzerTest(unittest.TestCase):

    def test_morphological_analyzer(self):
        testcase = "Seluruh pakaian saya sudah kering. Kemarin matahari bersinar terang."
        expected = [
            [("Seluruh", []),
             ("pakaian", ["Number=Sing"]),
             ("saya", ["Number=Sing","Person=1","PronType=Prs"]),
            ("sudah", []),
            ("kering", []),
            (".", [])]
            ,
            [("Kemarin", ["Number=Sing"]),
             ("matahari", ["Number=Sing"]),
             ("bersinar", ["Voice=Act"]),
            ("terang", []),
            (".", [])]
        ]

        self.assertEqual(morphological_analyzer(testcase), expected)

    def test_morphological_analyzer_informal(self):
        testcase = "gw gak lg minum."
        expected = [
            [("gw", ["Abbr=Yes","Number=Sing","Person=1","Polite=Infm","PronType=Prs"]),
             ("gak", ["Abbr=Yes", "Polarity=Neg", "Polite=Infm"]),
             ("lg", ["Abbr=Yes", "Polite=Infm"]),
             ("minum", []),
             (".", [])]
        ]

        self.assertEqual(morphological_analyzer(testcase, is_informal=True), expected)

    def test_morphological_analyzer_empty(self):
        testcase = ""
        expected = []

        self.assertEqual(morphological_analyzer(testcase), expected)

    def test_input_file(self):
        expected = [
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

        file_path = os.path.join(os.path.dirname(
            __file__), "test_morphological.txt")
        result = morphological_analyzer_from_file(file_path)

        self.assertEqual(result, expected)

    def test_input_file_incorrect_filepath(self):
        file_path = os.path.join(os.path.dirname(
            __file__), "file_doesnt_exist.txt")

        with self.assertRaises(FileNotFoundError):
            morphological_analyzer_from_file(file_path)

    def test_output_file(self):

        output_path = os.path.join(os.path.dirname(
            __file__), "new_morph.txt")

        result = morphological_analyzer_from_text_to_file("aku makan. kamu minum.", output_path)

        self.assertEqual(result, output_path)

    def test_output_file_unknown_write_mode(self):

        output_path = os.path.join(os.path.dirname(
            __file__), "new_morph.txt")

        self.assertRaises(
            ValueError,
            lambda: morphological_analyzer_from_text_to_file(
                "teks", output_path, write_mode='unknown')
        )

    def test_output_file_x_mode_already_exixt(self):

        file_path = os.path.join(os.path.dirname(
            __file__), "test_already_exixt.txt")

        self.assertRaises(
            FileExistsError,
            lambda: morphological_analyzer_from_text_to_file(
                "sudah ada", file_path, write_mode='x')
        )

    def test_output_file_a_mode_already_exixt(self):

        file_path = os.path.join(os.path.dirname(
            __file__), "test_already_exixt.txt")

        str_before = ""
        str_after = ""

        with open(file_path, 'r') as file:
            str_before = file.read()

        result = morphological_analyzer_from_text_to_file("kamu minum.",
                                                          output_path=file_path,
                                                          write_mode='a')

        with open(file_path, 'r') as file:
            str_after = file.read()

        self.assertTrue(str_before in str_after)
        self.assertNotEqual(str_before, str_after)
        self.assertEqual(result, file_path)


    def test_input_file_output_file(self):

        input_path = os.path.join(os.path.dirname(
            __file__), "test_morphological.txt")

        output_path = os.path.join(os.path.dirname(
            __file__), "new_morph_2.txt")

        result = morphological_analyzer_from_file_to_file(
            input_path, output_path)

        self.assertEqual(result, output_path)

    def test_input_file_output_file_same_path(self):

        file_path = os.path.join(os.path.dirname(
            __file__), "test_morphological.txt")

        result = morphological_analyzer_from_file_to_file(
            file_path, file_path)

        self.assertEqual(
            result, "input_path and output_path must be different")
