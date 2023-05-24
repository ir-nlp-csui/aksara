from typing import List
import aksara.tokenizer as _internal_tokenizer

from .abstract_tokenizer import AbstractTokenizer

# pylint: disable=R0903
class BaseTokenizer(AbstractTokenizer):
    """
    Class to perform tokenization (multiword token will NOT be splitted)
    """

    def __init__(self) -> None:
        self.__base_tokenizer = _internal_tokenizer.BaseTokenizer()

    def tokenize(self, text: str, ssplit: bool=True, **kwargs) -> List[List[str]]:
        """tokenize `text` without splitting multiword token

        Parameters
        ----------

        text: str
            text that will be tokenized
        
        ssplit: bool, default=True
            Tell tokenizer to split sentences (ssplit=False, assume the text as one sentence)
        
        Returns
        -------
        list of list of str
            List of all tokens in each sentences
        
        Examples
        --------
        >>> from aksara import BaseTokenizer
        >>> tokenizer = BaseTokenizer()
        >>> text = "Biarlah saja seperti itu"   # 'Biarlah' is a multiword token ('Biar' + 'lah')
        >>> tokenizer.tokenize(text)
        [['Biarlah', 'saja', 'seperti', 'itu']]

        """

        stripped_text = text.strip()

        if len(stripped_text) == 0:
            return []

        # self.__base_tokenizer.tokenize return a tuple that contains word_list and sunflags
        all_tokens = []

        for sentence in self._preprocess_text(stripped_text, ssplit):
            token_in_sentence, _ = self.__base_tokenizer.tokenize(sentence)
            all_tokens.append(token_in_sentence)

        return all_tokens
