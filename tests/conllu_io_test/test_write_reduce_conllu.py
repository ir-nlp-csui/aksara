import os
from typing import List, Tuple
import unittest

from aksara.utils.conllu_io import _write_reduce_conllu

def read_reduced_conllu(file_path: str) -> Tuple[List[List[Tuple[str, str, str]]], List[str]]:
    """read 3 columns conllu"""

    sep = "\t"  # Conllu default column separator
    result = []
    texts = []
    with open(file_path, "r", encoding="utf-8") as input_file:
        next_line = input_file.readline()  # '# sent_id = <int>'

        while next_line != "":
            text = input_file.readline().replace('# text = ', '')  # '# text = <str>'
            texts.append(text.strip())

            tmp_result = []

            row = input_file.readline()
            while row not in ["", "\n"]:
                idx, token, col = row.split(sep)
                tmp_result.append((idx, token, col.strip()))

                row = input_file.readline()

            next_line = input_file.readline()  # '# sent_id = <int>'
            result.append(tmp_result)

    return result, texts

def get_tmp_dir():
    module_path = os.path.realpath(__file__)
    dir_path, _ = os.path.split(module_path)
    return os.path.join(dir_path, ".testtemp")

class ReducedConlluTest(unittest.TestCase):
    """Test write reduce conllu"""

    @classmethod
    def setUpClass(cls) -> None:
        os.mkdir(get_tmp_dir())
        return super().setUpClass()

    def setUp(self) -> None:
        self.path1 = os.path.join(get_tmp_dir(), "file1.txt")
        self.all_path = [self.path1]
        return super().setUp()

    def tearDown(self) -> None:
        for file_path in self.all_path:
            if os.path.lexists(file_path):
                os.remove(file_path)

        return super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir(get_tmp_dir())
        return super().tearDownClass()

    def validate_helper(self, expected_conllu, expected_texts):
        actual_conllu, actual_text = read_reduced_conllu(self.path1)
        self.assertListEqual(expected_conllu, actual_conllu)
        self.assertListEqual(expected_texts, actual_text)

    def test_empty_list(self):

        _write_reduce_conllu([], [], self.path1)

        self.validate_helper([], [])

    def test_contains_multiword_token(self):
        list_conllu = [
            [('1-2', 'a', 'b'), ('1', 'b', 'c'), ('2', 'c', 'd')],
            [('1', 'a', 'd')]
        ]

        _write_reduce_conllu(['a b c', 'a'], list_conllu, self.path1)
        self.validate_helper(list_conllu, ['a b c', 'a'])

    def test_x_mode_raise_error_if_file_exists(self):

        _write_reduce_conllu([], [], self.path1, write_mode='x')

        with self.assertRaises(FileExistsError):
            _write_reduce_conllu([], [], self.path1, write_mode='x')

    def test_w_mode_overwrite_file(self):

        _write_reduce_conllu(['a'], [[('1', 'a', 'b')]], self.path1, write_mode='x')

        _write_reduce_conllu(['c'], [[('1', 'c', 'd')]], self.path1, write_mode='w')

        self.validate_helper([[('1', 'c', 'd')]], ['c'])

    def test_a_mode_append_file(self):

        _write_reduce_conllu(['a'], [[('1', 'a', 'b')]], self.path1)

        _write_reduce_conllu(['c'], [[('1', 'c', 'd')]], self.path1, write_mode='a')

        self.validate_helper([[('1', 'a', 'b')], [('1', 'c', 'd')]], ['a', 'c'])

    def test_sentence_list_len_differ_from_conllu_list(self):
        with self.assertRaises(ValueError):
            _write_reduce_conllu(['abc'], [], self.path1)


    def test_none_separator_use_default_separator(self):

        _write_reduce_conllu(['c'], [[('1', 'c', 'd')]], self.path1, write_mode='w', separator=None)

        self.validate_helper([[('1', 'c', 'd')]], ['c'])
