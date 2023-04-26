from abc import ABCMeta, abstractmethod
from typing import List
from aksara.conllu import ConlluData

class AbstractDrawer(metaclass=ABCMeta):
    """
    Abstract drawer class.
    Subclass must implement `draw` and `save_image` method
    
    """

    @abstractmethod
    def draw(self, conllu_datas: List[List[ConlluData]], *args, **kwargs):
        """
        abstract draw method
        
        Parameters
        ----------
        conllu_datas: list of list of ConlluData
            conllu_datas that will be drawn
        
        See Also
        --------
        aksara.dependency_tree._drawer.MatplotlibDrawer: Matplotlib drawer instance
        aksara.dependency_tree._drawer.PlotlyDrawer: Plotly drawer instance
        """

        raise NotImplementedError("`draw` method is not implemented")

    @abstractmethod
    def save_image(self, conllu_datas: List[List[ConlluData]], output_path: str, *args, **kwargs):
        """
        abstract draw method
        
        Parameters
        ----------
        conllu_datas: list of list of ConlluData
            conllu_datas that will be drawn and saved
        
        output_path: str
            file path at which the image will be saved
        
        See Also
        --------
        aksara.dependency_tree._drawer.MatplotlibDrawer: Matplotlib drawer instance
        aksara.dependency_tree._drawer.PlotlyDrawer: Plotly drawer instance
        """

        raise NotImplementedError("`save_image` method is not implemented")
