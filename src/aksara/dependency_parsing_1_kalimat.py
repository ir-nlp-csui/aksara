import codecs
import os
import re

from typing import List
from aksara.conllu import ConlluData
from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


def dependency_parsing_one_sentence(
    sentence: str, is_informal: bool = False, sep_regex: str = r"([\.\!\?]+[\s])"
) -> List:
    sentence = str(sentence).strip()

    if sentence == "":
        return []

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser()

    analyzed_sentence = analyze_sentence(
        sentence,
        default_analyzer,
        default_dependency_parser,
        v1=False,
        lemma=False,
        postag=False,
        informal=is_informal,
    )
    result = []
    for row in analyzed_sentence.split("\n"):
        idx, form, lemma, upos, xpos, feat, head_id, deprel, _, _ = row.split("\t")
        conllu_data = ConlluData(idx, form, lemma, upos, xpos, feat, head_id, deprel)
        result.append(conllu_data)

    return result


def __get_default_analyzer() -> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()
