__author__ = 'max'

import os.path
import random
import numpy as np
from .alphabet import Alphabet
from .logger import get_logger
from . import utils
import torch
from torch.autograd import Variable

# Special vocabulary symbols - we always put them at the start.
PAD = "_PAD"
PAD_POS = "_PAD_POS"
PAD_TYPE = "_<PAD>"
PAD_CHAR = "_PAD_CHAR"
PAD_CHUNK = "_PAD_CHUNK"
PAD_NER = "_PAD_NER"

ROOT = "_ROOT"
ROOT_POS = "_ROOT_POS"
ROOT_TYPE = "_<ROOT>"
ROOT_CHAR = "_ROOT_CHAR"

END = "_END"
END_POS = "_END_POS"
END_TYPE = "_<END>"
END_CHAR = "_END_CHAR"
_START_VOCAB = [PAD, ROOT, END]

UNK_ID = 0
PAD_ID_WORD = 1
PAD_ID_CHAR = 1
PAD_ID_TAG = 0

NUM_SYMBOLIC_TAGS = 3

_buckets = [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 140]

from .reader import CoNLLXReader


def create_alphabets(alphabet_directory, train_path, data_paths=None, max_vocabulary_size=50000, embedd_dict=None,
                     min_occurence=1, normalize_digits=True):
    def expand_vocab():
        vocab_set = set(vocab_list)
        max_sent_length = 0
        for data_path in data_paths:
            # logger.info("Processing data: %s" % data_path)
            with open(data_path, 'r') as file:
                sent_length = 1
                for line in file:
                    line = line.decode('utf-8')
                    line = line.strip()
                    if len(line) == 0:
                        for val in _buckets:
                            if val > sent_length:
                                sent_length = val
                                break
                        if sent_length > max_sent_length:
                            max_sent_length = sent_length
                        sent_length = 1
                        continue

                    tokens = line.split('\t')
                    for char in tokens[1]:
                        char_alphabet.add(char)

                    word = utils.DIGIT_RE.sub(b"0", tokens[1]) if normalize_digits else tokens[1]
                    pos = tokens[4]
                    type = utils.get_main_deplabel(tokens[7])

                    pos_alphabet.add(pos)
                    type_alphabet.add(type)

                    if embedd_dict is not None:
                        if word not in vocab_set and (word in embedd_dict or word.lower() in embedd_dict):
                            vocab_set.add(word)
                            vocab_list.append(word)

        return max_sent_length

    def cosine_dict(dic1, dic2):
        numerator = 0
        dena = 0
        for key1, val1 in list(dic1.items()):
            numerator += val1 * dic2.get(key1, 0)
            dena += val1 * val1
        denb = 0
        for val2 in list(dic2.values()):
            denb += val2 * val2
        import math
        return numerator / math.sqrt(dena * denb)

    def check_sentences_for_types(data_path, src_types, freq_dict):
        """temporarily written for stat check - wasi"""
        # logger.info("Processing data: %s" % data_path)
        count1, count2 = 1, 0
        new_line = True
        type_alph_dict = dict()
        with open(data_path, 'r') as file:
            for line in file:
                line = line.decode('utf-8')
                line = line.strip()
                if len(line) == 0:
                    new_line = True
                    count1 += 1
                    continue

                tokens = line.split('\t')
                type = tokens[7]
                if type in type_alph_dict:
                    type_alph_dict[type] += 1
                else:
                    type_alph_dict[type] = 1

                if type not in src_types and new_line:
                    count2 += 1
                    new_line = False

            print(('total sentences = ', count1))
            print(('total sentences that contain a label not appeared in src lang = ', count2))
            print(('cosine similarity = ', cosine_dict(freq_dict, type_alph_dict)))

    logger = get_logger("Create Alphabets")
    word_alphabet = Alphabet('word', defualt_value=True, singleton=True)
    char_alphabet = Alphabet('character', defualt_value=True)
    pos_alphabet = Alphabet('pos')
    type_alphabet = Alphabet('type')
    max_sent_length = 0
    if not os.path.isdir(alphabet_directory):
        # logger.info("Creating Alphabets: %s" % alphabet_directory)

        char_alphabet.add(PAD_CHAR)
        pos_alphabet.add(PAD_POS)
        type_alphabet.add(PAD_TYPE)

        char_alphabet.add(ROOT_CHAR)
        pos_alphabet.add(ROOT_POS)
        type_alphabet.add(ROOT_TYPE)

        char_alphabet.add(END_CHAR)
        pos_alphabet.add(END_POS)
        type_alphabet.add(END_TYPE)

        vocab = dict()
        type_alph_dict = dict()  ## temporary
        sent_length = 1
        with open(train_path, 'r') as file:
            for line in file:
                line = line.decode('utf-8')
                line = line.strip()
                if len(line) == 0:
                    for val in _buckets:
                        if val > sent_length:
                            sent_length = val
                            break
                    if sent_length > max_sent_length:
                        max_sent_length = sent_length
                    sent_length = 1
                    continue

                tokens = line.split('\t')
                for char in tokens[1]:
                    char_alphabet.add(char)

                sent_length += 1
                word = utils.DIGIT_RE.sub(b"0", tokens[1]) if normalize_digits else tokens[1]
                pos = tokens[4]
                type = utils.get_main_deplabel(tokens[7])

                pos_alphabet.add(pos)
                type_alphabet.add(type)
                if type in type_alph_dict:
                    type_alph_dict[type] += 1
                else:
                    type_alph_dict[type] = 1

                if word in vocab:
                    vocab[word] += 1
                else:
                    vocab[word] = 1

        #############################
        # temporary code
        # if data_paths is not None:
        #     check_sentences_for_types(data_paths[1], type_alphabet.items(), type_alph_dict)
        ############################

        # collect singletons
        singletons = set([word for word, count in list(vocab.items()) if count <= min_occurence])

        # if a singleton is in pretrained embedding dict, set the count to min_occur + c
        if embedd_dict is not None:
            for word in list(vocab.keys()):
                if word in embedd_dict or word.lower() in embedd_dict:
                    vocab[word] += min_occurence

        vocab_list = _START_VOCAB + sorted(vocab, key=vocab.get, reverse=True)
        # logger.info("Total Vocabulary Size: %d" % len(vocab_list))
        # logger.info("Total Singleton Size:  %d" % len(singletons))
        vocab_list = [word for word in vocab_list if word in _START_VOCAB or vocab[word] > min_occurence]
        # logger.info("Total Vocabulary Size (w.o rare words): %d" % len(vocab_list))

        if len(vocab_list) > max_vocabulary_size:
            vocab_list = vocab_list[:max_vocabulary_size]

        if data_paths is not None:
            # logger.info("expanding vocab")
            sent_length = expand_vocab()
            if sent_length > max_sent_length:
                max_sent_length = sent_length

        # if data_paths is not None and embedd_dict is not None:
        #     expand_vocab()

        for word in vocab_list:
            word_alphabet.add(word)
            if word in singletons:
                word_alphabet.add_singleton(word_alphabet.get_index(word))

        word_alphabet.save(alphabet_directory)
        char_alphabet.save(alphabet_directory)
        pos_alphabet.save(alphabet_directory)
        type_alphabet.save(alphabet_directory)
    else:
        word_alphabet.load(alphabet_directory)
        char_alphabet.load(alphabet_directory)
        pos_alphabet.load(alphabet_directory)
        type_alphabet.load(alphabet_directory)

    word_alphabet.close()
    char_alphabet.close()
    pos_alphabet.close()
    type_alphabet.close()
    # logger.info("Word Alphabet Size (Singleton): %d (%d)" % (word_alphabet.size(), word_alphabet.singleton_size()))
    # logger.info("Character Alphabet Size: %d" % char_alphabet.size())
    # logger.info("POS Alphabet Size: %d" % pos_alphabet.size())
    # logger.info("Type Alphabet Size: %d" % type_alphabet.size())
    # logger.info("Maximum Sentence Length: %d" % max_sent_length)

    return word_alphabet, char_alphabet, pos_alphabet, type_alphabet, max_sent_length


