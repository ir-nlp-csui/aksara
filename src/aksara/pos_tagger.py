"""This file contains various POS tagging functions"""

import os
from warnings import warn
from typing import List, Tuple, Literal
from aksara.core import analyze_sentence, split_sentence, sentences_from_file
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser


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

    def _pos_tag_one_word(self, word: str, is_informal: bool = False) -> str:
        stripped_word = word.strip()

        if stripped_word == "":
            return ""

        # check space
        if stripped_word.find(" ") != -1:
            warn(f'expected a single word input but "{word}" was given')
            return "X"

        analyzed_word = analyze_sentence(
            stripped_word,
            self.analyzer,
            self.dependency_parser,
            v1=False,
            lemma=False,
            postag=True,
            informal=is_informal,
        )

        # check if tokenizer recognize stripped_word as a multi word
        if len(analyzed_word.split("\n")) > 1:
            warn(f'expected a single word input but "{word}" was given')
            return "X"
        _, _, tag = analyzed_word.split("\t")
        return tag

    def _pos_tag_one_sentence(
        self, sentence: str, is_informal: bool = False
    ) -> list[tuple[str, str]]:
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

        all_write_modes = ["x", "a", "w"]

        if write_mode not in all_write_modes:
            raise ValueError(f"write_mode must be in {all_write_modes}")

        sentence_list = split_sentence(text, sep_regex)

        result_list: List[List[Tuple[str, str]]] = self._pos_tag_multi_sentences(
            text, sep_regex=sep_regex, is_informal=is_informal
        )

        header_format = "# sent_id = {}\n# text = {}"

        with open(file_path, write_mode, encoding="utf-8") as output_file:
            if write_mode == "a" and len(result_list) != 0:
                output_file.writelines("\n\n")

            for i, token_with_tag in enumerate(result_list):
                output_file.writelines(
                    header_format.format(str(i + 1), sentence_list[i])
                )

                for idx, (token, tag) in enumerate(token_with_tag):
                    output_file.writelines(f"\n{idx + 1}\t{token}\t{tag}")

                if i < len(result_list) - 1:  # don't add \n at the end of the file
                    output_file.writelines("\n\n")

        return True

    def __get_default_analyzer(self) -> BaseAnalyzer:
        bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")

        return BaseAnalyzer(bin_path)

    def __get_default_dependency_parser(self) -> DependencyParser:
        return DependencyParser()
