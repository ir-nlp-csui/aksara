import os

from typing import Union
from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser

# Lemmatization Satu Kata
def lemmatization(input: Union[list, str], is_informal: bool = False) -> Union[list,str]:
    """ 

    performs lemmatization on the text or sentence, 

    then returns a list or sentence containing its corresponding

    lemma as the result 

 

    parameters 
    ---------- 

    input: list | str

        the word/list of words (sentence) that will be analyzed

 

    is_informal: bool 

        tell aksara to treat text as informal , default to False 

 

    return 
    ------ 

    ReturnType: list | str 

        will return string/list containing each word's lemma

    """ 

    if isinstance(input, str):
        if input == '':
            return ''
        processed_input = input.strip()
    else:
        if input == []:
            return []
        processed_input = ' '.join(input)
        result = []

    analyzer = __get_default_analyzer()
    dependency_parser = __get_default_dependency_parser()

    temp_result = analyze_sentence(text=processed_input,
                                   analyzer=analyzer,
                                   dependency_parser=dependency_parser,
                                   v1=False,
                                   lemma=True,
                                   postag=False,
                                   informal=is_informal)

    if isinstance(input,list):
        for line in temp_result.split("\n"):
            _, word, lemma = line.split("\t")
            result.append((word, lemma))
        return result

    _, _, result = temp_result.split("\t")
    return result

def __get_default_analyzer()-> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser()->DependencyParser:
    return DependencyParser()
