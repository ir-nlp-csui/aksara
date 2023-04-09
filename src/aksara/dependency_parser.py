"""
Module for aksara dependency parsing feature
"""

import codecs
import os
import re

from typing import List, Literal
from enum import Enum
from tqdm import tqdm
from aksara.conllu import ConlluData
from aksara.core import analyze_sentence, get_num_lines
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser
from .utils.conllu_io import write_conllu


class InputMode(Enum):
    """Enumerate input ode for dependency_parse and dependency_parse_to_file functions"""

    TEXT = "text"
    FILE = "file"


def dependency_parse(
        input_str: str, input_mode: InputMode,
        is_informal: bool = False,
        sep_regex: str = None,
        model: str = "FR_GSD-ID_CSUI"
) -> List[List[ConlluData]]:

    all_input_modes = [InputMode.TEXT, InputMode.FILE]

    if input_mode not in all_input_modes:
        raise ValueError(f"write_mode must be one of {all_input_modes}, but {input_mode} was given")

    all_models = [
        "FR_GSD-ID_CSUI",
        "FR_GSD-ID_GSD",
        "IT_ISDT-ID_CSUI",
        "IT_ISDT-ID_GSD",
        "EN_GUM-ID_CSUI",
        "EN_GUM-ID_GSD",
        "SL_SSJ-ID_CSUI",
        "SL_SSJ-ID_GSD"
    ]

    if model not in all_models:
        raise ValueError(f"model must be one of {all_models}, but {model} was given")

    result = []

    if input_mode == InputMode.TEXT:
        result = _dependency_parse_input_text(
            sentences=input_str,
            is_informal=is_informal,
            sep_regex=sep_regex,
            model=model
        )

    elif input_mode == InputMode.FILE:
        result = _dependency_parse_input_file(
            file_path=input_str,
            is_informal=is_informal,
            sep_regex=sep_regex,
            model=model
        )

    return result


def dependency_parse_to_file(
        input_str: str, input_mode: InputMode, file_path: str,
        is_informal: bool = False,
        sep_regex: str = None,
        write_mode: Literal['a', 'w', 'x'] = 'x', sep_column: str = '\t',
        model: str = "FR_GSD-ID_CSUI"
) -> str:
    result = dependency_parse(
        input_str, input_mode=input_mode,
        is_informal=is_informal, sep_regex=sep_regex, model=model
    )

    return write_conllu(result, file_path,
                        write_mode=write_mode, separator=sep_column)


def _dependency_parse_one_sentence(
        sentence: str,
        is_informal: bool = False,
        model: str = "FR_GSD-ID_CSUI"
) -> List[ConlluData]:
    sentence = sentence.strip()

    if sentence == "":
        return []

    default_analyzer = __get_default_analyzer()
    default_dependency_parser = __get_default_dependency_parser(model)

    analyzed_sentence = analyze_sentence(
        sentence,
        default_analyzer,
        default_dependency_parser,
        v1=False,
        lemma=False,
        postag=False,
        informal=is_informal,
    )

    result = []
    for row in analyzed_sentence.split("\n"):
        idx, form, lemma, upos, xpos, feat, head_id, deprel, _, _ = row.split("\t")
        conllu_data = ConlluData(
            idx, form, lemma, upos, xpos, feat, head_id, deprel
        )
        result.append(conllu_data)

    return result


def _dependency_parse_input_text(
        sentences: str,
        is_informal: bool = False,
        sep_regex: str = None,
        model: str = "FR_GSD-ID_CSUI",
) -> List[List[ConlluData]]:
    sentences = sentences.strip()

    if sentences == "":
        return []

    sentence_list = __split_sentence(sentences, sep_regex)

    result = []
    for sentence in sentence_list:
        sentence_result = _dependency_parse_one_sentence(
            sentence, is_informal=is_informal, model=model
        )
        result.append(sentence_result)

    return result


def _dependency_parse_input_file(
        file_path: str,
        is_informal: bool = False,
        sep_regex: str = None,
        model: str = "FR_GSD-ID_CSUI"
) -> List[List[ConlluData]]:
    result = []

    with open(file_path, "r", encoding="utf-8") as infile:
        tqdm_setup = tqdm(
            infile,
            total=get_num_lines(infile.name),
            bar_format="{l_bar}{bar:50}{r_bar}{bar:-10b}",
        )

        for _, line in enumerate(tqdm_setup, 1):
            sentence_list = __split_sentence(line.rstrip(), sep_regex)
            for sentence in sentence_list:
                sentence_result = _dependency_parse_one_sentence(
                    sentence, is_informal=is_informal, model=model
                )
                result.append(sentence_result)

    return result


def __split_sentence(text: str, sep_regex: str = None) -> List[str]:
    """
    this method will split a multi sentences text based on separator regex (sep_regex)

    parameters
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

    if sep_regex is None:
        sep_regex = r"([.!?]+[\\s])"

    splitted_sentences = re.split(codecs.decode(sep_regex, "unicode_escape"), text)
    sentence_list = []
    for i, sentence in enumerate(splitted_sentences):
        if i % 2 == 0:
            sentence_with_end_mark = sentence + (
                splitted_sentences[i + 1] if i != len(splitted_sentences) - 1 else ""
            )

            sentence_list.append(sentence_with_end_mark)

    return sentence_list


def __get_default_analyzer() -> BaseAnalyzer:
    bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
    return BaseAnalyzer(bin_path)


def __get_default_dependency_parser(model) -> DependencyParser:
    return DependencyParser(model)
