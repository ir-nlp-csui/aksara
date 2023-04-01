from typing import List, Literal
import re
import os

from ..conllu import ConlluData

def read_conllu(file_path: str, separator: str=r'\s+') -> List[List[ConlluData]]:
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


def write_conllu(list_list_conllu: List[List[ConlluData]], file_path: str,
                 write_mode: Literal['a', 'w', 'x'] = 'x', separator: str='\t'
                 ) -> str:

    all_write_modes = ['a', 'w', 'x']

    if write_mode not in all_write_modes:
        raise ValueError(f"write_mode must be one of {all_write_modes}, but {write_mode} was given")

    with open(file_path, mode=write_mode, encoding='utf-8') as file:
        if write_mode == 'a':
            file.writelines('\n')

        for sentence_idx, list_conllu in enumerate(list_list_conllu):
            file.writelines(f'# sent_id = {sentence_idx + 1}\n')

            sentence = " ".join(map(lambda x: x.get_form(), list_conllu))
            file.writelines(f'# text = {sentence}\n')

            for row_idx, conllu in enumerate(list_conllu):
                _, *row = str(conllu).split('\t')
                row_sentence = separator.join(row)
                file.writelines(f"{row_idx + 1}{separator}{row_sentence}\n")

            if sentence_idx < len(list_list_conllu) - 1:
                file.writelines('\n')

    return os.path.realpath(file_path)
