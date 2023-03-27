"""This file contains various POS tagging functions"""

import re
import os
import codecs
from typing import List, Tuple, Literal
from tqdm import tqdm
from aksara.core import analyze_sentence, get_num_lines
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


# POS Tagging Satu Kata
# TODO

# POS Tagging Satu Kalimat
def pos_tagging_one_sentence(sentence: str, is_informal: bool = False) -> list[tuple[str, str]]:
    """
        performs pos tagging on the text that will be considered as a sentence,
        then returns a list of tuple containing each word with its corresponding
        POS tag as the result

        parameters
        ----------
        sentece: str
            the sentence that will be analyzed

        is_informal: bool
            tell aksara to treat text as informal one, default to False

        return
        ------
        ReturnType: list[tuple[str, str]]
            will return list of tuple containing each word with its corresponding POS tag
        """

    sentence = str(sentence).strip()

    if sentence == '':
        return []

    analyzer = __get_default_analyzer()
    dependency_parser = __get_default_dependency_parser()

    temp_result = analyze_sentence(
        text=sentence,
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


def tag_multi_sentences(sentences: str, is_informal: bool = False,
                        sep_regex: str = '([.!?]+[\\\s])') -> List[List[Tuple[str, str]]]:
    sentences = sentences.strip()

    if sentences == '':
        return []

    result: List[List[Tuple[str, str]]] = []

    sentence_list = __split_sentence(sentences, sep_regex)

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser()
    for sentence in sentence_list:
        analyzed_sentence = analyze_sentence(sentence, default_analyzer,
                                             default_dependency_parser, v1=False,
                                             lemma=False, postag=True,
                                             informal=is_informal)

        temp_result = []
        for token_with_tag_str in analyzed_sentence.split('\n'):
            _, token, tag = token_with_tag_str.split('\t')

            temp_result.append((token, tag))

        result.append(temp_result)

    return result


# POS Tagging File
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


def __get_default_analyzer() -> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser() -> DependencyParser:
    return DependencyParser()


# POS Tagging File
# TODO


# POS Tagging output file
def tag_then_save_to_file(text: str, file_path: str,
                          sep_regex: str = '([.!?]+[\\\s])',
                          write_mode: Literal['x', 'a', 'w'] = 'w',
                          is_informal: bool = False) -> bool:
    """
    performs pos tagging on the text, then save the result in the file specified by file_path 

    parameters
    ----------
    text: str
        the text that will be analyzed

    file_path: str
        path to the file where the pos tagging result will be saved to

    sep_regex: str
        regex rule that specify end of sentence
        
    write_mode: str, ['x', 'a', 'w'], default to 'w'
        mode while writing on the file specified by file_path

        'x': create the specified file, throws error FileExistsError if already exists
        'a': append the pos tagging result at the end of the file, 
                create the specified file if not exists
        'w': overwrite the current file content with the pos tagging result, 
                create the specified file if not exists

        NOTE:
        - if write_mode not in ['x', 'a', 'w'] will throws ValueError
        - 'a' write_mode will add '\n\n' before the pos tagging result.
        - If you plan to use 'a' write_mode in a file that already has 
            pos taging result on connlu format, the sent_id between 
            the old (already in the file) and new pos tag result will not ne in sequence.

    is_informal: bool
        tell aksara to treat text as informal one, default to False
            
    return
    ------
    ReturnType: bool
        will return true if succesfully pos tag and save the result on the given file_path
    """

    all_write_modes = ['x', 'a', 'w']

    if write_mode not in all_write_modes:
        raise ValueError(f"write_mode must be in {all_write_modes}")

    sentence_list = __split_sentence(text, sep_regex)

    result_list: List[List[Tuple[str, str]]] = tag_multi_sentences(text,
                                                                   sep_regex=sep_regex,
                                                                   is_informal=is_informal)

    header_format = "# sent_id = {}\n# text = {}"

    with open(file_path, write_mode, encoding="utf-8") as output_file:

        if write_mode == 'a' and len(result_list) != 0:
            output_file.writelines('\n\n')

        for i, token_with_tag in enumerate(result_list):
            output_file.writelines(header_format.format(str(i + 1), sentence_list[i]))

            for idx, (token, tag) in enumerate(token_with_tag):
                output_file.writelines(f"\n{idx + 1}\t{token}\t{tag}")

            if i < len(result_list) - 1:  # don't add \n at the end of the file
                output_file.writelines('\n\n')

    return True


def __split_sentence(text: str, sep_regex: str = '([.!?]+[\\\s])') -> List[str]:
    """
    this method will split a multi sentences text based on separator regex (sep_regex)
    
    paramters
    ---------

    text: str
        sentences that will be splitted

    sep_regex: str
        regex rule that determine the points where the text will be splitted at.
    
    return
    ------
    ReturnType: List of string
        splitted text
    """

    splitted_sentences = re.split(codecs.decode(sep_regex, 'unicode_escape'), text)
    sentence_list = []
    for i in range(len(splitted_sentences)):
        if i % 2 == 0:
            sentence_with_end_mark = splitted_sentences[i] + \
                                     (splitted_sentences[i + 1] if i != len(splitted_sentences) - 1 else "")

            sentence_list.append(sentence_with_end_mark)

    return sentence_list
