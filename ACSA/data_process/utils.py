import os
import numpy as np
import random
from xml.etree.ElementTree import parse
from data_process.vocab import Vocab
from src.module.utils.constants import UNK, PAD_INDEX, ASPECT_INDEX
import re
import json
from tqdm import tqdm

def check(x):
    return len(x) >= 1 and not x.isspace()

def tokenizer(text):
    tokens = text.split()
    return list(filter(check, tokens))

def parse_sentence_term(path, lowercase=False):
    tree = parse(path)
    sentences = tree.getroot()
    data = []
    split_char = '__split__'
    for sentence in sentences:
        text = sentence.find('text')
        if text is None:
            continue
        text = text.text
        if lowercase:
            text = text.lower()
        aspectTerms = sentence.find('aspectTerms')
        if aspectTerms is None:
            continue
        for aspectTerm in aspectTerms:
            term = aspectTerm.get('term')
            if lowercase:
                term = term.lower()
            polarity = aspectTerm.get('polarity')
            start = aspectTerm.get('from')
            end = aspectTerm.get('to')
            piece = text + split_char + term + split_char + polarity + split_char + start + split_char + end
            data.append(piece)
    return data

def parse_sentence_category(path, lowercase=False):
    tree = parse(path)
    sentences = tree.getroot()
    data = []
    split_char = '__split__'
    for sentence in sentences:
        text = sentence.find('text')
        if text is None:
            continue
        text = text.text
        if lowercase:
            text = text.lower()
        aspectCategories = sentence.find('aspectCategories')
        if aspectCategories is None:
            continue
        for aspectCategory in aspectCategories:
            category = aspectCategory.get('category')
            polarity = aspectCategory.get('polarity')
            piece = text + split_char + category + split_char + polarity
            data.append(piece)
    return data

def category_filter(data, remove_list):
    remove_set = set(remove_list)
    filtered_data = []
    for text in data:
        if not text.split('__split__')[2] in remove_set:
            filtered_data.append(text)
    return filtered_data

def build_vocab(data, max_size, min_freq):
    if max_size == 'None':
        max_size = None
    vocab = Vocab()
    for piece in data:
        text = piece.split('__split__')[0]
        text = tokenizer(text)
        vocab.add_list(text)
    return vocab.get_vocab(max_size=max_size, min_freq=min_freq)

