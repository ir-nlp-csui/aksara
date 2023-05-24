import unittest
import os

from aksara.utils.conllu_io import read_conllu, write_conllu
from aksara.conllu import ConlluData


def get_tmp_dir():
    module_path = os.path.realpath(__file__)
    dir_path, _ = os.path.split(module_path)
    return os.path.join(dir_path, '.conllu_writer_temp')

class ConlluWriterTest(unittest.TestCase):
    """class to test aksara.utils.conllu_io.write_conllu method"""
    @classmethod
    def setUpClass(cls) -> None:
        os.mkdir(get_tmp_dir())
        return super().setUpClass()

    def setUp(self) -> None:

        self.path1 = os.path.join(get_tmp_dir(), 'file1.txt')
        self.all_path = [self.path1]
        self.one_sentence_text = 'Andi pergi ke pasar.'
        self.multi_sentence_text = self.one_sentence_text + \
                                    ' Kemudian, Budi tidur'

        self.single_sentence_conllu = [
            [
                ConlluData(
                    '1', form='Andi', lemma='Andi',
                    upos='PROPN', xpos='_', feat='_',
                    head_id='2', deprel='nsubj'
                ),
                ConlluData(
                    '2', form='pergi', lemma='pergi',
                    upos='VERB', xpos='_', feat='_',
                    head_id='0', deprel='root'
                ),
                ConlluData(
                    '3', form='ke', lemma='ke',
                    upos='ADP', xpos='_', feat='_',
                    head_id='4', deprel='case'
                ),
                ConlluData(
                    '4', form='pasar', lemma='pasar',
                    upos='NOUN', xpos='_', feat='Number=Sing',
                    head_id='2', deprel='obl'
                ),
                ConlluData(
                    '5', form='.', lemma='.',
                    upos='PUNCT', xpos='_', feat='_',
                    head_id='4', deprel='punct'
                )
            ]
        ]

        self.multiple_sentence_conllu = self.single_sentence_conllu + [
            [
                ConlluData(
                    '1', form='Kemudian', lemma='kemudi',
                    upos='NOUN', xpos='_', feat='Number=Sing',
                    head_id='4', deprel='obl'
                ),
                ConlluData(
                    '2', form=',', lemma=',',
                    upos='PUNCT', xpos='_', feat='_',
                    head_id='4', deprel='punct'
                ),
                ConlluData(
                    '3', form='Budi', lemma='Budi',
                    upos='PROPN', xpos='_', feat='_',
                    head_id='4', deprel='nsubj'
                ),
                ConlluData(
                    '4', form='tidur', lemma='tidur',
                    upos='VERB', xpos='_', feat='_',
                    head_id='0', deprel='root'
                )
            ]
        ]

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

    def test_empty_list_input(self):

        dest_path = write_conllu([], [], self.path1)

        self.assertEqual([], read_conllu(dest_path))

    def test_single_sentence_input(self):

        dest_path = write_conllu([self.one_sentence_text], self.single_sentence_conllu,
                                 self.path1)

        self.assertListEqual(self.single_sentence_conllu,
                             read_conllu(dest_path))

    def test_multiple_sentence_input(self):
        dest_path = write_conllu(
            self.multi_sentence_text.split('.'),
            self.multiple_sentence_conllu,
            self.path1
        )

        self.assertListEqual(self.multiple_sentence_conllu,
                             read_conllu(dest_path))

    def test_all_mode_should_create_new_file_if_not_exists(self):
        not_exists_x = os.path.join(get_tmp_dir(), 'not_exists_x.txt')
        not_exists_w = os.path.join(get_tmp_dir(), 'not_exists_w.txt')
        not_exists_a = os.path.join(get_tmp_dir(), 'not_exists_a.txt')

        self.assertFalse(os.path.lexists(not_exists_x))
        self.assertFalse(os.path.lexists(not_exists_w))
        self.assertFalse(os.path.lexists(not_exists_a))

        new_file_x = write_conllu([], [], not_exists_x, write_mode='x')
        new_file_w = write_conllu([], [], not_exists_w, write_mode='w')
        new_file_a = write_conllu([], [], not_exists_a, write_mode='a')

        self.assertTrue(os.path.lexists(new_file_x))
        self.assertTrue(os.path.lexists(new_file_w))
        self.assertTrue(os.path.lexists(new_file_a))

        # clean up
        os.remove(not_exists_x)
        os.remove(not_exists_w)
        os.remove(not_exists_a)

    def test_x_mode_should_raise_error_if_file_already_exists(self):

        write_conllu([], [], self.path1)

        with self.assertRaises(FileExistsError):
            write_conllu([], [], self.path1)

        os.remove(self.path1)

    def test_w_mode_should_overwrite_old_file_content(self):
        # create a non empty file
        with open(self.path1, 'w', encoding='utf-8') as file:
            file.writelines("abc def")

        self.assertTrue(os.path.lexists(self.path1))

        dest_path = write_conllu([self.one_sentence_text], self.single_sentence_conllu, self.path1, write_mode='w')

        self.assertListEqual(self.single_sentence_conllu,
                             read_conllu(dest_path))

    def test_a_mode_should_append_conllu_class(self):

        # write self.single_sentence_conllu into self.path1
        dest_path = write_conllu([self.one_sentence_text], self.single_sentence_conllu, self.path1)
        self.assertListEqual(self.single_sentence_conllu,
                             read_conllu(dest_path))

        # then append self.multiple_sentence_connlu
        dest_path = write_conllu(self.multi_sentence_text.split('.'), self.multiple_sentence_conllu, dest_path, write_mode='a')
        self.assertListEqual(
            self.single_sentence_conllu + self.multiple_sentence_conllu,
            read_conllu(dest_path)
        )

    def test_should_raise_value_error_for_unknown_write_mode(self):

        with self.assertRaises(ValueError):
            write_conllu([], [], self.path1, write_mode='unknown')


    def test_writer_custom_separator(self):

        dest_path = write_conllu([self.one_sentence_text], self.single_sentence_conllu, self.path1, separator='??')
        self.assertListEqual(self.single_sentence_conllu,
                             read_conllu(dest_path, separator=r'\?\?'))

    def test_sentence_list_len_differ_from_conllu_list(self):
        with self.assertRaises(ValueError):
            write_conllu(['abc'], [], self.path1)

    def test_none_separator_use_default_separator(self):

        dest_path = write_conllu([self.one_sentence_text], self.single_sentence_conllu, self.path1, separator=None)
        self.assertListEqual(self.single_sentence_conllu,
                             read_conllu(dest_path))