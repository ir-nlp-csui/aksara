"""
This module contains unit test for internal methods
in dependency_tree_drawer.py
"""

import unittest
from unittest.mock import Mock, patch

from aksara.dependency_tree.drawer._drawer_utils import (
    filter_multiword,
    create_edge_list,
    get_conllu_root,
    create_igraph,
    is_in_ipython
)
import aksara.dependency_tree.drawer._drawer_utils

from aksara.conllu import ConlluData

# pylint: disable=W0212
class TestFilterMultiwordToken(unittest.TestCase):
    """Test filter_multiword function
    """

    def setUp(self) -> None:

        self.no_multiword = [
            ConlluData(idx='1', head_id='0'),
            ConlluData(idx='2', head_id='1')
        ]

        self.contains_multiword = [
            ConlluData(idx='1', head_id='0'),
            ConlluData(idx='2-3'),
            ConlluData(idx='2', head_id='3'),
            ConlluData(idx='3', head_id='1')
        ]

        self.no_head_ids = [
            ConlluData(idx='1'),
            ConlluData(idx='2')
        ]

        return super().setUp()

    def test_empty_input_should_return_empty(self):
        self.assertEqual([], filter_multiword([]))

    def test_should_keep_non_multiword_token(self):
        self.assertListEqual(self.no_multiword, filter_multiword(self.no_multiword))

    def test_should_keep_token_with_no_head_id(self):
        self.assertListEqual(self.no_head_ids, filter_multiword(self.no_head_ids))

    def test_should_remove_multiword_token(self):
        expected = self.contains_multiword.copy()
        expected.remove(ConlluData(idx='2-3'))

        self.assertListEqual(expected, filter_multiword(self.contains_multiword))


class TestCreateEdgeList(unittest.TestCase):
    """Test create_edge_list function
    """

    def setUp(self) -> None:

        self.conllu_datas = [
            ConlluData(idx='1', head_id='2'),
            ConlluData(idx='2', head_id='0'),
            ConlluData(idx='3', head_id='1'),
            ConlluData(idx='4', head_id='2')
        ]

        self.edge_list_expectation = [
            [0, 1],
            [2, 0],
            [3, 1]
        ]

        self.no_head_ids = [
            ConlluData(idx='1'),
            ConlluData(idx='2')
        ]

        return super().setUp()

    def test_empty_input_should_return_empty_list(self):
        self.assertEqual([], create_edge_list([]))

    def test_input_with_no_head_ids_should_return_empty_list(self):
        self.assertEqual([], create_edge_list(self.no_head_ids))

    def test_should_create_edge_list_based_on_head_ids_and_start_from_zero(self):
        self.assertListEqual(self.edge_list_expectation, create_edge_list(self.conllu_datas))

class TestGetRoot(unittest.TestCase):
    """Test get_conllu_root function
    """

    def setUp(self) -> None:
        self.single_root = [
            ConlluData(idx='1', head_id='2'),
            ConlluData(idx='2', head_id='0'),
        ]

        self.duplicate_root = [
            ConlluData(idx='1', head_id='0'),
            ConlluData(idx='2', head_id='0')
        ]

        self.no_root_conllu = [
            ConlluData(idx='1')
        ]

        return super().setUp()

    def test_empty_list_return_negative_one(self):
        self.assertEqual(-1, get_conllu_root([]))

    def test_no_root_conllu_return_negative_one(self):
        self.assertEqual(-1, get_conllu_root(self.no_root_conllu))

    def test_single_root_conllu_return_root_id(self):
        self.assertEqual(1, get_conllu_root(self.single_root))

    def test_return_first_root_for_conllu_with_duplicated_root(self):
        self.assertEqual(0, get_conllu_root(self.duplicate_root))

class TestCreateIGraph(unittest.TestCase):
    """Test create_igraph function
    """

    def setUp(self) -> None:

        self.full_detail_conllus = [
            ConlluData(idx='1', form='aku', upos='AUX', head_id='3', deprel='nsubj'),
            ConlluData(idx='2', form='sedang', upos='AUX', head_id='3', deprel='aux'),
            ConlluData(idx='3', form='makan', upos='VERB', head_id='0', deprel='root'),
            ConlluData(idx='4', form='malam', upos='NOUN', head_id='3', deprel='obj')
        ]

        self.conllu_without_head_ids = [
            ConlluData(idx='1', form='aku', upos='AUX'),
            ConlluData(idx='2', form='sedang', upos='AUX'),
            ConlluData(idx='3', form='makan', upos='VERB'),
            ConlluData(idx='4', form='malam', upos='NOUN')
        ]

        return super().setUp()

    def test_full_detail_conllus_vertex_names_contains_form_upos_deprel(self):
        graph = create_igraph(self.full_detail_conllus)

        expected_vertex_names = [
            conllu.get_form() + '\n' + conllu.get_deprel() + '\n' + conllu.get_upos()
            for conllu in self.full_detail_conllus
        ]
        self.assertListEqual(expected_vertex_names, graph.vs['name'])

    def test_no_head_ids_conllus_vertex_names_contains_from_upos(self):
        graph = create_igraph(self.conllu_without_head_ids)

        expected_vertex_names = [
            conllu.get_form() + '\n' + conllu.get_upos()
            for conllu in self.full_detail_conllus
        ]
        self.assertListEqual(expected_vertex_names, graph.vs['name'])


@patch(aksara.dependency_tree.drawer._drawer_utils.__name__ + '.' + 'get_ipython', create=True)
class TestInIPythonCheck(unittest.TestCase):
    """Test is_in_ipython function
    """

    def test_in_ipython_return_true(self, mock_ipython: Mock):
        
        self.assertTrue(is_in_ipython())

    def test_not_in_ipython_return_false(self, mock_ipython: Mock):
        mock_ipython.side_effect = NameError()
        self.assertFalse(is_in_ipython())