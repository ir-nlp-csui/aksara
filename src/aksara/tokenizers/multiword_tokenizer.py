from typing import List
import os

from dependency_parsing.core import DependencyParser
from ..core import analyze_sentence
from ..analyzer import BaseAnalyzer

from .abstract_tokenizer import AbstractTokenizer

# pylint: disable=R0903
class MultiwordTokenizer(AbstractTokenizer):
    """Class to perform tokenization (multiword token will be splitted)
    
    """

    def __init__(self) -> None:
        __bin_path = os.path.join(os.path.dirname(__file__), "..", "bin", "aksara@v1.2.0.bin")
        self.__base_analyzer = BaseAnalyzer(__bin_path)
        self.__dependency_parser = DependencyParser()

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

        stripped_sentence = text.strip()

        if stripped_sentence == "":
            return []

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

        return result
