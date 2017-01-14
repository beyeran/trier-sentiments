# gensim modules
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from sklearn.multiclass import OneVsOneClassifier

# numpy
import numpy

# classifier
from sklearn.svm import LinearSVC

# unitlities
import logging
import sys

log = logging.getLogger()
log.setLevel(logging.DEBUG)

class Doc2VecModel:
    model      = None
    classifier = None
    vectors    = []
    labels     = []

    # I have not thought about a better  way to present the offsets of the
    # doc2vec model yet.
    length_neg    = 7072
    length_sw_neg = 27273
    length_neu    = 79582
    length_sw_pos = 32927
    length_pos    = 9206

    def __init__(self, path):
        self.path = path

        log.info("Loading doc2vec model ...")
        self.model = Doc2Vec.load(self.path)

        # The model is stored as a whole in the same sequence it is learned.
        # Each length has the range of it encoded indirectly: since counting
        # starts at zero it is it's length minus 1. All examples are subsequently
        # the sum minus 1.
        log.info("Transforming labels ...")
        for i in range( self.length_neg + self.length_sw_neg + self.length_neu + self.length_sw_pos + self.length_pos - 1):
            if i <= (self.length_neg - 1):
                self.labels  += [4]
            elif i <= (self.length_neg + self.length_sw_neg - 1):
                self.labels  += [3]
            elif i <= (self.length_neg + self.length_sw_neg + self.length_neu - 1):
                self.labels  += [2]
            elif i <= (self.length_neg + self.length_sw_neg + self.length_neu + self.length_sw_pos - 1):
                self.labels  += [1]
            elif i < (self.length_neg + self.length_sw_neg + self.length_neu + self.length_sw_pos + self.length_pos):
                self.labels  += [0]

            self.vectors += [self.model.docvecs[i]]

        # train the classifier
        log.info("Training the classifier ...")
        self.classifier = OneVsOneClassifier(LinearSVC())
        self.classifier.fit(numpy.array(self.vectors), numpy.array(self.labels))

    def classify(self, sentence):
        vector = self.model.infer_vector( sentence )
        prediction = self.classifier.predict(vector.reshape(1, -1))

        return prediction[0]

    def test(self, path):
        correct = []
        wrong   = []
        count   = 0

        with open(path, 'r') as f:
            sentimentreader = csv.reader(f, delimiter='\t')

            for row in sentimentreader:
                sentiment = int(row[0])
                sentence  = row[2]

                prediction = self.classify(sentence)

                if sentiment == prediction:
                    correct.append((count, sentence, sentiment, sentiment))
                else:
                    wrong.append((count, sentence, sentiment, prediction))

                    count += 1

        return [correct, wrong]
