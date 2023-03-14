"""This file contains various POS tagging function"""

from typing import List, Tuple
import re
import os
import codecs

from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


# POS Tagging Satu Kata
# TODO

# POS Tagging Satu Kalimat
def pos_tagging_one_sentence(input_text: str, is_informal: bool = False) -> list[tuple[str, str]]:
    """This function receives a sentence (containing only a dot) and returns a list of tuple
    containing each word with its corresponding POS tag"""

    input_text = str(input_text).strip()

    punct_pattern = r"[\.\!\?]"
    punct_count = len(re.findall(punct_pattern, input_text))
    punct_index = re.search(punct_pattern, input_text)
    if punct_count != 1 or isinstance(punct_index, type(None)) \
            or punct_index.start() != len(input_text) - 1:
        return [("", "")]

    analyzer = __get_default_analyzer()
    dependency_parser = __get_default_dependency_parser()

    temp_result = analyze_sentence(
        text=input_text,
        analyzer=analyzer,
        dependency_parser=dependency_parser,
        v1=False,
        lemma=False,
        postag=True,
        informal=is_informal
    )

    result = []

    for line in temp_result.split("\n"):
        _, word, postag = line.split("\t")
        result.append((word, postag))

    return result


# POS Tagging Multi-Kalimat
# TODO

def tag_multi_sentences(
        sentences: str,
        is_informal: bool = False,
        sep_regex: str = '([.!?]+[\s])'
) -> List[List[Tuple[str, str]]]:
    sentences = sentences.strip()

    if sentences == '':
        return []

    result: List[List[Tuple[str, str]]] = []

    splitted_sentences = re.split(codecs.decode(sep_regex, 'unicode_escape'), sentences)
    sentence_list = []
    for i in range(len(splitted_sentences)):
        if i % 2 == 0:
            sentence_list.append(
                splitted_sentences[i]
                + (splitted_sentences[i + 1]
                   if i != len(splitted_sentences) - 1
                   else ""))

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser()
    for sentence in sentence_list:
        analyzed_sentence = analyze_sentence(
            sentence,
            default_analyzer,
            default_dependency_parser,
            v1=False,
            lemma=False,
            postag=True,
            informal=is_informal
        )

        temp_result = []
        for token_with_tag_str in analyzed_sentence.split('\n'):
            _, token, tag = token_with_tag_str.split('\t')

            temp_result.append((token, tag))

        result.append(temp_result)

    return result


def __get_default_analyzer() -> BaseAnalyzer:
    current_module_path = os.path.realpath(__file__)
    current_dir_path, _ = os.path.split(current_module_path)
    src_path, _ = os.path.split(current_dir_path)

    bin_path = os.path.join(src_path, 'bin', 'aksara@v1.2.0.bin')
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()


# POS Tagging File
# TODO

