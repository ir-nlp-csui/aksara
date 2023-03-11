from typing import List, Tuple
import re
import os

from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser
import codecs


# POS Tagging Satu Kata
# TODO

# POS Tagging Satu Kalimat
# TODO

# POS Tagging Multi-Kalimat
# TODO

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

    current_module_path = os.path.realpath(__file__)
    current_dir_path, _ = os.path.split(current_module_path)
    src_path, _ = os.path.split(current_dir_path)

    bin_path = os.path.join(src_path, 'bin', 'aksara@v1.2.0.bin')
    return BaseAnalyzer(bin_path)

def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()

# POS Tagging File
# TODO
