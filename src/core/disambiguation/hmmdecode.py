import math
import os, sys
from .hmmlearn import HMMLearn

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


class HMMDecode:

    def __init__(self, hmm, log=False):
        self.hmm = hmm
        self.log = log

    def decode(self, sentence, tags=None):
        if tags is not None:
            tags = [s.split("/") for s in tags]
        else:
            tags = [self.hmm.TAGS for _ in range(len(sentence))]

        if self.hmm.trigram:
            return self.__decode_trigram(sentence, tags)
        else:
            return self.__decode_bigram(sentence, tags)

    def __decode_bigram(self, sentence, tags):
        viterbi_tag = {}
        viterbi_backpointer = {}
        if len(tags[0]) == 1:
            tag = tags[0][0]
            if self.log:
                viterbi_tag[tag] = 0.0
            else:
                viterbi_tag[tag] = 1.0
            viterbi_backpointer[tag] = "START"
        else:
            for tag in tags[0]:
                if self.log:
                    viterbi_tag[tag] = math.log(self.hmm.get_transition_prob(tag, "START")) + \
                                       math.log(self.hmm.get_emission_prob(sentence[0], tag))
                else:
                    viterbi_tag[tag] = self.hmm.get_transition_prob(tag, "START") * \
                                       self.hmm.get_emission_prob(sentence[0], tag)
                viterbi_backpointer[tag] = "START"

        viterbi_main = []
        backpointer_main = []

        viterbi_main.append(viterbi_tag)
        backpointer_main.append(viterbi_backpointer)
        return self.__viterbi(sentence, tags, viterbi_main, backpointer_main)

    def __decode_trigram(self, sentence, tags):
        viterbi_tag = {}
        viterbi_backpointer = {}
        if len(tags[0]) == 1:
            tag = tags[0][0]
            if self.log:
                viterbi_tag[tag] = 0.0
            else:
                viterbi_tag[tag] = 1.0
            viterbi_backpointer[tag] = ("END", "START")
        else:
            for tag in tags[0]:
                if self.log:
                    viterbi_tag[tag] = math.log(self.hmm.get_transition_prob(tag, ("END", "START"))) + \
                                       math.log(self.hmm.get_emission_prob(sentence[0], tag))
                else:
                    viterbi_tag[tag] = self.hmm.get_transition_prob(tag, ("END", "START")) * \
                                       self.hmm.get_emission_prob(sentence[0], tag)
                viterbi_backpointer[tag] = ("END", "START")

        viterbi = []
        backpointer = []

        viterbi.append(viterbi_tag)
        backpointer.append(viterbi_backpointer)
        return self.__viterbi(sentence, tags, viterbi, backpointer)

    def __viterbi(self, sentence, tags, viterbi, backpointer):
        N = len(sentence)
        for index in range(1, N):
            cur_viterbi = {}
            cur_backpointer = {}
            prev_viterbi = viterbi[-1]

            if len(tags[index]) == 1:
                prev_best = max(prev_viterbi.keys(), key=lambda prevtag: prev_viterbi[prevtag])
                tag = tags[index][0]
                cur_viterbi[tag] = prev_viterbi[prev_best]
                cur_backpointer[tag] = prev_best
            else:
                for tag in tags[index]:
                    prev_best = max(prev_viterbi.keys(),
                                    key=lambda prev_tag: \
                                        self.__calculate_viterbi_value(
                                            prev_viterbi[prev_tag],
                                            self.hmm.get_transition_prob(tag, prev_tag),
                                            self.hmm.get_emission_prob(sentence[index], tag)))

                    cur_viterbi[tag] = self.__calculate_viterbi_value\
                        (prev_viterbi[prev_best],
                         self.hmm.get_transition_prob(tag, prev_best),
                         self.hmm.get_emission_prob(sentence[index], tag))
                    cur_backpointer[tag] = prev_best

            viterbi.append(cur_viterbi)
            backpointer.append(cur_backpointer)

        prev_viterbi = viterbi[-1]
        prev_best = max(prev_viterbi.keys(),
                        key=lambda prev_tag: self.__calculate_viterbi_value(
                            prev_viterbi[prev_tag],
                            self.hmm.get_transition_prob("END", prev_tag),
                            1.0
                        ))

        # print("viterbi:")
        # print(viterbi)
        # print("backpointer:")
        # print(backpointer)
        # prob_tag_sequence = prev_viterbi[prev_best] * self.hmm.get_transition_prob("END", prev_best)
        # print("prob_tag_sequence: ", prob_tag_sequence)

        best_tag_sequence = ["END", prev_best]
        backpointer.reverse()

        current_best_tag = prev_best
        for pointer in backpointer:
            best_tag_sequence.append(pointer[current_best_tag])
            current_best_tag = pointer[current_best_tag]

        best_tag_sequence.reverse()
        return best_tag_sequence[1:-1]

    def __calculate_viterbi_value(self, prev_prob, trans_prob, emission_prob):
        if self.log:
            return prev_prob + math.log(trans_prob) + math.log(emission_prob)
        else:
            return prev_prob * trans_prob * emission_prob


if __name__ == "__main__":
    hmmlearn = HMMLearn(trigram=True)
    sample_sentence = ["Mereka", "membaca", "banyak", "sekali", "buku", "."]
    sample_tags = ["VERB/PRON", "VERB", "DET/ADJ", "DET/ADV", "NOUN", "PUNCT"]
    hmmdecode = HMMDecode(hmmlearn, log=True)
    best_tag = hmmdecode.decode(sample_sentence)
    print(best_tag)
