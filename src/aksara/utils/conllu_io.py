from typing import Any, List, Literal, Tuple
import re
import os

from ..conllu import ConlluData

def read_conllu(file_path: str, separator: str=r'\s+') -> List[List[ConlluData]]:
    """
    Read CoNNL-U format file.

    Parameters
    ----------
    file_path: str
        the path of file containing CoNNL-U data
    
    separator: str
        Regex separator between 2 columns in CoNNL-U, default to one or more whitespaces.
    
    Returns
    -------
    list of list of :class:`ConnluData`
        The inner list contains CoNNL-U rows for one sentence.

    """

    conllu_result = []
    with open(file_path, encoding='utf-8') as conllu_file:
        next_sentence = conllu_file.readline()
        while next_sentence != '':

            # next_line currently is '# sent_id = ...'
            conllu_file.readline()  #  '# read text = ...'

            one_sentence_result = []
            next_line = conllu_file.readline()
            while next_line not in ['', '\n']:
                conllu_attrs= re.split(separator, next_line)
                one_sentence_result.append(ConlluData(*conllu_attrs[:8]))
                next_line = conllu_file.readline()

            conllu_result.append(one_sentence_result)
            next_sentence = conllu_file.readline()

    return conllu_result


def write_conllu(list_sentences: List[str], list_list_conllu: List[List[ConlluData]],
                 file_path: str, write_mode: Literal['a', 'w', 'x'] = 'x', separator: str='\t'
                 ) -> str:
    """
    Write list of list of :class:`ConnluData` of an Indonesian text to a file.

    If we have a detokenizer, we may drop list_sentences argument.
    """

    all_write_modes = ['a', 'w', 'x']

    if write_mode not in all_write_modes:
        raise ValueError(f"write_mode must be one of {all_write_modes}, but {write_mode} was given")

    if len(list_sentences) != len(list_list_conllu):
        raise ValueError("list_sentences length must be equal with list_list_conllu length")

    if separator is None:
        separator = '\t'

    with open(file_path, mode=write_mode, encoding='utf-8') as file:
        if write_mode == 'a':
            file.writelines('\n')

        for idx, (sentence, list_conllu) in enumerate(zip(list_sentences, list_list_conllu)):
            file.writelines(f'# sent_id = {idx + 1}\n')

            sentence = sentence.strip()
            file.writelines(f'# text = {sentence}\n')

            for conllu in list_conllu:
                row = str(conllu).split('\t')
                row_sentence = separator.join(row)
                file.writelines(f"{row_sentence}\n")

            if idx < len(list_list_conllu) - 1:
                file.writelines('\n')

    return os.path.realpath(file_path)

def _write_reduce_conllu(
        list_sentences: List[str],
        list_list_conllu: List[List[Tuple[str, str, Any]]],
        file_path: str,
        write_mode:Literal['a', 'w', 'x']='x',
        separator='\t'):
    """
    Write 3 columns of CoNNL-U (idx, form, another column) in a file.

    ``list_list_conllu`` represents the conllu for each sentence in ``list_sentences``.

    If we have a detokenizer, we may drop list_sentences argument.
    """

    if len(list_sentences) != len(list_list_conllu):
        raise ValueError("list_sentences length must be equal with list_list_conllu length")

    if separator is None:
        separator = '\t'

    with open(file_path, mode=write_mode, encoding='utf-8') as file:
        if write_mode == 'a':
            file.writelines('\n')

        sentence_with_conllu = zip(list_sentences, list_list_conllu)
        for sentence_idx, (sentence, list_conllu) in enumerate(sentence_with_conllu):
            file.writelines(f'# sent_id = {sentence_idx + 1}\n')

            sentence = sentence.strip()

            file.writelines(f'# text = {sentence}\n')

            for idx, form, conllu_col in list_conllu:
                file.writelines(f"{idx}{separator}{form}{separator}{conllu_col}\n")

            if sentence_idx < len(list_list_conllu) - 1:
                file.writelines('\n')
