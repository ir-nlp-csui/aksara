import os

from aksara.core import analyze_sentence
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser

def lemmatization_one_word(word_input: str, is_informal: bool = False) -> str:
    """ 

    performs lemmatization on a word, 

    then returns a string containing its corresponding

    lemma as the result 

 

    parameters 
    ---------- 

    input: str

        the word that will be analyzed

 

    is_informal: bool 

        tell aksara to treat text as informal , default to False 

 

    return 
    ------ 

    ReturnType: str 

        will return string containing each word's lemma

    """
    word_input = word_input.strip()

    if word_input == '':
        return ''

    analyzer = __get_default_analyzer()
    dependency_parser = __get_default_dependency_parser()

    temp_result = analyze_sentence(text=word_input,
                                   analyzer=analyzer,
                                   dependency_parser=dependency_parser,
                                   v1=False,
                                   lemma=True,
                                   postag=False,
                                   informal=is_informal)

    _, _, lemma = temp_result.split("\t")
    result = lemma

    return result


def lemmatization_list(list_word: list[str], is_informal: bool = False) -> list[tuple[str, str]]:
    """ 

    performs lemmatization on the sentence list, 

    then returns a list containing each word paired with its 
    
    corresponding lemma as the result 

 

    parameters 
    ---------- 

    input: list

        the list of words (sentence) that will be analyzed

 

    is_informal: bool 

        tell aksara to treat text as informal , default to False 

 

    return 
    ------ 

    ReturnType: list

        will return list containing each word paired with its
        
        corresponding lemma as the result

    """
    result = []

    if list_word == []:
        return result

    for word in list_word:
        lemma = lemmatization_one_word(word, is_informal)
        result.append((word, lemma))

    return result

def __get_default_analyzer()-> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser()->DependencyParser:
    return DependencyParser()
