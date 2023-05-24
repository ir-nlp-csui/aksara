from typing import List, Type, Any
from aksara.conllu import ConlluData
from .drawer import MatplotlibDrawer, AbstractDrawer, PlotlyDrawer

class TreeDrawer:
    """
    Draw dependency tree with specific drawer (e.g. Matplotlib, Plotly, etc)
    
    See Also
    --------
    :class:`aksara.dependency_tree.drawer.MatplotlibDrawer`: drawer for `drawer_name='matploltlib'`
    :class:`aksara.dependency_tree.drawer.PlotlyDrawer`: drawer for `drawer_name='plotly'`
    
    """

    name_to_drawer = {
        'matplotlib' : MatplotlibDrawer(),
        'plotly': PlotlyDrawer()
    }

    def __init__(self, drawer_name: str = 'matplotlib') -> None:
        self.set_drawer(drawer_name)

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
            will be passed to its drawer instance
        
        **kwargs
            will be passed to its drawer instance

        Returns
        -------
        Any
            See drawer return value

        See Also
        --------
        :class:`aksara.dependency_tree.drawer.MatplotlibDrawer`: 
            drawer instance for `drawer_name='matploltlib'`
        :class:`aksara.dependency_tree.drawer.PlotlyDrawer`: 
            drawer instance for `drawer_name='plotly'` 
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
        Save dependency tree

        Parameters
        ----------
        conllu_datas: list of list of ConlluData
            conllu_datas that will be drawn and saved
        
        output_path: str
            file path at which the dependency tree image will be saved
        
        *args: tuple
            will be passed to its drawer instance
        
        **kwargs
            will be passed to its drawer instance

        Returns
        -------
        None

        See Also
        --------
        :class:`aksara.dependency_tree.drawer.MatplotlibDrawer`: 
            drawer instance for `drawer_name='matploltlib'`
        :class:`aksara.dependency_tree.drawer.PlotlyDrawer`: 
            drawer instance for `drawer_name='plotly'`

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
