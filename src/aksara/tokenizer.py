#!/usr/bin/python3

import re


class BaseTokenizer:
    _whitespace_pattern = r"\s+"
    _tokenize_pattern = r'([0-9]+\-an|[+-]?[0-9]*[,.]?[0-9]+|[A-Z][a-z]\.|(?:[A-Z]+\.)(?:[A-Za-z]+\.){1,}|[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}|(?P<punct>[^\w\s+])(?P=punct)+|@[\w.]+|:[\S](?=\s|$)|:-[\S](?=\s|$)|\w+(?=n\'t)|n\'t|\w+(?=\'[m|s]\s)|\'[m|s]\s|[^\w\s+]|(?:[\w-]{0,}))'

    def __init__(self):
        self.regex = re.compile(self._tokenize_pattern)
        self.whitespace_regex = re.compile(self._whitespace_pattern)

    def tokenize(self, sent):
        stripped_sent = self.whitespace_regex.sub(" ", sent).strip()
        tokens = self.regex.findall(stripped_sent)
        tokens = [token[0] for token in tokens]
        spaceafterflags = self.__getspaceafterflag(tokens)
        tokens = [token for token in tokens if token != '']
        return tokens, spaceafterflags

    def __getspaceafterflag(self, tokens):
        flag = [False for token in tokens if token != '']

        # Iterate over list
        i = 0
        is_whitespace = True
        for token in tokens:
            if token == '':
                is_whitespace = True
            else:
                flag[i] = not is_whitespace
                i += 1
                is_whitespace = False

        return flag[1:] + [False]