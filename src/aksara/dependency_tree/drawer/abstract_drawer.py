from abc import ABCMeta, abstractmethod
from typing import List
from aksara.conllu import ConlluData

class AbstractDrawer(metaclass=ABCMeta):
    """
    Abstract class for all drawers.
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
        :class:`drawer.MatplotlibDrawer`: Matplotlib drawer instance
        :class:`drawer.PlotlyDrawer`: Plotly drawer instance
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
        """

        raise NotImplementedError("`save_image` method is not implemented")
