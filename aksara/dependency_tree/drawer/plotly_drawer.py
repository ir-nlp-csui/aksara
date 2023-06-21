from typing import List
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots
import igraph

from aksara.conllu import ConlluData
from .abstract_drawer import AbstractDrawer
from ._drawer_utils import (
    create_igraph,
    filter_multiword,
    get_conllu_root,
    is_in_ipython,
    create_igraph_layout
)

# pylint: disable=W0212, W0221

class PlotlyDrawer(AbstractDrawer):
    """
    Plotly-based dependency tree drawer

    """
    def save_image(self,
            conllu_datas: List[List[ConlluData]],
            output_path: str,
            *args,
            **kwargs) -> None:
        """
        Draw and save dependency tree
        
        Parameters
        ----------
        conllu_datas: list of list of :class:`ConlluData`
            The conllu data that will be visualized
        
        output_path: str
            The file path to save the dependency tree image.
        
        figure: plotly.Figure, optional
            Figure at which the tree will be drawn at.
        
        fontsize: int, default=12
            The fontsize for text annotation inside a node.
        
        width: int, optional
            The width of the `figure`
        
        height: int, optional
            The height of the `figure`
            
        scale_x: float, default=1.0
            Scale the x-coordinate (horizontal) of all nodes.
        
        scale_y: float, default=1.0
            Scale the y-coordinate (vertical) of all nodes.

        Returns
        -------
        Plotly.Figure
            The figure at which dependency tree has been drawn.

        """

        figure = self.draw(conllu_datas, *args, **kwargs)
        figure.write_image(output_path)
        print(f"Image has been saved at {output_path}")

    def draw(
            self,
            conllu_datas: List[List[ConlluData]],
            figure: Figure = None,
            fontsize: int = 12,
            width: int = None,
            height: int = None,
            scale_x: float = 1.0,
            scale_y: float = 1.0
        ) -> Figure:
        """
        Draw dependency tree
        
        Parameters
        ----------
        conllu_datas: list of list of :class:`ConlluData`
            The conllu data that will be visualized

        figure: plotly.Figure, optional
            Figure at which the tree will be drawn at.
        
        fontsize: int, default=12
            The fontsize for text annotation inside a node.
        
        width: int, optional
            The width of the `figure`
        
        height: int, optional
            The height of the `figure`
            
        scale_x: float, default=1.0
            Scale the x-coordinate (horizontal) of all nodes.
        
        scale_y: float, default=1.0
            Scale the y-coordinate (vertical) of all nodes.

        Returns
        -------
        Plotly.Figure
            The figure at which dependency tree has been drawn.

        """

        filtered_conllus = list(map(filter_multiword, conllu_datas))
        vertex_size = 4 * fontsize

        heights = list(map(lambda conllus: len(conllus) * vertex_size, filtered_conllus))

        if figure is None:
            figure = make_subplots(rows=len(conllu_datas), cols=1, row_heights=heights)

        total_subplot = self._get_total_subplots(figure)
        if total_subplot != len(conllu_datas):
            raise ValueError("Total subplot in `figure` must be equal to "
                             + "the lenght of `conllu_datas`")

        self.__add_traces_to_figure(conllu_datas, figure, fontsize, scale_x, scale_y)

        if height is None:
            height = 1.5 * sum(heights)

        figure.update_layout(
            showlegend=False,
            width=width,
            height=height,
            margin={'l':0, 'r':0, 'b':0, 't':0}
        )

        axis = {
            'showline':False,
            'zeroline':False,
            'showgrid':False,
            'showticklabels':False
        }
        figure.update_xaxes(axis)
        figure.update_yaxes(axis)

        if not is_in_ipython():
            figure.show()

        return figure

    def _get_total_subplots(self, figure: Figure) -> int:

        if figure is None:
            return 0
        if figure._grid_ref is None:
            return 1

        # created using make_subplot
        row_range, col_range = figure._get_subplot_rows_columns()
        return len(row_range) * len(col_range)

    def __add_traces_to_figure(
            self,
            conllu_datas: List[List[ConlluData]],
            figure: Figure,
            fontsize: int,
            scale_x: float,
            scale_y: float
        ) -> None:

        row = col = 1
        max_col = self.__get_total_columns(figure)

        for conllu_data in conllu_datas:

            graph = create_igraph(conllu_data)
            root = get_conllu_root(conllu_data)

            # use Reingold-Tilford Tree layout
            layout = create_igraph_layout(graph, root, scale_x, scale_y)

            edge_trace = self.__create_edge_trace(graph, layout)

            vertex_trace = self.__create_vertex_trace(graph, layout, fontsize)

            if figure._grid_ref is None:
                figure.add_trace(edge_trace)
                figure.add_trace(vertex_trace)
            else:
                figure.add_trace(edge_trace, row=row, col=col)
                figure.add_trace(vertex_trace, row=row, col=col)

            col += 1
            if col > max_col:
                row += 1
                col = 1

    def __get_total_columns(self, figure: Figure) -> int:
        max_col = 1
        total_subplot = self._get_total_subplots(figure)
        if total_subplot > 1:
            max_col = len(figure._get_subplot_rows_columns()[1])

        return max_col

    def __create_edge_trace(self, graph: igraph.Graph, layout: igraph.Layout):

        edge_list = [e.tuple for e in graph.es] # list of edges

        edge_xs = []
        edge_ys = []
        for (vertex1, vertex2) in edge_list:
            edge_xs += [layout.coords[vertex1][0], layout.coords[vertex2][0], None]
            edge_ys += [layout.coords[vertex1][1], layout.coords[vertex2][1], None]

        edge_trace = go.Scatter(
            x=edge_xs,
            y=edge_ys,
            mode='lines',
            line={'color':'rgb(210,210,210)', 'width':2},
            hoverinfo='none'
        )

        return edge_trace

    def __create_vertex_trace(self, graph: igraph.Graph, layout: igraph.Layout, fontsize: int):

        vertex_xs = []
        vertex_ys = []
        for x_coord, y_coord in layout.coords:
            vertex_xs.append(x_coord)
            vertex_ys.append(y_coord)

        names = self.__create_vertex_names(graph)

        vertex_size = 4 * fontsize

        vertex_trace = go.Scatter(
            x=vertex_xs,
            y=vertex_ys,
            mode='markers+text',
            marker={'symbol':'circle-dot',
                    'size':vertex_size,
                    'color':'#6175c1',
                    'line':{'color':'rgb(50,50,50)', 'width':2},
                    'opacity':0.2
            },
            text=names,
            textposition='middle center',
            textfont={'size':fontsize},
            hoverinfo='none'
        )

        return vertex_trace

    def __create_vertex_names(self, graph: igraph.Graph) -> List[str]:
        names = []
        for raw_name in graph.vs['name']:
            splitted_name = raw_name.split("\n")

            if len(splitted_name) > 2:
                splitted_name[1] = f'<span style="color:red">{splitted_name[1]}</span>'

            names.append('<br>'.join(splitted_name))
        return names
