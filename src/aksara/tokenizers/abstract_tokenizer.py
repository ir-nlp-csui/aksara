from typing import List
from abc import ABCMeta, abstractmethod

# pylint: disable=R0903
class AbstractTokenizer(metaclass=ABCMeta):
    """
    Abstract class for Tokenization.
    
    Subclass only need to implement tokenize method
    
    """

    @abstractmethod
    def tokenize(self, text: str, *args, **kwargs) -> List[str]:
        """Abstract method that performs tokenization

        Parameters
        ----------
        text: str
            Text that will be tokenized
        *args : tuple
            See concrete implementation
        **kwargs: dict
            See concrete implementation
        
        Returns
        -------
        list of str
            List of all tokens in the text
        
        """
        raise NotImplementedError("`tokenize` method is not implemented")
