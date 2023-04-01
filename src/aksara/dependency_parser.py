import codecs
import os
import re

from typing import List, Literal
from aksara.conllu import ConlluData
from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser
from .utils.conllu_io import write_conllu

def dependency_parsing_multi_sentences(
        sentences: str, is_informal: bool = False, sep_regex: str = r'([\.\!\?]+[\s])'
) -> List[List[ConlluData]]:

    sentences = sentences.strip()

    if sentences == "":
        return []

    result = []

    splitted_sentences = re.split(codecs.decode(sep_regex, 'unicode_escape'), sentences)
    sentence_list = []
    for i in range(len(splitted_sentences)):
        if i % 2 == 0:
            sentence_list.append(
                splitted_sentences[i] + (
                    splitted_sentences[i+1] if i != len(splitted_sentences) - 1 else ""
                )
            )

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser()

    for sentence in sentence_list:
        analyzed_sentence = analyze_sentence(sentence, default_analyzer,
                                             default_dependency_parser, v1=False,
                                             lemma=False, postag=False, informal=is_informal)
        sentence_result = []
        for row in analyzed_sentence.split("\n"):
            idx, form, lemma, upos, xpos, feat, head_id, deprel, _, _ = row.split("\t")
            conllu_data = ConlluData(idx, form, lemma, upos, xpos,
                                     feat, head_id, deprel)
            sentence_result.append(conllu_data)

        result.append(sentence_result)

    return result

def parse_then_save_to_file(
        sentences: str, file_path: str, is_informal: bool=False,
        sep_regex: str=r'([\.\!\?]+[\s])',
        write_mode: Literal['a', 'w', 'x']='x', sep_column: str='\t'
) -> str:
    list_list_conllu = dependency_parsing_multi_sentences(
        sentences, is_informal=is_informal, sep_regex=sep_regex
    )

    return write_conllu(list_list_conllu, file_path,
                        write_mode=write_mode, separator=sep_column)


def __get_default_analyzer() -> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()
