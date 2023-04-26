from typing import List, Union
import igraph
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np

from aksara.conllu import ConlluData
from ._abstract_drawer import AbstractDrawer
from ._drawer_utils import create_igraph, filter_multiword, get_conllu_root, create_igraph_layout

# pylint: disable=W0212, W0221
class MatplotlibDrawer(AbstractDrawer):
    """
    Matplotlib-based dependency tree drawer

    """

    def draw(
            self,
            conllu_datas: List[List[ConlluData]],
            axs: Union[List[plt.Axes], plt.Axes, np.ndarray] = None,
            scale_x: float = 1.0,
            scale_y: float = 1.0
        ) -> Figure:

        figure = None
        if axs is None:
            _, axs = plt.subplots(len(conllu_datas))

        if isinstance(axs, plt.Axes):
            axs = [axs]

        if isinstance(axs, np.ndarray) and len(axs.shape) > 1:
            raise RuntimeError("axs only accepts one dimensional array."
                             + "\n\tIf axs has been created using `plt.subplots`,"
                             + "then set ncols to 1"
                             + "\n\t(e.g. fig, axs = plt.subplots(n, 1))")

        if len(axs) != len(conllu_datas):
            raise RuntimeError("`axs` length must match `conllu_datas` length")

        figure = axs[0].figure

        for axis in axs:
            axis.clear()

        for i, conllu_data in enumerate(conllu_datas):
            filtered_conllu = filter_multiword(conllu_data)
            graph = create_igraph(filtered_conllu)
            root = get_conllu_root(filtered_conllu)

            graph.vs["color"] = [(0, 0, 0, 0.3)] * len(filtered_conllu)

            # use Reingold-Tilford Tree layout
            layout = create_igraph_layout(graph, root, scale_x, scale_y)

            # Currently, igraph support for matplotlib annotation is limited
            for j, coords in enumerate(layout):
                axs[i].annotate(
                    graph.vs["name"][j],
                    coords,
                    ha='left',
                    va='bottom',
                    bbox={
                        "boxstyle":'round', 
                        "facecolor":'wheat'
                    }
                )

            igraph.plot(graph, layout=layout, target=axs[i])

        if not plt.isinteractive():
            plt.show()

        plt.close(figure)

        return figure

    def save_image(self,
            conllu_datas: List[List[ConlluData]],
            output_path: str,
            *args,
            **kwargs) -> None:

        figure = self.draw(conllu_datas, *args, **kwargs)
        figure.savefig(output_path)

        print(f"Dependency tree image is successfully saved at {output_path}")
