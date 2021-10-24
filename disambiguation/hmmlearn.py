import nltk


class HMMLearn:

    N = 0
    TAGS = [
        'NOUN', 'PRON', 'VERB',
        'NUM', 'ADJ', 'ADP',
        'CCONJ', 'SCONJ', 'X',
        'AUX', 'DET', 'ADV',
        'PART', 'INTJ', 'PUNCT',
        'SYM', 'PROPN',
    ]

    def __init__(self, train_file="etc/dataset/preprocessed.txt", trigram=False):
        self.trigram = trigram
        word_tags = []
        train = open(train_file, "r+", encoding="utf-8").readlines()
        for sentence in train:
            word_tags.append(("START", "START"))
            pairs = sentence.split(" ")
            pairs = pairs[:-1]  # ignore newline
            for pair in pairs:
                word = "/".join(pair.split("/")[0:-1])
                tag = pair.split("/")[-1]
                if tag != "":
                    word_tags.append((tag, word))
                else:
                    word_tags.append(("/", "PUNCT"))
                self.N += 1

            word_tags.append(("END", "END"))

        # get the conditional frequency distribution
        self.cfd_word_tags = nltk.ConditionalFreqDist(word_tags)

        tags = []

        for sentence in train:
            tags.append("START")
            pairs = sentence.split(" ")
            pairs = pairs[:-1]  # ignore newline
            for pair in pairs:
                tag = pair.split("/")[-1]
                if tag != "":
                    tags.append(tag)
                else:
                    tags.append("PUNCT")

            tags.append("END")

        # self.fd = nltk.FreqDist(tags)
        # for key, val in sorted(self.fd.items(), key=lambda x: x[1], reverse=True):
        #     print(key, val)

        if not trigram:
            self.cfd_tags = nltk.ConditionalFreqDist(nltk.bigrams(tags))
            # print(self.cfd_tags.keys())
        else:
            trigrams = [((x,y),z) for x,y,z in nltk.trigrams(tags)]
            self.cfd_tags = nltk.ConditionalFreqDist(trigrams)

    def get_emission_prob(self, word, tag, smoothing=True):
        num = self.cfd_word_tags[tag][word]
        denom = sum(list(self.cfd_word_tags[tag].values()))
        if smoothing:
            return (num + 1) / (denom + self.N)
        else:
            return num / denom

    def get_transition_prob(self, tag, prev_tag, smoothing=True):
        num = self.cfd_tags[prev_tag][tag]
        denom = sum(list(self.cfd_tags[prev_tag].values()))
        if smoothing:
            return (num + 1) / (denom + len(self.TAGS))
        else:
            return num / denom
