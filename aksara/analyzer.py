#!/usr/bin/python3

from tempfile import NamedTemporaryFile

import os
import re
import subprocess


# BIN_FILE = "bin/umabi@v1.0.3.bin"


class BaseAnalyzer:

    def __init__(self, bin_file):
        self.__bin_file = bin_file

    def __get_analysis(self, word):
        temp_file = NamedTemporaryFile(delete=True)
        with open(temp_file.name, 'w', encoding="utf-8") as f:
            f.write("load " + self.__bin_file + "\n")
            f.write("apply up " + word)

        os.chmod(temp_file.name, 777)
        temp_file.file.close()
        out = subprocess.check_output(['foma', '-q', '-f', temp_file.name])
        return repr(out)[2:-1]

    def analyze(self, word):
        # Get lemma from Foma
        analysis = self.__get_analysis(word)
        analysis = analysis[:-2]  # Remove most right \n

        if analysis == '???':
            analysis = self.__analyze_unknown(word)

        analysis = list(set(analysis.split("\\n")))
        return "\\n".join(analysis)

    def __trim_analysis(self, analysis):
        # Remove the clitics
        temp = analysis.split("+_")[-1]  # Remove proclitic
        temp = temp.split("_+")[0]  # Remove enclitic
        return temp.split("+")

    def __get_postag(self, text):
        return self.__trim_analysis(text)[1]

    def __get_lemma(self, text):
        return self.__trim_analysis(text)[0]

    def __analyze_redup(self, surface):
        # Regex pattern
        redup_pattern = r'^([a-z]+)(\-)([a-z]+)$'

        # Setting up
        redup_search = re.search(redup_pattern, surface, re.IGNORECASE)
        if not redup_search:
            return "???"
        first_word = redup_search.group(1)
        second_word = redup_search.group(3)

        # Get analysis for each word
        first_word_analysis = self.__get_analysis(first_word)[:-2]
        second_word_analysis = self.__get_analysis(second_word)[:-2]

        if first_word_analysis == "???":
            return "???"

        # Write up results
        new_analysis = ""
        new_postag = ""
        if self.__get_lemma(first_word_analysis) == self.__get_lemma(second_word_analysis):
            new_postag = self.__get_postag(first_word_analysis)
            new_analysis = first_word_analysis
        elif second_word_analysis == "???":
            new_postag = self.__get_postag(first_word_analysis)
            new_analysis = first_word_analysis
        else:
            return "???"

        if new_postag == "NOUN":
            new_analysis = re.sub(r'(?<=\+Number=)Sing', 'Plur', new_analysis)

        return new_analysis

    def __analyze_unknown(self, surface):
        # Regex pattern
        redup_pattern = re.compile(r'([a-z]+)(\-)([a-z]+)')
        proper_noun_pattern = re.compile(r'[A-Z]+[a-z]*')
        punct_pattern = re.compile(r'[“”,.?!()—":\'(\-\-)\-]')
        sym_pattern = re.compile(r'[^\w“”,.?!()—":\'(\-\-)\-]')

        # Word list
        proper_noun_lst = ['of', 'the', "n't", "'s", "'m"]

        # Check every pattern
        analysis = "???"

        if redup_pattern.match(surface):
            analysis = self.__analyze_redup(surface)

        if analysis != "???":
            return analysis

        postag = "X"
        if proper_noun_pattern.match(surface):
            postag = 'PROPN'
        elif surface in proper_noun_lst:
            postag = 'PROPN'
        elif punct_pattern.match(surface):
            postag = "PUNCT"
        elif sym_pattern.match(surface):
            postag = "SYM"

        analysis = "".join([surface, "+", postag])
        analysis += self.__get_feature_tags(analysis, postag)
        return analysis

    def __get_feature_tags(self, analysis, postag):
        tags = []

        if postag == "X":
            tags.append("Foreign=Yes")

        # Add first plus sign
        tags = "+".join(sorted(tags))
        if tags:
            tags = "+" + tags

        return tags