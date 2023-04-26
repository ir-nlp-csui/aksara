from typing import List
from igraph import Graph
import igraph
from aksara.conllu import ConlluData

def filter_multiword(conllu_datas: List[ConlluData]) -> List[ConlluData]:

    filtered_conllu = list(
        filter(lambda conllu_row: '-' not in conllu_row.get_id(), conllu_datas)
    )

    return filtered_conllu

def get_conllu_root(conllu_datas: List[ConlluData]) -> int:
    """get the index (start from 0) of the conllu root (row with head_id='0' or deprel='root')"""

    for idx, conllu_data in enumerate(conllu_datas):
        if conllu_data.get_head_id() == '0':
            return idx

    return -1

def create_igraph(conllu_datas: List[ConlluData]) -> Graph:
    edge_list = create_edge_list(conllu_datas)

    num_of_vertexs = len(conllu_datas)

    graph = Graph(n=num_of_vertexs, edges=edge_list)

    vertex_names = []
    for conllu_data in conllu_datas:
        vs_name = f"{conllu_data.get_form()}\n"

        if conllu_data.get_deprel() != '_':
            vs_name += f"{conllu_data.get_deprel()}\n"

        vs_name += conllu_data.get_upos()

        vertex_names.append(vs_name)

    graph.vs['name'] = vertex_names
    return graph

def create_edge_list(conllu_datas: List[ConlluData]) -> List[List[int]]:

    edge_list = []

    for my_idx, conllu_row in enumerate(conllu_datas):
        if conllu_row.get_head_id() in ['_', '0']:
            continue

        offset = int(conllu_row.get_id()) - my_idx
        parent_idx = int(conllu_row.get_head_id())
        edge_list.append([my_idx, parent_idx - offset])

    return edge_list

def is_in_ipython() -> bool:
    return hasattr(__builtins__, '__IPYTHON__')

def create_igraph_layout(
        graph: igraph.Graph,
        root: int,
        scale_x: float,
        scale_y: float
    ) -> igraph.Layout:

    # use Reingold-Tilford Tree layout
    layout = None
    if root == -1:
        layout = graph.layout('rt')
    else:
        layout = graph.layout('rt', root=[root])

    # put the root at the top of the tree
    layout.rotate(180)

    # rotate the graph with respect to y-axis
    # counteract the previuos rotation (for x-coordinate)
    layout.rotate(180, dim1=0, dim2=0)

    layout.scale([scale_x, scale_y])
    return layout
