"""
Module for aksara dependency parsing feature
"""

import os
import dependency_parsing.core as dep_parser_core

from typing import List, Literal
from aksara.conllu import ConlluData
from aksara.core import analyze_sentence, split_sentence, sentences_from_file
from aksara.analyzer import BaseAnalyzer
from .utils.conllu_io import write_conllu


class DependencyParser:
    __all_models = [
        "FR_GSD-ID_CSUI",
        "FR_GSD-ID_GSD",
        "IT_ISDT-ID_CSUI",
        "IT_ISDT-ID_GSD",
        "EN_GUM-ID_CSUI",
        "EN_GUM-ID_GSD",
        "SL_SSJ-ID_CSUI",
        "SL_SSJ-ID_GSD"
    ]

    __all_input_modes = ["f", "s"]

    def __init__(self):
        self.default_analyzer = self.__get_default_analyzer()

    def __get_sentence_list(self, input_str, input_mode, sep_regex) -> List[str]:
        if input_mode == "s":
            return split_sentence(input_str, sep_regex)

        if input_mode == "f":
            return sentences_from_file(input_str, sep_regex)

        raise ValueError(
            f"input_mode must be one of {self.__all_input_modes}, but {input_mode} was given"
        )

    def parse(
            self, input_src: str,
            input_mode: Literal["f", "s"] = "s",
            is_informal: bool = False,
            sep_regex: str = None,
            model: str = "FR_GSD-ID_CSUI"
    ) -> List[List[ConlluData]]:

        sentence_list = self.__get_sentence_list(input_src.strip(), input_mode, sep_regex)

        if len(sentence_list) == 0:
            return []

        result = []

        for sentence in sentence_list:
            sentence_result = self._parse_one_sentence(
                sentence, is_informal, model
            )
            result.append(sentence_result)

        return result

    def parse_to_file(
            self, input_src: str,
            write_path: str,
            input_mode: Literal["f", "s"] = "s",
            write_mode: Literal['a', 'w', 'x'] = 'x',
            is_informal: bool = False,
            sep_regex: str = None,
            sep_column: str = '\t',
            model: str = "FR_GSD-ID_CSUI"
    ) -> str:
        result = self.parse(
            input_src, input_mode=input_mode, is_informal=is_informal,
            sep_regex=sep_regex, model=model
        )

        return write_conllu(split_sentence(input_src, sep_regex), result, write_path,
                            write_mode=write_mode, separator=sep_column)

    def _parse_one_sentence(
            self, sentence: str,
            is_informal: bool = False,
            model: str = "FR_GSD-ID_CSUI"
    ):
        sentence = sentence.strip()

        if sentence == "":
            return []

        default_dependency_parser = self.__get_default_dependency_parser(model)

        analyzed_sentence = analyze_sentence(
            sentence,
            self.default_analyzer,
            default_dependency_parser,
            v1=False,
            lemma=False,
            postag=False,
            informal=is_informal
        )

        result = []
        for row in analyzed_sentence.split("\n"):
            idx, form, lemma, upos, xpos, feat, head_id, deprel, _, _ = row.split("\t")
            conllu_data = ConlluData(
                idx, form, lemma, upos, xpos, feat, head_id, deprel
            )
            result.append(conllu_data)

        return result

    def __get_default_analyzer(self) -> BaseAnalyzer:
        bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
        return BaseAnalyzer(bin_path)

    def __get_default_dependency_parser(self, model) -> dep_parser_core.DependencyParser:
        if model not in self.__all_models:
            raise ValueError(f"model must be one of {self.__all_models}, but {model} was given")

        return dep_parser_core.DependencyParser(model)