def read_data(source_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet, max_size=None,
              normalize_digits=True, symbolic_root=False, symbolic_end=False, lang_id="", len_thresh=None):
    data = [[] for _ in _buckets]
    max_char_length = [0 for _ in _buckets]
    print(('Reading data from %s' % source_path))
    counter = 0
    counter_added = 0
    reader = CoNLLXReader(source_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet, lang_id=lang_id)
    inst = reader.getNext(normalize_digits=normalize_digits, symbolic_root=symbolic_root, symbolic_end=symbolic_end)
    while inst is not None and (not max_size or counter < max_size):
        counter += 1
        if counter % 10000 == 0:
            print(("reading data: %d" % counter))

        inst_size = inst.length()
        if inst_size <= len_thresh:
            sent = inst.sentence
            for bucket_id, bucket_size in enumerate(_buckets):
                if inst_size < bucket_size:
                    data[bucket_id].append([sent.word_ids, sent.char_id_seqs, inst.pos_ids, inst.heads, inst.type_ids])
                    max_len = max([len(char_seq) for char_seq in sent.char_seqs])
                    if max_char_length[bucket_id] < max_len:
                        max_char_length[bucket_id] = max_len
                    break
            counter_added += 1

        inst = reader.getNext(normalize_digits=normalize_digits, symbolic_root=symbolic_root, symbolic_end=symbolic_end)
    reader.close()
    print(("Total number of data: %d, used: %d" % (counter, counter_added)))
    return data, max_char_length


