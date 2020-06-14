import sys
sys.path.append("./AESA/")

from preprocess_aesa import *
from stop_words import STOP_WORDS
import pickle
from os import system, name

class Inference_AESA():
  def __init__(self,vncorenlp):
    self.vectorizer = pickle.load(open('./AESA/model_AESA/vect.sav', 'rb'))
    self.model = {}
    self.model['AMBIENCE#GENERAL'] = pickle.load(open('./AESA/model_AESA/ambience_general.sav', 'rb'))
    self.model['DRINKS#PRICES'] = pickle.load(open('./AESA/model_AESA/drinks_prices.sav', 'rb'))
    self.model['DRINKS#QUALITY'] = pickle.load(open('./AESA/model_AESA/drinks_quality.sav', 'rb'))
    self.model['DRINKS#STYLEOPTIONS'] = pickle.load(open('./AESA/model_AESA/drinks_style_options.sav', 'rb'))
    self.model['FOOD#PRICES'] = pickle.load(open('./AESA/model_AESA/food_prices.sav', 'rb'))
    self.model['FOOD#QUALITY']  = pickle.load(open('./AESA/model_AESA/food_quality.sav', 'rb'))
    self.model['FOOD#STYLEOPTIONS'] = pickle.load(open('./AESA/model_AESA/food_style_options.sav', 'rb'))
    self.model['LOCATION#GENERAL'] = pickle.load(open('./AESA/model_AESA/location_general.sav', 'rb'))
    self.model['RESTAURANT#GENERAL'] = pickle.load(open('./AESA/model_AESA/restaurant_general.sav', 'rb'))
    self.model['RESTAURANT#MISCELLANEOUS'] = pickle.load(open('./AESA/model_AESA/restaurant_miscellaneous.sav', 'rb'))
    self.model['RESTAURANT#PRICES'] = pickle.load(open('./AESA/model_AESA/restaurant_prices.sav', 'rb'))
    self.model['SERVICE#GENERAL'] = pickle.load(open('./AESA/model_AESA/service_general.sav', 'rb'))

    self.vncorenlp = vncorenlp

  def predict(self, text):
    text = normalize_text(self.vncorenlp,text,STOP_WORDS,1,3)
    cands = self.vectorizer.transform([text])
    aspects = []
    for aspect,m in self.model.items():
      out = m.predict(cands)[0]
      if out == 1:
        aspects.append(aspect)
    return aspects