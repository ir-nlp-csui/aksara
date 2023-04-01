import codecs
import os
import re

from typing import List
from aksara.conllu import ConlluData
from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


def dependency_parsing_one_sentence(
    sentences: str, is_informal: bool = False, sep_regex: str = r"([\.\!\?]+[\s])"
) -> List:
    sentences = sentences.strip()

    if sentences == "":
        return []

    result = []

    splitted_sentences = re.split(codecs.decode(sep_regex, "unicode_escape"), sentences)
    sentence_list = []
    for i in range(len(splitted_sentences)):
        if i % 2 == 0:
            sentence_list.append(
                splitted_sentences[i]
                + (
                    splitted_sentences[i + 1]
                    if i != len(splitted_sentences) - 1
                    else ""
                )
            )

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser()

    for sentence in sentence_list:
        analyzed_sentence = analyze_sentence(
            sentence,
            default_analyzer,
            default_dependency_parser,
            v1=False,
            lemma=False,
            postag=False,
            informal=is_informal,
        )
        sentence_result = []
        for row in analyzed_sentence.split("\n"):
            idx, form, lemma, upos, xpos, feat, head_id, deprel, _, _ = row.split("\t")
            conllu_data = ConlluData(
                idx, form, lemma, upos, xpos, feat, head_id, deprel
            )
            sentence_result.append(conllu_data)

        result.append(sentence_result)

    if len(result) == 1:
        result = result[0]

    return result


def __get_default_analyzer() -> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()
