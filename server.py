from flask import jsonify
from flask import Flask
from flask import request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

from ACSA.inference import Inference_ACSA
from AESA.inference import Inference_AESA
from vncorenlp import VnCoreNLP

annotator = VnCoreNLP("./ACSA/VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg, pos", max_heap_size='-Xmx500m')

AESA_predict = Inference_AESA(annotator)
ACSA_predict = Inference_ACSA(annotator)

@app.route('/aspect_sentiment_analysis', methods=['POST'])
def analysis():
    sentence = request.get_data()
    sentence = sentence.decode(encoding='utf-8')
    category = AESA_predict.predict(sentence)

    polarity = []
    for cate in category:
        pol = ACSA_predict.predict(sentence, cate)
        polarity.append(pol)
        
    sentence = {
                "category": ["service", "food", "prize"],
                "polarity": ["negative", "positive", "neutral"]
    }
    # result = {"category": category, "polarity": polarity}
    return jsonify(category=category, polarity=polarity)

if __name__ == '__main__':
   app.run()