def save_term_data(data, word2index, path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    sentence = []
    aspect = []
    label = []
    context = []
    td_left = []
    td_right = []
    f = lambda x: word2index[x] if x in word2index else word2index[UNK]
    g = lambda x: list(map(f, tokenizer(x)))
    d = {
        'positive': 0,
        'negative': 1,
        'neutral': 2
    }
    for piece in data:
        text, term, polarity, start, end = piece.split('__split__')
        start, end = int(start), int(end)
        assert text[start: end] == term
        sentence.append(g(text))
        aspect.append(g(term))
        label.append(d[polarity])
        left_part = g(text[:start])
        right_part = g(text[end:])
        context.append(left_part + [ASPECT_INDEX] + right_part)
        td_left.append(g(text[:end]))
        td_right.append(g(text[start:])[::-1])
    max_length = lambda x: max([len(y) for y in x])
    sentence_max_len = max_length(sentence)
    aspect_max_len = max_length(aspect)
    context_max_len = max_length(context)
    td_left_max_len = max_length(td_left)
    td_right_max_len = max_length(td_right)
    num = len(data)
    for i in range(num):
        sentence[i].extend([0] * (sentence_max_len - len(sentence[i])))
        aspect[i].extend([0] * (aspect_max_len - len(aspect[i])))
        context[i].extend([0] * (context_max_len - len(context[i])))
        td_left[i].extend([0] * (td_left_max_len - len(td_left[i])))
        td_right[i].extend([0] * (td_right_max_len - len(td_right[i])))
    sentence = np.asarray(sentence, dtype=np.int32)
    aspect = np.asarray(aspect, dtype=np.int32)
    label = np.asarray(label, dtype=np.int32)
    context = np.asarray(context, dtype=np.int32)
    td_left = np.asarray(td_left, dtype=np.int32)
    td_right = np.asarray(td_right, dtype=np.int32)
    np.savez(path, sentence=sentence, aspect=aspect, label=label, context=context,
             td_left=td_left, td_right=td_right)

def save_category_data(data, word2index, path):
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    sentence = []
    aspect = []
    label = []
    f = lambda x: word2index[x] if x in word2index else word2index[UNK]
    g = lambda x: list(map(f, tokenizer(x)))
    d = {
        'positive': 0,
        'negative': 1,
        'neutral': 2
    }
    cd = {
        'FOOD#STYLEOPTIONS': 0,
        'FOOD#QUALITY': 1,
        'AMBIENCE#GENERAL': 2,
        'RESTAURANT#GENERAL': 3,
        'SERVICE#GENERAL': 4,
        'FOOD#PRICES': 5,
        'RESTAURANT#PRICES': 6,
        'LOCATION#GENERAL': 7,
        'RESTAURANT#MISCELLANEOUS': 8,
        'DRINKS#STYLEOPTIONS': 9,
        'DRINKS#PRICES': 10,
        'DRINKS#QUALITY': 11
    }
    # cd = {
    #     'HOTEL#DESIGNFEATURES': 0,
    #     'HOTEL#GENERAL': 1,
    #     'LOCATION#GENERAL': 2,
    #     'SERVICE#GENERAL': 3,
    #     'HOTEL#COMFORT': 4,
    #     'HOTEL#CLEANLINESS': 5,
    #     'FACILITIES#GENERAL': 6,
    #     'ROOMS#CLEANLINESS': 7,
    #     'ROOM_AMENITIES#COMFORT': 8,
    #     'ROOMS#COMFORT': 9,
    #     'FACILITIES#PRICES': 10,
    #     'ROOM_AMENITIES#GENERAL': 11,
    #     'FOODDRINKS#STYLEOPTIONS': 12,
    #     'ROOMS#PRICES': 13,
    #     'ROOMS#DESIGNFEATURES': 14,
    #     'ROOMS#GENERAL': 15,
    #     'HOTEL#QUALITY': 16,
    #     'ROOMS#QUALITY': 17,
    #     'FOODDRINKS#QUALITY': 18,
    #     'HOTEL#PRICES': 19,
    #     'FACILITIES#DESIGNFEATURES': 20,
    #     'FACILITIES#QUALITY': 21,
    #     'ROOM_AMENITIES#QUALITY': 22,
    #     'ROOM_AMENITIES#CLEANLINESS': 23,
    #     'ROOM_AMENITIES#DESIGNFEATURES': 24,
    #     'HOTEL#MISCELLANEOUS': 25,
    #     'FOODDRINKS#PRICES': 26,
    #     'FACILITIES#COMFORT': 27,
    #     'FOODDRINKS#MISCELLANEOUS': 28,
    #     'FACILITIES#CLEANLINESS': 29,
    #     'FACILITIES#MISCELLANEOUS': 30,
    #     'ROOMS#MISCELLANEOUS': 31,
    #     'ROOM_AMENITIES#MISCELLANEOUS': 32
    # }
    for piece in tqdm(data):
        text, category, polarity = piece.split('__split__')
        sentence.append(g(text))
        aspect.append(cd[category])
        label.append(d[polarity])
    max_length = lambda x: max([len(y) for y in x])
    sentence_max_len = max_length(sentence)
    num = len(data)
    for i in range(num):
        sentence[i].extend([0] * (sentence_max_len - len(sentence[i])))
    sentence = np.asarray(sentence, dtype=np.int32)
    aspect = np.asarray(aspect, dtype=np.int32)
    label = np.asarray(label, dtype=np.int32)
    np.savez(path, sentence=sentence, aspect=aspect, label=label)

def analyze_category(data):
    num = len(data)
    sentence_lens = []
    log = {'total': num}
    for piece in data:
        text, category, polarity = piece.split('__split__')
        sentence_lens.append(len(tokenizer(text)))
        if not polarity in log:
            log[polarity] = 0
        log[polarity] += 1
    log['sentence_max_len'] = max(sentence_lens)
    log['sentence_avg_len'] = sum(sentence_lens) / len(sentence_lens)
    return log

def load_glove(path, vocab_size, word2index):
    if not os.path.isfile(path):
        raise IOError('Not a file', path)
    glove = np.random.uniform(-0.01, 0.01, [vocab_size, 300])
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            content = line.split(' ')
            if content[0] in word2index:
                glove[word2index[content[0]]] = np.array(list(map(float, content[1:])))
    glove[PAD_INDEX, :] = 0
    return glove

def load_sentiment_matrix(glove_path, sentiment_path):
    sentiment_matrix = np.zeros((3, 300), dtype=np.float32)
    sd = json.load(open(sentiment_path, 'r', encoding='utf-8'))
    sd['positive'] = set(sd['positive'])
    sd['negative'] = set(sd['negative'])
    sd['neutral'] = set(sd['neutral'])
    with open(glove_path, 'r', encoding='utf-8') as f:
        for line in f:
            content = line.split(' ')
            word = content[0]
            vec = np.array(list(map(float, content[1:])))
            if word in sd['positive']:
                sentiment_matrix[0] += vec
            elif word in sd['negative']:
                sentiment_matrix[1] += vec
            elif word in sd['neutral']:
                sentiment_matrix[2] += vec
    sentiment_matrix -= sentiment_matrix.mean()
    sentiment_matrix = sentiment_matrix / sentiment_matrix.std() * np.sqrt(2.0 / (300.0 + 3.0))
    return sentiment_matrix