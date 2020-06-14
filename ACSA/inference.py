from train import make_aspect_category_model
import numpy as np
import pickle
import os
import spacy
import re
import torch
from src.module.utils.constants import UNK

from vncorenlp import VnCoreNLP

from preprocess_sentence import normalize_text

annotator = VnCoreNLP("./VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx500m')

import yaml

config = yaml.safe_load(open('config.yml'))

class Inference():
    def __init__(self):
        self.word2index = self.get_word2index()
        self.model, self.cuda = self.get_model()
        self.classes = ["positve", "negative", "neutral"]
        
    def get_word2index(self):
        with open(os.path.join(config['base_path'], 'processed/word2index.pickle'), 'rb') as handle:
            word2index = pickle.load(handle)
        return word2index

    def check(self, x):
        return len(x) >= 1 and not x.isspace()

    def tokenizer(self, text):
        tokens = text.split()
        return list(filter(self.check, tokens))

    def make_data(self, sen, aspt):
        sen = normalize_text(annotator, sen)

        data = [sen + "__split__" + aspt]
        sentence = []
        aspect = []
        f = lambda x: self.word2index[x] if x in self.word2index else self.word2index[UNK]
        g = lambda x: list(map(f, self.tokenizer(x)))
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

    def get_model(self):
        model = make_aspect_category_model.make_model(config)
        cuda = False
        if torch.cuda.is_available():
            cuda = True
            model = model.cuda()
            model_path = 'model/recurrent_capsnet.pth'
            model.load_state_dict(torch.load(model_path))
            model.eval()
        else:
            model_path = 'model/recurrent_capsnet.pth'
            model.load_state_dict(torch.load(model_path, map_location='cpu'))
            model.eval()
        return model, cuda
    
    def predict(self, sentence, aspect):
        sentence, aspect = self.make_data(sentence, aspect)
        if self.cuda:
            device = torch.device("cuda")
            preds = self.model(sentence.to(device), aspect.to(device))
        else:
            preds = self.model(sentence, aspect)
        index = torch.argmax(preds, dim=1)[0]
        return self.classes[index]
