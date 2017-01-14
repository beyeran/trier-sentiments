# models
from tfidf_models import SVMModel

# server
from flask import Flask
from flask_restplus import Resource, Api, reqparse

# obtain model
svm = SVMModel('data/train.tsv') # initialize model (path not really needed)
svm.fromdisk('models/svm.model') # load pretrained model

app = Flask(__name__)
api = Api(app)

class ClassifySentiment(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('sentiment', type=str, help='The sentiment to be classified.')
            args = parser.parse_args()

            _sentiment = args['sentiment']

            if _sentiment == None:
                return {'status': 100, 'message': 'invalid form data'}

            classification = svm.classify(_sentiment)

            sentiments = ['positive', 'somewhat positive', 'neutral', 'somewhat negative', 'negative']
            
            return {'status': 200, 'classification': sentiments[classification]}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(ClassifySentiment, "/sentiment")

if __name__ == '__main__':
    app.run(debug=True)
