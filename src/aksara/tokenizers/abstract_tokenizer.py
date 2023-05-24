from typing import List
from abc import ABCMeta, abstractmethod
from ..core import split_sentence

# pylint: disable=R0903
class AbstractTokenizer(metaclass=ABCMeta):
    """
    Abstract class for Tokenization.
    
    Subclass only need to implement tokenize method
    
    """

    @abstractmethod
    def tokenize(self, text: str, ssplit: bool=True, **kwargs) -> List[List[str]]:
        """Abstract method that performs tokenization

        Parameters
        ----------
        text: str
            Text that will be tokenized
        ssplit: bool, default = True
            Tell tokenizer to split sentences (ssplit=False, assume the text as one sentence)
        *args : tuple
            See concrete implementation
        **kwargs: dict
            See concrete implementation
        
        Returns
        -------
        list of list of str
            List of all tokens in each sentences
        
        """
        raise NotImplementedError("`tokenize` method is not implemented")

    def _preprocess_text(self, text: str, ssplit: bool) -> List[str]:
        """
        Split sentence in the text and remove whitespace only sentence
        """

        if not ssplit:
            return [text]

        return split_sentence(text)