def get_batch(data, batch_size, word_alphabet=None, unk_replace=0.):
    data, max_char_length = data
    bucket_sizes = [len(data[b]) for b in range(len(_buckets))]
    total_size = float(sum(bucket_sizes))
    # A bucket scale is a list of increasing numbers from 0 to 1 that we'll use
    # to select a bucket. Length of [scale[i], scale[i+1]] is proportional to
    # the size if i-th training bucket, as used later.
    buckets_scale = [sum(bucket_sizes[:i + 1]) / total_size for i in range(len(bucket_sizes))]

    # Choose a bucket according to data distribution. We pick a random number
    # in [0, 1] and use the corresponding interval in train_buckets_scale.
    random_number = np.random.random_sample()
    bucket_id = min([i for i in range(len(buckets_scale)) if buckets_scale[i] > random_number])

    bucket_length = _buckets[bucket_id]
    char_length = min(utils.MAX_CHAR_LENGTH, max_char_length[bucket_id] + utils.NUM_CHAR_PAD)
    bucket_size = bucket_sizes[bucket_id]
    batch_size = min(bucket_size, batch_size)

    wid_inputs = np.empty([batch_size, bucket_length], dtype=np.int64)
    cid_inputs = np.empty([batch_size, bucket_length, char_length], dtype=np.int64)
    pid_inputs = np.empty([batch_size, bucket_length], dtype=np.int64)
    hid_inputs = np.empty([batch_size, bucket_length], dtype=np.int64)
    tid_inputs = np.empty([batch_size, bucket_length], dtype=np.int64)

    masks = np.zeros([batch_size, bucket_length], dtype=np.float32)
    single = np.zeros([batch_size, bucket_length], dtype=np.int64)

    for b in range(batch_size):
        wids, cid_seqs, pids, hids, tids = random.choice(data[bucket_id])

        inst_size = len(wids)
        # word ids
        wid_inputs[b, :inst_size] = wids
        wid_inputs[b, inst_size:] = PAD_ID_WORD
        for c, cids in enumerate(cid_seqs):
            cid_inputs[b, c, :len(cids)] = cids
            cid_inputs[b, c, len(cids):] = PAD_ID_CHAR
        cid_inputs[b, inst_size:, :] = PAD_ID_CHAR
        # pos ids
        pid_inputs[b, :inst_size] = pids
        pid_inputs[b, inst_size:] = PAD_ID_TAG
        # type ids
        tid_inputs[b, :inst_size] = tids
        tid_inputs[b, inst_size:] = PAD_ID_TAG
        # heads
        hid_inputs[b, :inst_size] = hids
        hid_inputs[b, inst_size:] = PAD_ID_TAG
        # masks
        masks[b, :inst_size] = 1.0

        if unk_replace:
            for j, wid in enumerate(wids):
                if word_alphabet.is_singleton(wid):
                    single[b, j] = 1

    if unk_replace:
        noise = np.random.binomial(1, unk_replace, size=[batch_size, bucket_length])
        wid_inputs = wid_inputs * (1 - noise * single)

    return wid_inputs, cid_inputs, pid_inputs, hid_inputs, tid_inputs, masks


