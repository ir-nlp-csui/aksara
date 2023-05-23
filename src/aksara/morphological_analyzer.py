import os

from typing import List, Literal
from aksara.core import analyze_sentence, sentences_from_file, split_sentence
from aksara.analyzer import BaseAnalyzer
from aksara.utils.conllu_io import _write_reduce_conllu
from dependency_parsing.core import DependencyParser

class MorphologicalAnalyzer:
    """
    Class for aksara morphological analyzer
    """

    __all_input_modes = ["f", "s"]

    def __init__(self):
        self.default_analyzer = self.__get_default_analyzer()
        self.default_dependency_parser = self.__get_default_dependency_parser()

    def __get_sentence_list(self, input_str, input_mode, sep_regex) -> List[str]:
        if input_mode == "s":
            return split_sentence(input_str, sep_regex=sep_regex)

        if input_mode == "f":
            return sentences_from_file(input_str, sep_regex)

        raise ValueError(
            f"input_mode must be one of {self.__all_input_modes}, but {input_mode} was given"
        )

    def analyze(
        self, input_src: str,
        input_mode: Literal["f", "s"] = "s",
        is_informal: bool = False,
        sep_regex: str = None,
    ) -> List[List[tuple[str, str]]]:

        if input_mode == "f" and os.stat(input_src).st_size == 0:
            return []

        sentence_list = self.__get_sentence_list(input_src.strip(), input_mode, sep_regex)

        if len(sentence_list) == 0:
            return []

        result = []

        for sentence in sentence_list:
            sentence_result = self._analyze_one_sentence(sentence, is_informal)
            result.append(sentence_result)

        return result

    def analyze_to_file(
        self, input_src: str,
        write_path: str,
        input_mode: Literal["f", "s"] = "s",
        write_mode: Literal['a', 'w', 'x'] = 'x',
        is_informal: bool = False,
        sep_regex: str = None
    ) -> str:

        all_write_modes = ["x", "a", "w"]

        if write_mode not in all_write_modes:
            raise ValueError(f"write_mode must be in {all_write_modes}")

        sentence_list = self.__get_sentence_list(input_src.strip(), input_mode, sep_regex)

        idx_token_misc = []

        for sentence in sentence_list:
            analyzed_sentence = analyze_sentence(
                        sentence,
                        self.default_analyzer,
                        self.default_dependency_parser,
                        v1=False,
                        lemma=False,
                        postag=False,
                        informal=is_informal
                    )

            result = []
            for row in analyzed_sentence.split("\n"):
                idx, form, _, _, _, _, _, _, _, morf = row.split("\t")

                result.append((idx, form, morf))

            idx_token_misc.append(result)

        _write_reduce_conllu(
            sentence_list,
            idx_token_misc,
            write_path,
            write_mode=write_mode,
            separator=sep_regex
        )

        return os.path.realpath(write_path)

    def _analyze_one_sentence(
        self, sentence: str,
        is_informal: bool = False
    ) -> List[tuple[str, str]]:

        sentence = sentence.strip()

        analyzed_sentence = analyze_sentence(
            sentence,
            self.default_analyzer,
            self.default_dependency_parser,
            v1=False,
            lemma=False,
            postag=False,
            informal=is_informal
        )

        result = []
        for row in analyzed_sentence.split("\n"):
            _, form, _, _, _, _, _, _, _, morf = row.split("\t")

            result.append((form, morf))

        return result

    def __get_default_analyzer(self) -> BaseAnalyzer:
        bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")
        return BaseAnalyzer(bin_path)

    def __get_default_dependency_parser(self) -> DependencyParser:
        return DependencyParser()
