import unittest
import os
from typing import List, Tuple

from aksara.pos_tag import _pos_tag_then_save_to_file, _pos_tag_multi_sentences


def read_pos_tag_file(file_path: str) -> List[List[Tuple[str, str]]]:
    """pos tag in CONLLU format"""

    sep = "\t"  # Conllu default column separator
    result = []
    with open(file_path, "r", encoding="utf-8") as input_file:
        next_line = input_file.readline()  # '# sent_id = <int>'

        while next_line != "":
            input_file.readline()  # '# text = <str>'

            tmp_result = []

            row = input_file.readline()
            while row not in ["", "\n"]:
                _, token, tag = row.split(sep)
                tmp_result.append((token, tag.strip()))

                row = input_file.readline()

            next_line = input_file.readline()  # '# sent_id = <int>'
            result.append(tmp_result)

    return result


def get_tmp_dir():
    module_path = os.path.realpath(__file__)
    dir_path, _ = os.path.split(module_path)
    return os.path.join(dir_path, ".testtemp")


class POSTagOutputFile(unittest.TestCase):
    """Test pos tagging that will put the result into a file"""

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

    def test_should_return_true_if_succesfully_save_pos_tag(self):
        self.assertTrue(_pos_tag_then_save_to_file("teks membaca", self.path1))

    def test_unknown_write_mode(self):
        self.assertRaises(
            ValueError,
            lambda: _pos_tag_then_save_to_file(
                "teks", self.path1, write_mode="unknown"
            ),
        )

    def test_x_mode_create_file_if_not_exists(self):
        self.assertFalse(os.path.lexists(self.path1))

        expected = _pos_tag_multi_sentences("Ani membaca buku.")

        _pos_tag_then_save_to_file("Ani membaca buku.", self.path1, write_mode="x")

        self.assertTrue(os.path.lexists(self.path1))
        self.assertEqual(expected, read_pos_tag_file(self.path1))

    def test_x_mode_throws_error_if_file_already_axists(self):
        # create file1
        with open(self.path1, "x", encoding="utf-8") as _:
            pass

        self.assertTrue(os.path.lexists(self.path1))

        self.assertRaises(
            FileExistsError,
            lambda: _pos_tag_then_save_to_file(
                "sebuah kalimat", self.path1, write_mode="x"
            ),
        )

    def test_w_mode_create_file_if_not_exists(self):
        self.assertFalse(os.path.lexists(self.path1))

        expected = _pos_tag_multi_sentences("Ani membaca buku.")

        _pos_tag_then_save_to_file("Ani membaca buku.", self.path1, write_mode="w")

        self.assertTrue(os.path.lexists(self.path1))
        self.assertEqual(expected, read_pos_tag_file(self.path1))

    def test_w_mode_will_overwrite_current_file_content(self):
        self.assertFalse(os.path.lexists(self.path1))

        expected = _pos_tag_multi_sentences("Buku.")

        _pos_tag_then_save_to_file("Buku.", self.path1, write_mode="w")

        self.assertTrue(os.path.lexists(self.path1))
        self.assertEqual(expected, read_pos_tag_file(self.path1))

        expected2 = _pos_tag_multi_sentences("budi tidur di kelas.")
        _pos_tag_then_save_to_file("budi tidur di kelas.", self.path1)

        self.assertEqual(expected2, read_pos_tag_file(self.path1))

    def test_a_mode_create_file_if_not_exists(self):
        self.assertFalse(os.path.lexists(self.path1))

        _pos_tag_then_save_to_file("Ani membaca buku.", self.path1, write_mode="a")

        self.assertTrue(os.path.lexists(self.path1))

    def test_a_mode_will_append__pos_tag_result(self):
        self.assertFalse(os.path.lexists(self.path1))

        expected = _pos_tag_multi_sentences("Buku.")

        _pos_tag_then_save_to_file("Buku.", self.path1, write_mode="w")

        self.assertTrue(os.path.lexists(self.path1))
        self.assertEqual(expected, read_pos_tag_file(self.path1))

        # combined with the _pos tag result in self.path1 ('Buku')
        expected2 = _pos_tag_multi_sentences("Buku. budi tidur di kelas.")
        _pos_tag_then_save_to_file("budi tidur di kelas.", self.path1, write_mode="a")

        self.assertEqual(expected2, read_pos_tag_file(self.path1))

    def test_empty_string_should_write_blank_file(self):
        expected = _pos_tag_multi_sentences("")

        _pos_tag_then_save_to_file("", self.path1)

        self.assertEqual(expected, read_pos_tag_file(self.path1))

    def test_one_sentence(self):
        expected = _pos_tag_multi_sentences("Ani suka makan")

        _pos_tag_then_save_to_file("Ani suka makan", self.path1)

        self.assertEqual(expected, read_pos_tag_file(self.path1))

    def test_multi_sentences(self):
        text = "Ani suka makan. Budi suka tidur. Caca suka belajar"
        expected = _pos_tag_multi_sentences(text)

        _pos_tag_then_save_to_file(text, self.path1)

        self.assertEqual(expected, read_pos_tag_file(self.path1))