def iterate_batch(data, batch_size, word_alphabet=None, unk_replace=0., shuffle=False):
    data, max_char_length = data
    bucket_sizes = [len(data[b]) for b in range(len(_buckets))]
    total_size = float(sum(bucket_sizes))
    bucket_indices = np.arange(len(_buckets))
    if shuffle:
        np.random.shuffle((bucket_indices))

    for bucket_id in bucket_indices:
        bucket_size = bucket_sizes[bucket_id]
        if bucket_size == 0:
            continue

        bucket_length = _buckets[bucket_id]
        char_length = min(utils.MAX_CHAR_LENGTH, max_char_length[bucket_id] + utils.NUM_CHAR_PAD)
        wid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)
        cid_inputs = np.empty([bucket_size, bucket_length, char_length], dtype=np.int64)
        pid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)
        hid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)
        tid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)

        masks = np.zeros([bucket_size, bucket_length], dtype=np.float32)
        single = np.zeros([bucket_size, bucket_length], dtype=np.int64)

        for i, inst in enumerate(data[bucket_id]):
            wids, cid_seqs, pids, hids, tids = inst
            inst_size = len(wids)
            # word ids
            wid_inputs[i, :inst_size] = wids
            wid_inputs[i, inst_size:] = PAD_ID_WORD
            for c, cids in enumerate(cid_seqs):
                cid_inputs[i, c, :len(cids)] = cids
                cid_inputs[i, c, len(cids):] = PAD_ID_CHAR
            cid_inputs[i, inst_size:, :] = PAD_ID_CHAR
            # pos ids
            pid_inputs[i, :inst_size] = pids
            pid_inputs[i, inst_size:] = PAD_ID_TAG
            # type ids
            tid_inputs[i, :inst_size] = tids
            tid_inputs[i, inst_size:] = PAD_ID_TAG
            # heads
            hid_inputs[i, :inst_size] = hids
            hid_inputs[i, inst_size:] = PAD_ID_TAG
            # masks
            masks[i, :inst_size] = 1.0
            if unk_replace:
                for j, wid in enumerate(wids):
                    if word_alphabet.is_singleton(wid):
                        single[i, j] = 1

        if unk_replace:
            noise = np.random.binomial(1, unk_replace, size=[bucket_size, bucket_length])
            wid_inputs = wid_inputs * (1 - noise * single)

        indices = None
        if shuffle:
            indices = np.arange(bucket_size)
            np.random.shuffle(indices)
        for start_idx in range(0, bucket_size, batch_size):
            if shuffle:
                excerpt = indices[start_idx:start_idx + batch_size]
            else:
                excerpt = slice(start_idx, start_idx + batch_size)
            yield wid_inputs[excerpt], cid_inputs[excerpt], pid_inputs[excerpt], hid_inputs[excerpt], \
                  tid_inputs[excerpt], masks[excerpt]


def read_data_to_variable(source_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet, max_size=None,
                          normalize_digits=True, symbolic_root=False, symbolic_end=False,
                          use_gpu=False, volatile=False, lang_id="", len_thresh=100000):
    data, max_char_length = read_data(source_path, word_alphabet, char_alphabet, pos_alphabet, type_alphabet,
                                      max_size=max_size, normalize_digits=normalize_digits, symbolic_root=symbolic_root,
                                      symbolic_end=symbolic_end, lang_id=lang_id, len_thresh=len_thresh)
    bucket_sizes = [len(data[b]) for b in range(len(_buckets))]

    data_variable = []

    for bucket_id in range(len(_buckets)):
        bucket_size = bucket_sizes[bucket_id]
        if bucket_size == 0:
            data_variable.append((1, 1))
            continue

        bucket_length = _buckets[bucket_id]
        char_length = min(utils.MAX_CHAR_LENGTH, max_char_length[bucket_id] + utils.NUM_CHAR_PAD)
        wid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)
        cid_inputs = np.empty([bucket_size, bucket_length, char_length], dtype=np.int64)
        pid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)
        hid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)
        tid_inputs = np.empty([bucket_size, bucket_length], dtype=np.int64)

        masks = np.zeros([bucket_size, bucket_length], dtype=np.float32)
        single = np.zeros([bucket_size, bucket_length], dtype=np.int64)

        lengths = np.empty(bucket_size, dtype=np.int64)

        for i, inst in enumerate(data[bucket_id]):
            wids, cid_seqs, pids, hids, tids = inst
            inst_size = len(wids)
            lengths[i] = inst_size
            # word ids
            wid_inputs[i, :inst_size] = wids
            wid_inputs[i, inst_size:] = PAD_ID_WORD
            for c, cids in enumerate(cid_seqs):
                cid_inputs[i, c, :len(cids)] = cids
                cid_inputs[i, c, len(cids):] = PAD_ID_CHAR
            cid_inputs[i, inst_size:, :] = PAD_ID_CHAR
            # pos ids
            pid_inputs[i, :inst_size] = pids
            pid_inputs[i, inst_size:] = PAD_ID_TAG
            # type ids
            tid_inputs[i, :inst_size] = tids
            tid_inputs[i, inst_size:] = PAD_ID_TAG
            # heads
            hid_inputs[i, :inst_size] = hids
            hid_inputs[i, inst_size:] = PAD_ID_TAG
            # masks
            masks[i, :inst_size] = 1.0
            for j, wid in enumerate(wids):
                if word_alphabet.is_singleton(wid):
                    single[i, j] = 1

        with torch.no_grad():
            words = torch.from_numpy(wid_inputs)
            chars = torch.from_numpy(cid_inputs)
            pos = torch.from_numpy(pid_inputs)
            heads = torch.from_numpy(hid_inputs)
            types = torch.from_numpy(tid_inputs)
            masks = torch.from_numpy(masks)
            single = torch.from_numpy(single)
            lengths = torch.from_numpy(lengths)
            if use_gpu:
                words = words.cuda()
                chars = chars.cuda()
                pos = pos.cuda()
                heads = heads.cuda()
                types = types.cuda()
                masks = masks.cuda()
                single = single.cuda()
                lengths = lengths.cuda()

        data_variable.append((words, chars, pos, heads, types, masks, single, lengths))

    return data_variable, bucket_sizes


