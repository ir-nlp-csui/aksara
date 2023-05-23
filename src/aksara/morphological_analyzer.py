import os

from typing import List, Literal
from aksara.core import analyze_sentence, split_sentence, sentences_from_file
from aksara.analyzer import BaseAnalyzer
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
            return split_sentence(input_str, sep_regex)

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

        if len(sentence_list) == 1 and sentence_list[0] == "":
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
        """
        Get all morphological features in `input_src` and saved the result in a file

        Parameters
        ----------
        input_src: str
            Python string or file path that contains Indonesian text
        write_path: str
            The file path at which the result will be saved
        input_mode: {'f', 's'}, default='s'
            's' mode : `input_src` is assumed to be a Python str.
            'f' mode : `input_src` is processed as a file path
        write_mode: {'a', 'w', 'x'}, default='x'
            'a': append to the old content of `file_path`.
            'w': overwrite `file_path`.
            'x': write only if `file_path` is not existed.
        is_informal: bool, default=False
            Processes text in `input_src` as informal text or not (default treat text as formal text)
        sep_regex: str, optional
            Regex that will be used to split a multi sentences text into a list of single sentence 

        Returns
        -------
        str
            The absolute path of `write_path`.

        """

        all_write_modes = ["x", "a", "w"]

        if write_mode not in all_write_modes:
            raise ValueError(f"write_mode must be in {all_write_modes}")

        sentence_list = self.__get_sentence_list(input_src.strip(), input_mode, sep_regex)
        analyzed_text = self.analyze(input_src, input_mode, is_informal, sep_regex)

        with open(write_path, write_mode, encoding="utf-8") as output_file:
            if write_mode == "a" and len(analyzed_text) != 0:
                output_file.writelines("\n\n")

            for i, sentence_morf in enumerate(analyzed_text):
                output_file.writelines(
                    f"# sent_id = {str(i + 1)}\n# text = {sentence_list[i]}")

                for idx, (form, morf) in enumerate(sentence_morf):

                    output_file.writelines(f"\n{idx + 1}\t{form}\t{morf}")

                if i < len(analyzed_text) - 1:  # don't add \n at the end of the file
                    output_file.writelines("\n\n")

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
