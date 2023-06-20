import os

from typing import List, Literal
from ._nlp_internal import _get_foma_script_path, TextNormalizer
from ._nlp_internal.core import analyze_sentence
from ._nlp_internal.analyzer import BaseAnalyzer
from ._nlp_internal.core import DependencyParser

from .utils.conllu_io import _write_reduce_conllu
from .utils.sentence_util import _get_sentence_list

class MorphologicalAnalyzer:
    """
    Class to get all morphological analysis
    """

    def __init__(self):
        self.default_analyzer = BaseAnalyzer(_get_foma_script_path(), TextNormalizer())
        self.default_dependency_parser = DependencyParser()

    def analyze(
        self, input_src: str,
        input_mode: Literal["f", "s"] = "s",
        is_informal: bool = False,
        sep_regex: str = None,
    ) -> List[List[tuple[str, str]]]:
        """
        Get all morphological analysis in `input_src`

        Parameters
        ----------
        input_src: str
            Python string or file path that contains Indonesian text
        input_mode: {'f', 's'}, default='s'
            's' mode : `input_src` is assumed to be a Python str.
            'f' mode : `input_src` is processed as a file path.
        is_informal: bool, default=False
            Processes text in `input_src` as informal text or not 
            (default treat text as formal text)
        sep_regex: str, optional
            Regex that will be used to split a multi sentences text 
            into a list of single sentence

        Returns
        -------
        list of list of tuple
            The inner list contains a pair of token and its morphological analysis for
            one sentence in the `input_src`.

        Raises
        ------
        FileNotFoundError
            if `input_mode` is set to 'f' but file in `input_src` doesn't exist
        ValueError
            if `input_mode` is not in ['f', 's']

        Examples
        --------
        >>> from aksara import MorphologicalAnalyzer
        >>> analyzer = MorphologicalAnalyzer()
        >>> analyzer.analyze('Andi tidur')
        [[('Andi', 'Morf=Andi<PROPN>_PROPN'), ('tidur', 'Morf=tidur<VERB>_VERB')]]

        """

        if input_mode == "f" and os.stat(input_src).st_size == 0:
            return []

        sentence_list = _get_sentence_list(input_src.strip(), input_mode, sep_regex)

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
        """
        Get all morphological analysis in `input_src` and save the result in a file

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
            Processes text in `input_src` as informal text or not 
            (default treat text as formal text)
        sep_regex: str, optional
            Regex that will be used to split a multi sentences text into a list of single sentence

        Returns
        -------
        str
            The absolute path of `write_path`.

        Raises
        ------
        FileNotFoundError
            if `input_mode` is set to 'f' but file in `input_src` doesn't exist
        FileExistError
            if `write_mode` is set to 'x' but file already exists
        ValueError
            if `write_mode` not in ['x', 'a', 'w'],
            also if `input_mode` not in ['f', 's']

        """

        all_write_modes = ["x", "a", "w"]

        if write_mode not in all_write_modes:
            raise ValueError(f"write_mode must be in {all_write_modes}")

        sentence_list = _get_sentence_list(input_src.strip(), input_mode, sep_regex)

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
