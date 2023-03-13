from typing import List, Tuple
from tqdm import tqdm
import re
import os

from aksara.core import analyze_sentence, get_num_lines
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser
import codecs

def pos_tagging_file(
    input_file: str, is_informal: bool = False
) -> list[list[tuple[str]]]:
    result = []

    analyzer = __get_default_analyzer()
    dependency_parser = __get_default_dependency_parser()

    file = open(input_file, "r")

    with file as infile:
        tqdm_setup = tqdm(
            infile,
            total=get_num_lines(infile.name),
            bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
        )

        for _, line in enumerate(tqdm_setup, 1):
            sentences_inline = re.split(r"([.!?]+[\s])", line.rstrip())
            sentences = []
            for i in range(len(sentences_inline)):
                if i % 2 == 0:
                    sentences.append(
                        sentences_inline[i]
                        + (
                            sentences_inline[i + 1]
                            if i != len(sentences_inline) - 1
                            else ""
                        )
                    )

            for j in range(len(sentences)):
                analyzed_sentence = []
                analyzed = analyze_sentence(
                    sentences[j],
                    analyzer,
                    dependency_parser,
                    v1=False,
                    lemma=False,
                    postag=True,
                    informal=is_informal,
                )
                for token in analyzed.split("\n"):
                    _, word, postag = token.split("\t")
                    analyzed_sentence.append((word, postag))

                result.append(analyzed_sentence)

    file.close()

    return result

def tag_multi_sentences(sentences: str, is_informal: bool= False, sep_regex: str = '([.!?]+[\s])') -> List[List[Tuple[str, str]]]:

    sentences = sentences.strip()

    if sentences == '':
        return []

    result: List[List[Tuple[str, str]]] = []

    splitted_sentences = re.split(codecs.decode(sep_regex, 'unicode_escape'), sentences)
    sentence_list = []
    for i in range(len(splitted_sentences)):
        if i % 2 == 0:
            sentence_list.append(splitted_sentences[i] + (splitted_sentences[i + 1] if i != len(splitted_sentences) - 1 else ""))

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser()
    for sentence in sentence_list:
        analyzed_sentence = analyze_sentence(sentence, default_analyzer, default_dependency_parser, v1=False, lemma=False,
                                    postag=True, informal=is_informal)
        
        temp_result = []
        for token_with_tag_str in analyzed_sentence.split('\n'):

            _, token, tag = token_with_tag_str.split('\t')

            temp_result.append((token, tag))

        result.append(temp_result)

    return result

def __get_default_analyzer() -> BaseAnalyzer:
    bin_path = os.path.join(
        os.path.join(os.path.dirname(__file__), ".."), "bin/aksara@v1.2.0.bin"
    )

    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()
