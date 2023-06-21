import unittest
from unittest.mock import Mock, patch
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from aksara.dependency_parser import DependencyParser
from aksara.pos_tagger import POSTagger
from aksara.conllu import ConlluData
import aksara.dependency_tree.drawer.plotly_drawer
from aksara.dependency_tree.drawer import PlotlyDrawer
from aksara.dependency_tree.drawer._drawer_utils import is_in_ipython

def get_tmp_dir():
    dir_path = os.path.dirname(__file__)
    return os.path.join(dir_path, '.plotly_drawer_temp')

# pylint: disable=W0212,R0801
@patch.object(go.Figure, 'show')
class TestPlotlyDrawer(unittest.TestCase):
    """Test Plotly Class
    """

    @classmethod
    def setUpClass(cls) -> None:
        os.mkdir(get_tmp_dir())
        return super().setUpClass()

    def setUp(self) -> None:
        one_sentece = 'Ani sudah memakai Python selama 5 tahun.'
        two_sentence = one_sentece + ' Sedangkan Budi sudah 3 tahun memakai Java.'

        parser = DependencyParser()
        self.one_sentence_conllu = parser.parse(one_sentece)
        self.two_sentence_conllu = parser.parse(two_sentence)

        self.upos_only_conllu = []
        tagger = POSTagger()
        for list_form_tag in tagger.tag(one_sentece):
            tmp = []
            for i, (form, tag) in enumerate(list_form_tag):
                tmp.append(ConlluData(idx=str(i), form=form, upos=tag))
            self.upos_only_conllu.append(tmp)

        self.drawer = PlotlyDrawer()

        self.temp_path = os.path.join(get_tmp_dir(), 'image.png')
        return super().setUp()


    def tearDown(self) -> None:
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

        return super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        os.rmdir(get_tmp_dir())
        return super().tearDownClass()

    @patch(
        aksara.dependency_tree.drawer.plotly_drawer.__name__ + '.print'
    )
    @patch.object(go.Figure, 'write_image')
    def test_save_image_one_sentence_conllu(self, mock_write_img: Mock, *_):
        self.drawer.save_image(self.one_sentence_conllu, self.temp_path)

        mock_write_img.assert_called_once_with(self.temp_path)

    @patch(
        aksara.dependency_tree.drawer.plotly_drawer.__name__ + '.print'
    )
    @patch.object(go.Figure, 'write_image')
    def test_save_image_two_sentence_conllu(self, mock_write_img: Mock, *_):
        self.drawer.save_image(self.two_sentence_conllu, self.temp_path)

        mock_write_img.assert_called_once_with(self.temp_path)

    @patch(
        aksara.dependency_tree.drawer.plotly_drawer.__name__ + '.print'
    )
    @patch.object(go.Figure, 'write_image')
    def test_save_image_upos_only_conllu(self, mock_write_img: Mock, *_):
        self.drawer.save_image(self.upos_only_conllu ,self.temp_path)

        mock_write_img.assert_called_once_with(self.temp_path)

    def test_get_total_subplot_none_fig(self, _):

        self.assertEqual(0, self.drawer._get_total_subplots(None))

    def test_get_total_subplot_from_fig_without_grid_ref(self, _):

        fig = go.Figure()

        self.assertEqual(1, self.drawer._get_total_subplots(fig))

    def test_get_total_subplot_from_fig_with_gridref(self, _):

        fig = make_subplots(rows=2, cols=3)

        self.assertEqual(6, self.drawer._get_total_subplots(fig))

    def test_raise_error_if_figure_subplots_length_differ_from_conllus(self, _):
        figure = make_subplots(rows= len(self.one_sentence_conllu) + 1, cols = 1)

        with self.assertRaises(ValueError):
            self.drawer.draw(self.one_sentence_conllu, figure=figure)

    def test_draw_will_create_figure_if_not_given(self, _):
        generated_figure = self.drawer.draw(self.one_sentence_conllu)

        self.assertIsNotNone(generated_figure)
        self.assertIsInstance(generated_figure, go.Figure)

    def test_draw_use_figure_from_user_if_exists(self, _):
        figure = go.Figure()
        used_figure = self.drawer.draw(self.one_sentence_conllu, figure)

        self.assertEqual(figure, used_figure)

    def test_draw_will_provide_height_if_not_given(self, _):
        generated_figure = self.drawer.draw(self.one_sentence_conllu)

        self.assertIsNotNone(generated_figure.layout.height)

    def test_draw_will_use_height_from_user_input(self, _):
        generated_figure = self.drawer.draw(self.one_sentence_conllu, height=100)

        self.assertEqual(100, generated_figure.layout.height)

    @patch(aksara.dependency_tree.drawer.plotly_drawer.__name__ + '.' + is_in_ipython.__name__)
    def test_must_not_call_figure_show_from_ipython(self, mock_iphyton: Mock, mock_show: Mock):
        mock_iphyton.return_value = True

        self.drawer.draw(self.one_sentence_conllu)

        mock_show.assert_not_called()

    @patch(aksara.dependency_tree.drawer.plotly_drawer.__name__ + '.' + is_in_ipython.__name__)
    def test_must_call_figure_show_from_non_ipython(self, mock_iphyton: Mock, mock_show: Mock):
        mock_iphyton.return_value = False

        self.drawer.draw(self.one_sentence_conllu)

        mock_show.assert_called_once()
