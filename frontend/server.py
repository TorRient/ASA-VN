from flask import jsonify
from flask import Flask
from flask import request
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)
@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/tener', methods=['POST'])
def tener():
    print(request.get_data())
    sentence = {
                "category":["service", "food", "prize","ducbeo","dungdeptrai"],
                "polarity": ["negative", "positive", "neutral","positive","positive"]
    }
    return jsonify(sentence)

if __name__ == '__main__':
   app.run()

