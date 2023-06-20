#!/usr/bin/python3
from tempfile import NamedTemporaryFile
from tqdm import tqdm

import argparse
import mmap
import re

from .tokenizer import (
    BaseTokenizer,
)

from .formatter import (
    to_conllu_line,
    to_conllu_line_with_range,
)

from .analyzer import (
    BaseAnalyzer,
)

from .parser import (
    parse,
)

from .disambiguator import (
    Disambiguator
)

from .dependency_parsing.core import DependencyParser

HEADER = """# sent_id = {}
# text = {}
"""

HELP_MSG = {
    'string': 'text string',
    'file': 'input file',
    'output': 'output file',
    'lemma': 'only output lemmatization result',
    'postag': 'only output POS tagging result',
    'informal': 'to use informal rule beside the formal rule',
    'model': 'set dependency parser model (default: FR_GSD-ID_CSUI)',
}

base_tokenizer = BaseTokenizer()
disambiguator = Disambiguator()

def analyze_sentence(text, analyzer, dependency_parser, **kwargs):
    surface, SANflags = base_tokenizer.tokenize(text)
    tokens = surface[:]
    flag = dict()

    for key, value in kwargs.items():
        flag[key] = value

    # lowercase first word
    word_pattern = re.compile(r"[^\w\s+]")
    first_word_idx = 0
    while first_word_idx < len(tokens) and word_pattern.match(tokens[first_word_idx]):
        first_word_idx += 1

    # Analyze lemma
    lemma = []
    for i, token in enumerate(tokens):
        temp = token
        if i == first_word_idx:
            temp = token.lower()

        if flag["informal"]:
            temp = "@informal" + temp
        
        analysis = analyzer.analyze(temp)
        if i == first_word_idx and re.match(r'([A-Za-z]+)(\+X)', analysis):
            analysis = analyzer.analyze(token)
        
        lemma.append(analysis)
     
    rows = []
    line_id = 1

    for i in range(len(tokens)):
        temp_lemma = lemma[i].split("\\n")
        temp_lemma = filter(lambda x: x != '', temp_lemma)
        temp_lemma = [temp.split('_') for temp in temp_lemma]
        tmp = []

        # Filter different length lemmas, please handle this case in the future
        min_length = min([len(e) for e in temp_lemma])
        temp_lemma = list(filter(lambda x: len(x) == min_length, temp_lemma))
        
        for j in range(len(temp_lemma[0])):
            merged = [temp_lemma[k][j] for k in range(len(temp_lemma))]
            tmp.append("\\n".join(merged))
        temp_lemma = tmp

        # temp_lemma = lemma[i].split('_')
        temp_surface = surface[i]
        unsuffixed_pattern = ['PRON', 'DET']

        if len(temp_lemma) == 2:
            is_in_front = any([pattern in temp_lemma[0] for pattern in unsuffixed_pattern])
            split_point = 0

            if is_in_front:
                split_point = len(temp_lemma[0].split("+")[0])
            else:
                split_point = -len(temp_lemma[1].split("+")[0])
            
            temp_surface = [temp_surface[:split_point], temp_surface[split_point:]]
        else:
            temp_surface = [temp_surface]
        
        # Add full word line, if splitted
        n_tokens = len(temp_surface)
        if n_tokens > 1:
            new_row = to_conllu_line_with_range(line_id, surface[i], n_tokens)
            rows.append(new_row)
        
        # Add word line(s)
        for j in range(n_tokens):
            new_row = ""
            if j == n_tokens - 1:
                new_row = to_conllu_line(line_id, temp_surface[j], temp_lemma[j], space_after=SANflags[i])
            else:
                new_row = to_conllu_line(line_id, temp_surface[j], temp_lemma[j])
            rows.append(new_row)
            line_id += 1

    parsed_rows = parse(rows)
    if flag["v1"]:
        parsed_rows = dependency_parser.parse_rows(parsed_rows)
        if flag["lemma"] or flag["postag"]:
            return '\n'.join(get_lemma_or_postag(parsed_rows, flag["lemma"], flag["postag"]))
        else:
            return '\n'.join(rows)
    else:
        disambiguated_rows = disambiguator.disambiguate(parsed_rows)
        disambiguated_rows = dependency_parser.parse_rows(disambiguated_rows)
        if flag["lemma"] or flag["postag"]:
            return '\n'.join(get_lemma_or_postag(disambiguated_rows, flag["lemma"], flag["postag"]))
        else:
            return '\n'.join(['\t'.join(row) for row in disambiguated_rows])


def create_args_parser(bin_file):
    parser = argparse.ArgumentParser(description="Aksara")

    # Add a required, positional argument for the input data file name,
    # and open in 'read' mode
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-s", "--string", type=str, help=HELP_MSG['string'])
    input_group.add_argument("-f", "--file", type=argparse.FileType('r'), help="input file")

    # Add optional arguments
    # open in 'write' mode and and specify encoding
    parser.add_argument('--output', type=argparse.FileType('w', encoding='UTF-8'), help="")
    parser.add_argument('--v1', action='store_true')
    parser.add_argument('--lemma', action='store_true', help=HELP_MSG['lemma'])
    parser.add_argument('--postag', action='store_true', help=HELP_MSG['postag'])
    parser.add_argument('--informal', action='store_true', help=HELP_MSG['informal'])
    parser.add_argument('--model', type=str, help=HELP_MSG['model'])
    
    args = parser.parse_args()
    analyzer = BaseAnalyzer(bin_file)
    if args.model:
        dependency_parser = DependencyParser(args.model)
    else:
        dependency_parser = DependencyParser()

    output = ""
    if args.file:
        with args.file as infile:
            print("Processing inputs...")
            tqdm_setup = tqdm(
                infile,
                total=get_num_lines(infile.name),
                bar_format='{l_bar}{bar:50}{r_bar}{bar:-10b}'
            )
            idx_sentence = 1
            for i, line in enumerate(tqdm_setup, 1):
                text = line.rstrip()
                temp = re.split(r'([.!?]+[\s])', text)
                sentences = []
                for i in range(len(temp)):
                    if(i % 2 == 0):
                        sentences.append(temp[i] + (temp[i + 1] if i != len(temp) - 1 else ""))

                for j in range(len(sentences)):
                    temp = analyze_sentence(sentences[j], analyzer, dependency_parser, v1=args.v1, lemma=args.lemma, postag=args.postag, informal=args.informal)
                    output += HEADER.format(str(idx_sentence), sentences[j], '')
                    output += temp + '\n\n'
                    idx_sentence += 1
    else:
        text = args.string
        temp = re.split(r'([.!?]+[\s])', text)
        sentences = []
        for i in range(len(temp)):
            if(i % 2 == 0):
                sentences.append(temp[i] + (temp[i + 1] if i != len(temp) - 1 else ""))
                
        for i in range(len(sentences)):
            output += HEADER.format(str(i + 1), sentences[i], '')
            output += analyze_sentence(sentences[i], analyzer, dependency_parser, v1=args.v1, lemma=args.lemma, postag=args.postag, informal=args.informal)
            output += '\n\n'
        # output += '\n'.join(output)

    output = output.rstrip()
    if args.output:
        args.output.writelines(output)
    else:
        print(output)

def get_num_lines(file_path):
    fp = open(file_path, "r+", encoding="utf-8")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    fp.close()
    return lines


def get_lemma_or_postag(rows, lemma, postag):
    new_rows = []
    for row in rows:
        temp = [row[0], row[1]]
        if lemma: temp.append(row[2])
        if postag: temp.append(row[3])
        new_rows.append(temp)

    return ["\t".join(row) for row in new_rows]
