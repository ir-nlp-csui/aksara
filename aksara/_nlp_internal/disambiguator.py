#!/usr/bin/python3

from .disambiguation.hmmlearn import HMMLearn
from .disambiguation.hmmdecode import HMMDecode


class Disambiguator:

    def __init__(self):
        self.__hmmlearn = HMMLearn(trigram=True)
        self.__hmmdecode = HMMDecode(hmm=self.__hmmlearn, log=True)

    def disambiguate(self, rows):
        sentences = []
        tags = []
        for row in rows:
            sentences.append(row[1])
            tags.append(row[3])

        predicted_tags = self.__hmmdecode.decode(sentences, tags)
        new_rows = []
        for i in range(len(rows)):
            row = rows[i]
            temp = row.copy()
            lemmas = temp[2].split("/")
            tags = temp[3].split("/")
            features = temp[5].split("/")
            misc = temp[9].split("/")
            if len(tags) > 1:
                for j in range(len(tags)):
                    if tags[j] == predicted_tags[i]:
                        temp[2] = lemmas[j]
                        temp[3] = tags[j]
                        temp[9] = misc[j]
                        for feature in features:
                            temp[5] = "_"
                            if tags[j] in feature:
                                idx = feature.find("->")
                                temp[5] = feature[idx+3:-1]
                                break

                        break

            new_rows.append(temp)

        return new_rows
