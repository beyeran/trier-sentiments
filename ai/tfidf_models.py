#
# TODO abstract model class
#


# utilities
import csv
import numpy as np
import pickle

# learning stuff
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsOneClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import xgboost

###
### models
####
class SVMModel:
    model     = None
    train_set = []
    
    def __init__(self, path):
        with open(path, 'r') as f:
            sentimentreader = csv.reader(f, delimiter='\t')

            for row in sentimentreader:
                sentiment = row[0]
                sentence  = row[2]
                self.train_set.append((sentiment, sentence))

    def train(self):
        sentence_set = [sentence for label, sentence in self.train_set]
        label_set    = [int(label) for label, sentence in self.train_set]

        model = Pipeline([('vect', CountVectorizer()),
                          ('tfidf', TfidfTransformer()),
                          ('clf', OneVsOneClassifier(LinearSVC()))
        ])

        model.fit(np.asarray(sentence_set), np.asarray(label_set))

        self.model = model

    def classify(self, sentence):
        prediction = self.model.predict(np.asarray([sentence]))
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

    def todisk(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)

    @classmethod
    def fromdisk(cls, path):
        with open(path, 'rb') as f:
            cls.model = pickle.load(f)

            return cls



class XGBoostModel:
    model     = None
    train_set = []
    
    def __init__(self, path):
        with open(path, 'r') as f:
            sentimentreader = csv.reader(f, delimiter='\t')

            for row in sentimentreader:
                sentiment = row[0]
                sentence  = row[2]
                self.train_set.append((sentiment, sentence))

    def train(self, train_set):
        sentence_set = [sentence for label, sentence in self.train_set]
        label_set    = [int(label) for label, sentence in self.train_set]

        # This should been done within a pipeline normally. This workaround
        # was needed because I don't use a not-sklear classifier and do not
        # know any better.
        vect  = CountVectorizer()
        tfidf = TfidfTransformer()

        print("Feature extraction..")
        counts   = vect.fit_transform(np.asarray(sentence_set))
        weighted = tfidf.fit_transform(counts.toarray())

        print("Learning...")
        model = xgboost.XGBClassifier()
        model.fit(weighted.toarray(), np.asarray(label_set))
    
        self.model = model

    def classify(self, sentence):
        prediction = self.model.predict(np.asarray([sentence]))
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
