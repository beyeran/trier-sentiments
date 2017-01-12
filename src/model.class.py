# gensim modules
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

# numpy
import numpy

# classifier
from sklearn.svm import SVC

# unitlities
import logging
import sys

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# fixed ranges
length_train_neg    = 7072
length_train_sw_neg = 27273
length_train_neu    = 79582
length_train_sw_pos = 32927
length_train_pos    = 9206

class Model:
    model      = None
    vectors    = []
    labels     = []

    def __init__(self, path, length_neg, length_sw_neg, length_neu, length_sw_pos, length_pos):
        Model.path          = path
        Model.length_neg    = length_neg
        Model.length_sw_neg = length_sw_neg
        Model.length_neu    = length_neu
        Model.length_sw_pos = length_sw_pos
        Model.length_pos    = length_pos
    
    def load(self):
        log.info("Loading doc2vec model ...")
        Model.model = Doc2Vec.load(Model.path)

        # The model is stored as a whole in the same sequence it is learned.
        # Each length has the range of it encoded indirectly: since counting
        # starts at zero it is it's length minus 1. All examples are subsequently
        # the sum minus 1.
        log.info("Transforming labels ...")
        for i in range( Model.length_neg + Model.length_sw_neg + Model.length_neu + Model.length_sw_pos + Model.length_pos - 1):
            if i <= (Model.length_neg - 1):
                Model.labels  += [4]
            elif i <= (Model.length_neg + Model.length_sw_neg - 1):
                Model.labels  += [3]
            elif i <= (Model.length_neg + Model.length_sw_neg + Model.length_neu - 1):
                Model.labels  += [2]
            elif i <= (Model.length_neg + Model.length_sw_neg + Model.length_neu + Model.length_sw_pos - 1):
                Model.labels  += [1]
            elif i < (Model.length_neg + Model.length_sw_neg + Model.length_neu + Model.length_sw_pos + Model.length_pos):
                Model.labels  += [0]

            Model.vectors += [Model.model.docvecs[i]]

        # train the classifier
        log.info("Training the classifier ...")
        Model.classifier = SVC()
        Model.classifier.fit(numpy.array(Model.vectors), numpy.array(Model.labels))

    def classify(self, sentence):
        vector = Model.model.infer_vector( sentence )
        prediction = Model.classifier.predict(vector.reshape(1, -1))

        return prediction[0]

# foo = Model('./rotten.d2v', length_train_neg, length_train_sw_neg, length_train_neu, length_train_sw_pos, length_train_pos)
