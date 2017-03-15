# models
from ai.tfidf_models import SVMModel

# server
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import json
import os

# obtain model
svm = SVMModel('ai/data/train.tsv') # initialize model (path not really needed)
svm.fromdisk('ai/models/svm.model') # load pretrained model

# config app
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=template_dir, static_url_path='')

CORS(app)

# api
@app.route('/sentiment', methods=['POST'])
def sentiment_classification():
    print(request)
    
    try:
        req = json.loads(request.data.decode("utf-8"))
        _sentiment = str(req['sentiment'])

        if _sentiment == None:
            return jsonify({'status': 100, 'message': 'invalid form data'})

        classification = int(svm.classify(_sentiment))
        sentiments = ['positive', 'somewhat positive',
                      'neutral',
                      'somewhat negative', 'negative']

        return jsonify({'status': 200, 'classification': sentiments[classification]})

    except Exception as e:
        return jsonify({'error': str(e)})

# frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
