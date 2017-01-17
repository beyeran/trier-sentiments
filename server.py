# models
from ai.tfidf_models import SVMModel

# server
from flask import Flask, request, render_template, jsonify
import json

# obtain model
svm = SVMModel('ai/data/train.tsv') # initialize model (path not really needed)
svm.fromdisk('ai/models/svm.model') # load pretrained model

app = Flask(__name__)

# api
@app.route('/sentiment', methods=['POST'])
def sentiment_classification():
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


@app.route("/")
def main():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)
