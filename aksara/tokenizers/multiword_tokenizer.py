from typing import List
from .._nlp_internal import _get_foma_script_path, TextNormalizer
from .._nlp_internal.dependency_parsing.core import DependencyParser
from .._nlp_internal.core import analyze_sentence
from .._nlp_internal.analyzer import BaseAnalyzer

from .abstract_tokenizer import AbstractTokenizer

# pylint: disable=R0903
class MultiwordTokenizer(AbstractTokenizer):
    """
    Class to perform tokenization (multiword token will be splitted)
    """

    def __init__(self) -> None:
        self.__base_analyzer = BaseAnalyzer(_get_foma_script_path(), TextNormalizer())
        self.__dependency_parser = DependencyParser()

    def tokenize(self, text: str, ssplit: bool=True, **kwargs) -> List[str]:
        """tokenize `text`

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
        >>> from aksara import MultiwordTokenizer
        >>> tokenizer = MultiwordTokenizer()
        >>> text = "Biarlah saja seperti itu"   # 'Biarlah' is a multiword token ('Biar' + 'lah')
        >>> tokenizer.tokenize(text)
        [['Biar', 'lah', 'saja', 'seperti', 'itu']]
        
        """

        stripped_text = text.strip()

        if len(stripped_text) == 0:
            return []

        all_tokens = []

        for stripped_sentence in self._preprocess_text(stripped_text, ssplit):
            analyzed_result = analyze_sentence(
                stripped_sentence,
                self.__base_analyzer,
                self.__dependency_parser,
                informal=True,
                v1=False,
                postag=True,
                lemma=False
            )

            result: List[str] = []
            for conllu_row in analyzed_result.split("\n"):
                idx, form, _ = conllu_row.split("\t")
                if "-" not in idx:
                    result.append(form)

            all_tokens.append(result)

        return all_tokens
