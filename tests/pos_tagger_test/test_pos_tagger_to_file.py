import unittest
import os
from typing import List, Tuple

from aksara.pos_tagger import POSTagger


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


class PosTagToFileTest(unittest.TestCase):
    """Pos Tag to File Test"""

    @classmethod
    def setUpClass(cls) -> None:
        os.mkdir(get_tmp_dir())
        return super().setUpClass()

    def setUp(self) -> None:
        self.pos_tagger = POSTagger()
        self.path1 = os.path.join(get_tmp_dir(), "pos_tag.txt")
        self.all_path = [self.path1]
        self.testcase = "Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton. Namun, tidak semua orang menyukai itu."
        self.expected = self.pos_tagger.tag(self.testcase)
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

    def test_to_file_from_string(self):
        self.pos_tagger.tag_to_file(self.testcase, self.path1)

        self.assertEqual(read_pos_tag_file(self.path1), self.expected)

    def test_to_file_from_file(self):
        testcase = os.path.join(
            os.path.dirname(__file__), "sample_input", "testinput_postag.txt"
        )

        expected = self.pos_tagger.tag(testcase, "f")

        self.pos_tagger.tag_to_file(testcase, self.path1, "f")

        self.assertEqual(read_pos_tag_file(self.path1), expected)

    def test_incorrect_input_type(self):
        with self.assertRaises(ValueError):
            self.pos_tagger.tag_to_file(self.testcase, self.path1, "S")

    def test_file_already_exists(self):
        testcase = "Hari ini cerah, ya!"
        expected = self.pos_tagger.tag(testcase)

        self.pos_tagger.tag_to_file(self.testcase, self.path1)

        self.pos_tagger.tag_to_file(testcase, self.path1)

        self.assertEqual(read_pos_tag_file(self.path1), expected)
