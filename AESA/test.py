from vncorenlp import VnCoreNLP
import sys
sys.path.append(".")
from preprocess import *
from stop_words import STOP_WORDS
from vncorenlp import VnCoreNLP
import pickle
from os import system, name


vncorenlp_file = r'/VnCoreNLP/VnCoreNLP-1.1.1.jar'
vectorizer = pickle.load(open('model/vect.sav', 'rb'))
model = {}
model['ambience_general'] = pickle.load(open('model/ambience_general.sav', 'rb'))
model['drinks_prices'] = pickle.load(open('model/drinks_prices.sav', 'rb'))
model['drinks_quality'] = pickle.load(open('model/drinks_quality.sav', 'rb'))
model['drinks_style_options'] = pickle.load(open('model/drinks_style_options.sav', 'rb'))
model['food_prices'] = pickle.load(open('model/food_prices.sav', 'rb'))
model['food_quality']  = pickle.load(open('model/food_quality.sav', 'rb'))
model['food_style_options'] = pickle.load(open('model/food_style_options.sav', 'rb'))
model['location_general'] = pickle.load(open('model/location_general.sav', 'rb'))
model['restaurant_general'] = pickle.load(open('model/restaurant_general.sav', 'rb'))
model['restaurant_miscellaneous'] = pickle.load(open('model/restaurant_miscellaneous.sav', 'rb'))
model['restaurant_prices'] = pickle.load(open('model/restaurant_prices.sav', 'rb'))
model['service_general'] = pickle.load(open('model/service_general.sav', 'rb'))


vncorenlp = VnCoreNLP(vncorenlp_file, timeout=None, annotators='wseg,pos', max_heap_size='-Xmx500m', quiet=True)
while True:
  text = input("Nhập 1 chuỗi: ")
  text = normalize_text(vncorenlp,text,[],1,3)
  cands = vectorizer.transform([text])
  aspects = []
  for aspect,m in model.items():
    out = m.predict(cands)[0]
    if out == 1:
      aspects.append(aspect)
  print(aspects)
  choice = input('Press q to Quit')
  if choice.lower() == "q":
    vncorenlp.close()
    break
  if name == 'nt': 
      _ = system('cls') 
  # for mac and linux(here, os.name is 'posix') 
  else: 
      _ = system('clear') 