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
        """
        Abstract method that performs tokenization

        Parameters
        ----------
        text: str
            text that will be tokenized
        *args : tuple
            see concrete implementation
        **kwargs: dict
            see concrete implementation
        """
        raise NotImplementedError("`tokenize` method is not implemented")
