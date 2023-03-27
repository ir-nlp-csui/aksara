import codecs
import os
import re

from tqdm import tqdm
from typing import List
from aksara.conllu import ConlluData
from aksara.core import analyze_sentence, get_num_lines
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


def dependency_parsing_input_file(
        input_file: str,
        is_informal: bool = False,
        sep_regex: str = r'([\.\!\?]+[\s])'
) -> List[List[ConlluData]]:

    file = open(input_file, "r")

    sentence_list = []

    with file as infile:
        tqdm_setup = tqdm(
            infile,
            total=get_num_lines(infile.name),
            bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
        )

        for _, line in enumerate(tqdm_setup, 1):
            sentences_inline = re.split(codecs.decode(sep_regex, 'unicode_escape'), line.rstrip())
            for i in range(len(sentences_inline)):
                if i % 2 == 0:
                    sentence_list.append(
                        sentences_inline[i] 
                        + (sentences_inline[i + 1]
                        if i != len(sentences_inline) - 1
                        else "")
                    )
    

    result = []

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser()

    for sentence in sentence_list:
        analyzed_sentence = analyze_sentence(sentence, default_analyzer,
                                             default_dependency_parser, v1=False,
                                             lemma=False, postag=False, informal=is_informal)
        sentence_result = []
        for row in analyzed_sentence.split("\n"):
            idx, form, lemma, upos, xpos, feat, head_id, deprel, _, _ = row.split("\t")
            conllu_data = ConlluData(int(idx), form, lemma, upos, xpos,
                                     feat, int(head_id), deprel)
            sentence_result.append(conllu_data)

        result.append(sentence_result)

    return result


def __get_default_analyzer() -> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()