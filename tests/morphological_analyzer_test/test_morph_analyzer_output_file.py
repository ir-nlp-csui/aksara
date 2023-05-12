from typing import List, Tuple
import unittest
import os

from aksara.morphological_analyzer import MorphologicalAnalyzer

def read_morph_file(file_path: str) -> List[List[Tuple[str, str]]]:
    """
    Morphological Analyzer in reduced CONLLU format (form with morf_colom)
    """

    sep = "\t"  # Conllu default column separator
    result = []
    with open(file_path, "r", encoding="utf-8") as input_file:
        next_line = input_file.readline()  # '# sent_id = <int>'

        while next_line != "":
            input_file.readline()  # '# text = <str>'

            tmp_result = []

            row = input_file.readline()
            while row not in ["", "\n"]:
                _, token, morph = row.split(sep)
                tmp_result.append((token, morph.strip()))

                row = input_file.readline()

            next_line = input_file.readline()  # '# sent_id = <int>'
            result.append(tmp_result)

    return result

tmp_dir = os.path.join(os.path.dirname(__file__), '.temp')


class TestMorphAnalyzerOutputFile(unittest.TestCase):
    """Test Morphological Analyzer with input string and output file

    """

    @classmethod
    def setUpClass(cls) -> None:
        os.mkdir(tmp_dir)
        return super().setUpClass()

    def setUp(self) -> None:
        self.analyzer = MorphologicalAnalyzer()
        self.path1 = os.path.join(tmp_dir, "file1.txt")
        self.all_path = [self.path1]
        return super().setUp()

    def tearDown(self) -> None:
        for file_path in self.all_path:
            if os.path.lexists(file_path):
                os.remove(file_path)

        return super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir(tmp_dir)
        return super().tearDownClass()

    def test_invalid_input_mode_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.analyzer.analyze_to_file('teks', self.path1, input_mode='unknown')

    def test_formal_input_string(self):
        text = 'Aku ingin tidur'
        self.analyzer.analyze_to_file(text, self.path1)

        expected = self.analyzer.analyze(text)
        self.assertListEqual(expected, read_morph_file(self.path1))

    def test_informal_input_string(self):
        informal_text = 'gw mau makan'
        self.analyzer.analyze_to_file(informal_text, self.path1, is_informal=True)

        expected = self.analyzer.analyze(informal_text, is_informal=True)
        self.assertListEqual(expected, read_morph_file(self.path1))

    def test_formal_input_file(self):
        file_path = os.path.join(os.path.dirname(__file__), 'sample_input', 'multiple_sentence.txt')

        expected = self.analyzer.analyze(file_path, input_mode='f')
        self.analyzer.analyze_to_file(file_path, self.path1, input_mode='f')

        actual = read_morph_file(self.path1)
        self.assertListEqual(expected, actual)
    
    def test_informal_input_file(self):
        file_path = os.path.join(os.path.dirname(__file__), 'sample_input', 'informal_text.txt')

        expected = self.analyzer.analyze(file_path, input_mode='f', is_informal=True)
        self.analyzer.analyze_to_file(file_path, self.path1, input_mode='f', is_informal=True)

        actual = read_morph_file(self.path1)
        self.assertListEqual(expected, actual)

    def test_input_file_not_exists_raise_error(self):

        with self.assertRaises(FileNotFoundError):
            self.analyzer.analyze_to_file('file not exists.txt', self.path1, input_mode='f')

    def test_unknown_write_mode_throws_error(self):

        with self.assertRaises(ValueError):
            self.analyzer.analyze_to_file('text', self.path1, write_mode='unknown')

    def test_x_write_mode_create_file_if_not_exists(self):

        self.assertFalse(os.path.lexists(self.path1))

        self.analyzer.analyze_to_file('text', self.path1, write_mode='x')

        self.assertTrue(os.path.lexists(self.path1))

    def test_x_write_mode_throws_error_if_file_exists(self):

        self.analyzer.analyze_to_file('text', self.path1, write_mode='x')

        self.assertTrue(os.path.lexists(self.path1))

        with self.assertRaises(FileExistsError):
            self.analyzer.analyze_to_file('', self.path1, write_mode='x')

    def test_w_write_mode_overwrite_file(self):
        self.analyzer.analyze_to_file('text pertama', self.path1)

        self.analyzer.analyze_to_file('text kedua', self.path1, write_mode='w')
        self.assertListEqual(
            self.analyzer.analyze('text kedua'),
            read_morph_file(self.path1)
        )

    def test_a_mode_append_file(self):
        self.analyzer.analyze_to_file('pertama', self.path1)
        old_content = self.analyzer.analyze('pertama')

        self.analyzer.analyze_to_file('kedua', self.path1, write_mode='a')
        new_content = self.analyzer.analyze('kedua')
        self.assertListEqual(
            old_content + new_content,
            read_morph_file(self.path1)
        )
