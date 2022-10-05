#

# the multi-lingual version of create_alphabets

import os.path
import random
import numpy as np
from ..io.alphabet import Alphabet
from ..io.logger import get_logger
from ..io import utils

from .lang_id import guess_language_id, lang_specific_word

# Special vocabulary symbols - we always put them at the start.
PAD = b"_PAD"
PAD_POS = b"_PAD_POS"
PAD_TYPE = b"_<PAD>"
PAD_CHAR = b"_PAD_CHAR"
ROOT = b"_ROOT"
ROOT_POS = b"_ROOT_POS"
ROOT_TYPE = b"_<ROOT>"
ROOT_CHAR = b"_ROOT_CHAR"
END = b"_END"
END_POS = b"_END_POS"
END_TYPE = b"_<END>"
END_CHAR = b"_END_CHAR"
_START_VOCAB = [PAD, ROOT, END]

# a generator that returns the stream of (orig_tokens, normed_words, pos, types)
def iter_file(filename):
    with open(filename, 'r') as file:
        ret = {"len": 0, "word": [], "pos": [], "type": []}
        for line in file:
            line = line.strip()
            # yield and reset
            if len(line) == 0 or line[0] == "#":
                if ret["len"] > 0:
                    yield ret
                ret = {"len": 0, "word": [], "pos": [], "type": []}
            else:
                fields = line.split('\t')
                ret["len"] += 1
                ret["word"].append(fields[1])
                ret["pos"].append(fields[4])
                # ret["type"].append(fields[7])
                ret["type"].append(utils.get_main_deplabel(fields[7]))
        if ret["len"] > 0:
            yield ret

def create_alphabets(alphabet_directory, train_path, data_paths=None, max_vocabulary_size=100000, embedd_dict=None,
                     min_occurence=1, normalize_digits=True, creating_mode=False):
    logger = get_logger("Create Alphabets")
    word_alphabet = Alphabet('word', defualt_value=True, singleton=True)
    char_alphabet = Alphabet('character', defualt_value=True)
    pos_alphabet = Alphabet('pos')
    type_alphabet = Alphabet('type')
    max_sent_length = 0
    # guess language
    lang_id_train = guess_language_id(train_path)
    lang_id_extras = None if data_paths is None else [guess_language_id(fname) for fname in data_paths]
    logger.info("Here, the input files are: train(%s), extras(%s)." % (lang_id_train, lang_id_extras))
    if not os.path.isdir(alphabet_directory):
        logger.info("Creating Alphabets: %s" % alphabet_directory)
        # add special tokens
        char_alphabet.add(PAD_CHAR)
        pos_alphabet.add(PAD_POS)
        type_alphabet.add(PAD_TYPE)

        char_alphabet.add(ROOT_CHAR)
        pos_alphabet.add(ROOT_POS)
        type_alphabet.add(ROOT_TYPE)

        char_alphabet.add(END_CHAR)
        pos_alphabet.add(END_POS)
        type_alphabet.add(END_TYPE)

        # special one for Chinese
        type_alphabet.add("clf")

        # count from the main train file
        vocab = dict()
        for one_sent in iter_file(train_path):
            cur_len = one_sent["len"]
            max_sent_length = max(max_sent_length, cur_len)
            for idx in range(cur_len):
                cur_word, cur_pos, cur_type = one_sent["word"][idx], one_sent["pos"][idx], one_sent["type"][idx]
                #
                for char in cur_word:
                    char_alphabet.add(char)
                pos_alphabet.add(cur_pos)
                type_alphabet.add(cur_type)
                normed_word = utils.DIGIT_RE.sub(b"0", cur_word) if normalize_digits else cur_word
                # add prefix
                normed_word = lang_specific_word(normed_word, lang_id=lang_id_train)
                if normed_word in vocab:
                    vocab[normed_word] += 1
                else:
                    vocab[normed_word] = 1
        # collect singletons
        singletons = set([word for word, count in list(vocab.items()) if count <= min_occurence])
        # if a singleton is in pretrained embedding dict, set the count to min_occur + c
        if embedd_dict is not None:
            for word in list(vocab.keys()):
                if word in embedd_dict or word.lower() in embedd_dict:
                    vocab[word] += min_occurence
        #
        vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)
        logger.info("Total Vocabulary Size: %d" % len(vocab_list))
        logger.info("Total Singleton Size:  %d" % len(singletons))
        vocab_list = [word for word in vocab_list if word in _START_VOCAB or vocab[word] > min_occurence]
        logger.info("Total Vocabulary Size (w.o rare words): %d" % len(vocab_list))
        #
        if len(vocab_list) > max_vocabulary_size:
            vocab_list = vocab_list[:max_vocabulary_size]
        # extra directly added files (usually dev or test)
        if data_paths is not None:
            for one_path, one_lang_id in zip(data_paths, lang_id_extras):
                vocab_set = set(vocab_list)
                count_word_vocab_in_embed = 0
                count_word_all, count_word_in = 0, 0
                for one_sent in iter_file(one_path):
                    cur_len = one_sent["len"]
                    max_sent_length = max(max_sent_length, cur_len)
                    for idx in range(cur_len):
                        cur_word, cur_pos, cur_type = one_sent["word"][idx], one_sent["pos"][idx], one_sent["type"][idx]
                        #
                        for char in cur_word:
                            char_alphabet.add(char)
                        pos_alphabet.add(cur_pos)
                        type_alphabet.add(cur_type)
                        normed_word = utils.DIGIT_RE.sub(b"0", cur_word) if normalize_digits else cur_word
                        # add prefix
                        normed_word = lang_specific_word(normed_word, lang_id=one_lang_id)
                        if embedd_dict is not None:
                            if normed_word in embedd_dict or normed_word.lower() in embedd_dict:
                                if normed_word not in vocab_set:
                                    vocab_list.append(normed_word)
                                    count_word_vocab_in_embed += 1
                                count_word_in += 1
                        vocab_set.add(normed_word)
                        count_word_all += 1
                logger.info("For the file %s, vocab-size/in-size: %d/%d, word-size/in-size: %d/%d." % (one_path, len(vocab_set), count_word_vocab_in_embed, count_word_all, count_word_in))
        #
        for word in vocab_list:
            word_alphabet.add(word)
            if word in singletons:
                word_alphabet.add_singleton(word_alphabet.get_index(word))
        #
        word_alphabet.save(alphabet_directory)
        char_alphabet.save(alphabet_directory)
        pos_alphabet.save(alphabet_directory)
        type_alphabet.save(alphabet_directory)
    else:
        assert not creating_mode, "Cannot load existed vocabs in creating mode."
        logger.info("Loading Alphabets: %s" % alphabet_directory)
        word_alphabet.load(alphabet_directory)
        char_alphabet.load(alphabet_directory)
        pos_alphabet.load(alphabet_directory)
        type_alphabet.load(alphabet_directory)
    #
    word_alphabet.close()
    char_alphabet.close()
    pos_alphabet.close()
    type_alphabet.close()
    logger.info("Word Alphabet Size (Singleton): %d (%d)" % (word_alphabet.size(), word_alphabet.singleton_size()))
    logger.info("Character Alphabet Size: %d" % char_alphabet.size())
    logger.info("POS Alphabet Size: %d" % pos_alphabet.size())
    logger.info("Type Alphabet Size: %d" % type_alphabet.size())
    logger.info("Maximum Sentence Length: %d" % max_sent_length)
    #
    return word_alphabet, char_alphabet, pos_alphabet, type_alphabet, max_sent_length
