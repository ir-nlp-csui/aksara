from typing import List, Type, Any
from aksara.conllu import ConlluData
from ._drawer import MatplotlibDrawer, AbstractDrawer, PlotlyDrawer

class TreeDrawer:
    """
    Draw dependency tree with specific drawer (e.g. Matplotlib, Plotly, etc)

    Attributes
    ----------
    name_to_drawer: dict
        mapping drawer name with its instance
    
    Methods
    -------
    draw(conllu_datas)
        Draw dependency tree based on `conllu_datas`
    
    save_image(conllu_datas, ouput_path)
        Save dependency tree image

    """

    name_to_drawer = {
        'matplotlib' : MatplotlibDrawer(),
        'plotly': PlotlyDrawer()
    }

    def __init__(self, drawer: str = 'matplotlib') -> None:
        self.set_drawer(drawer)

    def draw(
        self,
        conllu_datas: List[List[ConlluData]],
        *args,
        **kwargs
    ) -> Any:
        """
        Draw dependency tree

        Parameters
        ----------
        conllu_datas: list of list of ConlluData
            conllu_datas that will be drawn
        
        *args: tuple
            will be passed to its drawer
        
        **kwargs
            will be passed to its drawer

        Returns
        -------
        Any
            See drawer return value

        See Also
        --------
        aksara.dependency_tree._drawer.MatplotlibDrawer: Matplotlib drawer instance
        aksara.dependency_tree._drawer.PlotlyDrawer: Plotly drawer instance
        """

        return self.__drawer.draw(conllu_datas, *args, **kwargs)

    def save_image(
        self,
        conllu_datas: List[List[ConlluData]],
        output_path: str,
        *args,
        **kwargs
    ) -> None:
        """
        Draw dependency tree

        Parameters
        ----------
        conllu_datas: list of list of ConlluData
            conllu_datas that will be drawn and saved
        
        output_path: str
            file path at which the dependency tree image will be saved
        
        *args: tuple
            will be passed to its drawer
        
        **kwargs
            will be passed to its drawer

        Returns
        -------
        None

        See Also
        --------
        aksara.dependency_tree._drawer.MatplotlibDrawer: Matplotlib drawer instance
        aksara.dependency_tree._drawer.PlotlyDrawer: Plotly drawer instance
        """

        self.__drawer.save_image(conllu_datas, output_path, *args, **kwargs)

    def get_drawer(self) -> Type[AbstractDrawer]:
        """drawer instance getter
        """

        return self.__drawer

    def set_drawer(self, drawer: str) -> None:
        """drawer setter
        """

        drawer_instance = TreeDrawer.name_to_drawer.get(drawer, None)

        if drawer_instance is None:
            raise ValueError(f"drawer name must be one of {TreeDrawer.name_to_drawer.keys()}")

        self.__drawer = drawer_instance
