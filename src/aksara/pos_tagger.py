"""This file contains various POS tagging functions"""

import os
from typing import List, Tuple, Literal
from aksara.core import analyze_sentence, split_sentence, sentences_from_file
from aksara.analyzer import BaseAnalyzer
from dependency_parsing.core import DependencyParser
from .utils.conllu_io import _write_reduce_conllu

class POSTagger:
    """
    Class to perform POS Tagging
    """

    __all_input_modes = ["f", "s"]

    def __init__(self) -> None:
        self.analyzer = self.__get_default_analyzer()
        self.dependency_parser = self.__get_default_dependency_parser()

    def tag(
        self,
        input_src: str,
        input_mode: Literal["s", "f"] = "s",
        is_informal: bool = False,
        sep_regex: str = None,
    ) -> List[List[Tuple[str, str]]]:
        """
        Performs POS tagging on the input text, then returns a list of list of tuple containing
        each word in each sentence with its corresponding POS tag as the result

        If `input_mode` is set to 's', `input_src` will refer to the input text.
        Alternatively, if `input_mode` is set to 'f', `input_src` will refer to
        the path to a file containing the text

        Parameters
        ----------
        input_src : str
            text that will be parsed if `input_mode` is set to 's' or
            file path to a file containing the text if `input_mode`
            is set to 'f'

        input_mode : {'f', 's'}, optional
            specifies the source of the input, default is 's'

        is_informal : bool, optional
            assumes the text is informal, default is False

        sep_regex : str, optional
            regex rule that specifies the end of sentence, default is None

        Returns
        -------
        list of list of tuple
            will return list of list of tuple containing each word
            in each sentence with its corresponding POS tag

        Raises
        ------
        ValueError
            if `input_mode` is not in ['f', 's']
        FileNotFoundError
            if `input_mode` is set to 'f' but the referenced file in `input_src` doesn't exist

        Examples
        --------
        >>> from aksara import POSTagger
        >>> tagger = POSTagger()
        >>> text = "Apa yang kamu inginkan?"
        >>> tagger.tag(text)
        [[('Apa', 'PRON'), ('yang', 'SCONJ'), ('kamu', 'PRON'), ('inginkan', 'VERB'), ('?', 'PUNCT')]]

        """

        sentence_list = self.__get_sentence_list(input_src, input_mode, sep_regex)
        result = []
        for sentence in sentence_list:
            analyzed_sentence = self._pos_tag_one_sentence(sentence, is_informal)

            result.append(analyzed_sentence)
        return result

    def tag_to_file(
        self,
        input_src: str,
        write_path: str,
        input_mode: Literal["s", "f"] = "s",
        write_mode: Literal["x", "a", "w"] = "x",
        is_informal: bool = False,
        sep_regex: str = None,
    ) -> str:
        """
        Performs POS tagging on the input text, then saves the result
        in CoNLL-U format in a file specified by `write_path`

        If `input_mode` is set to 's', `input_src` will refer to the input text.
        Alternatively, if `input_mode` is set to 'f', `input_src` will refer to
        the path to a file containing the text

        Parameters
        ----------
        input_src : str
            text that will be parsed if `input_mode` is set to 's' or
            file path to a file containing the text if `input_mode`
            is set to 'f'

        write_path : str
            path to the file where the result will be saved

        input_mode : {'f', 's'}, optional
            specifies the source of the input, default is 's'

        write_mode : {'x', 'a', 'w'}, optional
            mode when writing to the file specified by `write_path`, default is 'x' ::

                'x': create the specified file, throws error FileExistsError if already exists
                'a': append the pos tagging result at the end of the file,
                     create the specified file if not exists
                'w': overwrite the current file content with the pos tagging result,
                     create the specified file if not exists

            NOTE::

                - 'a' write_mode will add '\\n\\n' before the POS tagging result.
                - If you plan to use write_mode 'a' in a file that already contains
                  dependency parsed text in CoNLL-U format, the sent_id between the existing
                  text and the new dependency parsed result will not be in sequence.

        is_informal : bool, optional
            assumes the input text is informal, default is False

        sep_regex : str, optional
            regex rule that specifies the end of sentence, default is None

        Returns
        -------
        str
            absolute path of output file if succesful, null otherwise

        Raises
        ------
        ValueError
            if `input_mode` is not in ['f', 's'],
            if `write_mode` not in ['x', 'a', 'w']
        FileNotFoundError
            if `input_mode` is set to 'f' but the referenced file in `input_src` doesn't exist
        FileExistError
            if `write_mode` is set to 'w' but file already exists

        """

        all_write_modes = ["x", "a", "w"]

        if write_mode not in all_write_modes:
            raise ValueError(f"write_mode must be in {all_write_modes}")

        clean_sentence_list = self.__get_sentence_list(input_src, input_mode, sep_regex)
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

        _write_reduce_conllu(
            clean_sentence_list,
            result,
            write_path,
            write_mode=write_mode,
            separator=sep_regex
        )

        return os.path.abspath(write_path)

    def __get_sentence_list(self, input_str, input_mode, sep_regex) -> List[str]:
        """
        extracts all sentence from input text or file into
        a list of sentence

        If `input_mode` is set to 's', `input_src` will refer to the input text.
        Alternatively, if `input_mode` is set to 'f', `input_src` will refer to
        the path to a file containing the text
        """

        if input_mode == "s":
            return split_sentence(input_str, sep_regex)

        if input_mode == "f":
            return sentences_from_file(input_str, sep_regex)

        raise ValueError(
            f"input_mode must be one of {self.__all_input_modes}, but {input_mode} was given"
        )


    def _pos_tag_one_sentence(
        self, sentence: str, is_informal: bool = False
    ) -> list[tuple[str, str]]:
        """
        performs pos tagging on the text that will be considered as a sentence,
        then returns a list of tuple containing each word with its corresponding
        POS tag as the result
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

    def __get_default_analyzer(self) -> BaseAnalyzer:
        """
        returns a base analyzer instance containing the aksara binary file
        """
        bin_path = os.path.join(os.path.dirname(__file__), "bin", "aksara@v1.2.0.bin")

        return BaseAnalyzer(bin_path)

    def __get_default_dependency_parser(self) -> DependencyParser:
        """
        returns a dependency parser instance from the aksara library
        """
        return DependencyParser()
