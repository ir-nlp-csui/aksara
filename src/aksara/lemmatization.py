import os

from typing import Union
from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser

# Lemmatization Satu Kata
def lemmatization(input_text: Union[list, str], is_informal: bool = False) -> str:
    """This function receives a certain string or a list 
    and returns lemmatization result of the said word/list"""

    if type(input_text) is str:
        processed_input = input_text.strip()
    else:
        processed_input = ' '.join(input_text)
        result = []

    analyzer = __get_default_analyzer()
    dependency_parser = __get_default_dependency_parser()

    temp_result = analyze_sentence(text=processed_input, analyzer=analyzer,
                     dependency_parser=dependency_parser, v1=False,
                                   lemma=True, postag=False, informal=is_informal)

    if type(input_text) is list :
        for line in temp_result.split("\n"):
            _, word, lemma = line.split("\t")
            result.append((word, lemma))
        return result

    _, _, result = temp_result.split("\t")
    return result

# Lemmatization List
def lemmatization_list(list_word: list, is_informal: bool = False) -> list[tuple[str, str]]:
    """This function receives a list of words and returns a list of tuple
    containing each word with its lemmatization result"""

    input_text = ' '.join(list_word)

    analyzer = __get_default_analyzer()
    dependency_parser = __get_default_dependency_parser()

    temp_result = analyze_sentence(text=input_text, analyzer=analyzer, dependency_parser=dependency_parser, v1=False,
                                   lemma=True, postag=False, informal=is_informal)

    result = []

    for line in temp_result.split("\n"):
        _, word, lemma = line.split("\t")
        result.append((word, lemma))

    return result


def __get_default_analyzer():
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser():
    return DependencyParser()