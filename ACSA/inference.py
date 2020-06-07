from train import make_aspect_category_model
import numpy as np
import pickle
import os
import spacy
import re
import torch
from src.module.utils.constants import UNK

from vncorenlp import VnCoreNLP

annotator = VnCoreNLP("./VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx500m')

import yaml

config = yaml.safe_load(open('config.yml'))

def check(x):
    return len(x) >= 1 and not x.isspace()

def tokenizer(text):
    tokens = [tok.text for tok in annotator.tokenizer(text)]
    return list(filter(check, tokens))

with open(os.path.join(config['base_path'], 'processed/index2word.pickle'), 'rb') as handle:
    index2word = pickle.load(handle)

with open(os.path.join(config['base_path'], 'processed/word2index.pickle'), 'rb') as handle:
    word2index = pickle.load(handle)

def make_data(sen, aspt , word2index):
    data = [sen + "__split__" + aspt]
    sentence = []
    aspect = []
    f = lambda x: word2index[x] if x in word2index else word2index[UNK]
    g = lambda x: list(map(f, tokenizer(x)))
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
    for piece in data:
        text, category= piece.split('__split__')
        sentence.append(g(text))
        aspect.append(cd[category])
    max_length = lambda x: max([len(y) for y in x])
    sentence_max_len = max_length(sentence)
    num = len(data)
    for i in range(num):
        sentence[i].extend([0] * (sentence_max_len - len(sentence[i])))
    sentence = np.asarray(sentence, dtype=np.int32)
    aspect = np.asarray(aspect, dtype=np.int32)
    return torch.tensor(sentence).long(), torch.tensor(aspect).long()

# def make_tensor()

sen, aspect = make_data("view đẹp, dịch vụ chán", 'SERVICE#GENERAL', word2index)

model = make_aspect_category_model.make_model(config)
model = model.cuda()
model_path = os.path.join(config['base_path'], 'checkpoints/%s.pth' % config['aspect_' + mode + '_model']['type'])
model.load_state_dict(torch.load(model_path))
model.eval()

print(model(sen, aspect))

annotator.close()
