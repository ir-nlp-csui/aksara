from typing import List
import aksara.tokenizer as _internal_tokenizer

from .abstract_tokenizer import AbstractTokenizer

# pylint: disable=R0903
class BaseTokenizer(AbstractTokenizer):
    """Class to perform tokenization (multiword token will NOT be splitted)
    
    """

    def __init__(self) -> None:
        self.__base_tokenizer = _internal_tokenizer.BaseTokenizer()

    def tokenize(self, text: str, *args, **kwargs) -> List[str]:
        """
        tokenize `text`

        Parameters
        ----------

        text: str
            text that will be tokenized
        
        Returns
        -------
        list of str
            list of all token in text
        """

        # self.__base_tokenizer.tokenize return a tuple that contains word_list and sunflags
        word_list, _ = self.__base_tokenizer.tokenize(text)
        return word_list
