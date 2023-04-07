"""
This module a collection of tokenizer functions
"""

from typing import List
import os

from dependency_parsing.core import DependencyParser
from .core import analyze_sentence
from .analyzer import BaseAnalyzer
from .tokenizer import BaseTokenizer

__bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
__base_analyzer = BaseAnalyzer(__bin_path)
__dependency_parser = DependencyParser()

__base_tokenizer = BaseTokenizer()

def base_tokenize(sentence: str) -> List[str]:

    # __base_tokenizer.tokenize return a tuple that contains word_list and sunflags
    word_list, _ = __base_tokenizer.tokenize(sentence)

    return word_list

def multiword_tokenize(sentence: str) -> List[str]:

    stripped_sentence = sentence.strip()

    if stripped_sentence == "":
        return []

    analyzed_result = analyze_sentence(
        stripped_sentence,
        __base_analyzer,
        __dependency_parser,
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
