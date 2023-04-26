import unittest
from unittest.mock import patch, Mock
import matplotlib.pyplot as plt

from aksara.dependency_tree import TreeDrawer
from aksara.dependency_tree._drawer import MatplotlibDrawer, PlotlyDrawer
from aksara.conllu import ConlluData

class TreeDrawerTest(unittest.TestCase):
    """Test TreeDrawer Class
    """

    def test_set_drawer_valid_drawer(self):
        tree_drawer = TreeDrawer()
        tree_drawer.set_drawer('plotly')

        self.assertIsInstance(tree_drawer.get_drawer(), PlotlyDrawer)

    def test_set_invalid_drawer_throw_error(self):
        tree_drawer = TreeDrawer()

        with self.assertRaises(ValueError):
            tree_drawer.set_drawer('not_exists_drawer')

    @patch.object(MatplotlibDrawer, 'draw')
    def test_draw_should_call_its_corresponding_draw_in_drawer(self, mock_drawer: Mock):
        tree_drawer = TreeDrawer('matplotlib')

        tree_drawer.draw([[ConlluData(idx='1')]])

        mock_drawer.assert_called_once()


    @patch.object(MatplotlibDrawer, 'draw')
    def test_draw_should_return_the_same_with_its_drawer(self, mock_drawer: Mock):
        expected_return = plt.figure()
        mock_drawer.return_value = expected_return

        tree_drawer = TreeDrawer('matplotlib')

        actual_return = tree_drawer.draw([[ConlluData(idx='1')]])

        self.assertEqual(expected_return, actual_return)


    @patch.object(MatplotlibDrawer, 'save_image')
    def test_save_image_should_call_its_corresponding_save_image_in_drawer(self, mock_drawer: Mock):
        tree_drawer = TreeDrawer('matplotlib')

        tree_drawer.save_image([[ConlluData(idx='1')]], 'tmp.jpg')

        mock_drawer.assert_called_once()

    def test_get_drawer(self):
        tree_drawer = TreeDrawer('matplotlib')

        self.assertIsInstance(tree_drawer.get_drawer(), MatplotlibDrawer)
