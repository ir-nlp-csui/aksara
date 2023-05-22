"""This file contains various POS tagging functions"""

import os
from typing import List, Tuple, Literal
from aksara.core import analyze_sentence, split_sentence, sentences_from_file
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser
from .utils.sentence_preparator import _preprocess_text
from .utils.conllu_io import _write_reduce_conllu

class POSTagger:
    __all_input_modes = ["f", "s"]

    def __init__(self) -> None:
        self.analyzer = self.__get_default_analyzer()
        self.dependency_parser = self.__get_default_dependency_parser()

    def __get_sentences_string(self, input_str, input_mode, sep_regex) -> str:
        sentences = []
        if input_mode == "s":
            sentences = split_sentence(input_str, sep_regex)
        elif input_mode == "f":
            sentences = sentences_from_file(input_str, sep_regex)
        else:
            raise ValueError(
                f"input_mode must be one of {self.__all_input_modes}, but {input_mode} was given"
            )
        sentences_string = ""
        for i in sentences:
            sentences_string += i + " "

        return sentences_string

    def tag(
        self,
        input_src: str,
        input_mode: Literal["s", "f"] = "s",
        is_informal: bool = False,
        sep_regex: str = None,
    ) -> List[List[Tuple[str, str]]]:
        sentences_string = self.__get_sentences_string(input_src, input_mode, sep_regex)

        return self._pos_tag_multi_sentences(sentences_string, is_informal, sep_regex)

    def tag_to_file(
        self,
        input_src: str,
        write_path: str,
        input_mode: Literal["s", "f"] = "s",
        write_mode: Literal["x", "a", "w"] = "w",
        is_informal: bool = False,
        sep_regex: str = None,
    ) -> str:
        sentences_string = self.__get_sentences_string(input_src, input_mode, sep_regex)

        self._pos_tag_then_save_to_file(
            sentences_string, write_path, sep_regex, write_mode, is_informal
        )

        return write_path

    def _pos_tag_multi_sentences(
        self, sentences: str, is_informal: bool = False, sep_regex: str = None
    ) -> List[List[Tuple[str, str]]]:
        sentences = sentences.strip()

        if sentences == "":
            return []

        result: List[List[Tuple[str, str]]] = []

        sentence_list = split_sentence(sentences, sep_regex)
        for sentence in sentence_list:
            analyzed_sentence = self._pos_tag_one_sentence(sentence, is_informal)

            result.append(analyzed_sentence)

        return result


    def _pos_tag_one_sentence(
        self, sentence: str, is_informal: bool = False
    ) -> list[tuple[str, str]]:
        """
        performs pos tagging on the text that will be considered as a sentence
        """

        sentence = str(sentence).strip()

        if sentence == "":
            return []

        temp_result = analyze_sentence(
            text=sentence,
            analyzer=self.analyzer,
            dependency_parser=self.dependency_parser,
            v1=False,
            lemma=False,
            postag=True,
            informal=is_informal,
        )

        result = []

        for line in temp_result.split("\n"):
            _, word, postag = line.split("\t")
            result.append((word, postag))

        return result

    def _pos_tag_then_save_to_file(
        self,
        text: str,
        file_path: str,
        sep_regex: str = None,
        write_mode: Literal["x", "a", "w"] = "w",
        is_informal: bool = False,
    ) -> bool:
        """
        performs pos tagging on the text, then save the result in the file specified by file_path
        """

        all_write_modes = ["x", "a", "w"]

        if write_mode not in all_write_modes:
            raise ValueError(f"write_mode must be in {all_write_modes}")

        clean_sentence_list = _preprocess_text(text, ssplit=True, sep_regex=sep_regex)

        result = []
        for sentence in clean_sentence_list:
            temp_result = analyze_sentence(
                text=sentence,
                analyzer=self.analyzer,
                dependency_parser=self.dependency_parser,
                v1=False,
                lemma=False,
                postag=True,
                informal=is_informal,
            )

            one_sentence_result = []

            for line in temp_result.split("\n"):
                id_token_tag = line.split("\t")
                one_sentence_result.append(id_token_tag)

            result.append(one_sentence_result)

        _write_reduce_conllu(clean_sentence_list, result, file_path, write_mode=write_mode, separator=sep_regex)

        return True

    def __get_default_analyzer(self) -> BaseAnalyzer:
        bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")

        return BaseAnalyzer(bin_path)

    def __get_default_dependency_parser(self) -> DependencyParser:
        return DependencyParser()
