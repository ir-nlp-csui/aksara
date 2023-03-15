import os

from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser

# Lemmatization Satu Kata
def lemmatization_list(list_word: list, is_informal: bool = False) -> list[tuple[str, str]]:
    """This function receives a certain word and returns a list of tuple
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
    current_module_path = os.path.realpath(__file__)
    current_dir_path, _ = os.path.split(current_module_path)
    src_path, _ = os.path.split(current_dir_path)

    bin_path = os.path.join(src_path, 'bin', 'aksara@v1.2.0.bin')
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser():
    return DependencyParser()