def get_batch_variable(data, batch_size, unk_replace=0.):
    data_variable, bucket_sizes = data
    total_size = float(sum(bucket_sizes))
    # A bucket scale is a list of increasing numbers from 0 to 1 that we'll use
    # to select a bucket. Length of [scale[i], scale[i+1]] is proportional to
    # the size if i-th training bucket, as used later.
    buckets_scale = [sum(bucket_sizes[:i + 1]) / total_size for i in range(len(bucket_sizes))]

    # Choose a bucket according to data distribution. We pick a random number
    # in [0, 1] and use the corresponding interval in train_buckets_scale.
    random_number = np.random.random_sample()
    bucket_id = min([i for i in range(len(buckets_scale)) if buckets_scale[i] > random_number])
    bucket_length = _buckets[bucket_id]

    words, chars, pos, heads, types, masks, single, lengths = data_variable[bucket_id]
    bucket_size = bucket_sizes[bucket_id]
    batch_size = min(bucket_size, batch_size)
    index = torch.randperm(bucket_size).long()[:batch_size]
    if words.is_cuda:
        index = index.cuda()

    words = words[index]
    if unk_replace:
        ones = Variable(single.data.new(batch_size, bucket_length).fill_(1))
        noise = Variable(masks.data.new(batch_size, bucket_length).bernoulli_(unk_replace).long())
        words = words * (ones - single[index] * noise)

    return words, chars[index], pos[index], heads[index], types[index], masks[index], lengths[index]


def iterate_batch_variable(data, batch_size, unk_replace=0., shuffle=False):
    data_variable, bucket_sizes = data

    bucket_indices = np.arange(len(_buckets))
    if shuffle:
        np.random.shuffle((bucket_indices))

    for bucket_id in bucket_indices:
        bucket_size = bucket_sizes[bucket_id]
        bucket_length = _buckets[bucket_id]
        if bucket_size == 0:
            continue

        words, chars, pos, heads, types, masks, single, lengths = data_variable[bucket_id]
        if unk_replace:
            ones = Variable(single.data.new(bucket_size, bucket_length).fill_(1))
            noise = Variable(masks.data.new(bucket_size, bucket_length).bernoulli_(unk_replace).long())
            words = words * (ones - single * noise)

        indices = None
        if shuffle:
            indices = torch.randperm(bucket_size).long()
            if words.is_cuda:
                indices = indices.cuda()
        for start_idx in range(0, bucket_size, batch_size):
            if shuffle:
                excerpt = indices[start_idx:start_idx + batch_size]
            else:
                excerpt = slice(start_idx, start_idx + batch_size)
            yield words[excerpt], chars[excerpt], pos[excerpt], heads[excerpt], types[excerpt], \
                  masks[excerpt], lengths[excerpt]
