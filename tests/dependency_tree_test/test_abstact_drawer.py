import unittest
from unittest.mock import patch

from aksara.dependency_tree.drawer import AbstractDrawer
from aksara.conllu import ConlluData

# pylint: disable=E0110
@patch.object(AbstractDrawer, '__abstractmethods__', set())
class TestAbstractDrawer(unittest.TestCase):
    """Test AbsractDrawer Class
    """

    def test_should_have_draw_and_save_image_method(self):
        all_attributes = dir(AbstractDrawer)
        self.assertIn('draw', all_attributes)
        self.assertIn('save_image', all_attributes)

    def test_override_abstract_draw(self):
        mock_instance = AbstractDrawer()

        with self.assertRaises(NotImplementedError):
            mock_instance.draw([[ConlluData('1')]])

    def test_override_absract_save_image(self):
        mock_instance = AbstractDrawer()

        with self.assertRaises(NotImplementedError):
            mock_instance.save_image([[ConlluData('1')]], 'out.jpg')
