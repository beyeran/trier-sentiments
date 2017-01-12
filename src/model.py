# gensim modules
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

# numpy
import numpy

# classifier
from sklearn.linear_model import LogisticRegression

import logging
import sys

# fixed ranges
length_train_neg    = 7072
length_train_sw_neg = 27273
length_train_neu    = 79582
length_train_sw_pos = 32927
length_train_pos    = 9206

class Model:
    model      = None
    vec_pos    = []
    vec_sw_pos = []
    vec_neu    = []
    vec_sw_neg = []
    vec_neg    = []

    def __init__(self, path, length_neg, length_sw_neg, length_neu, length_sw_pos, length_pos):
        Model.path          = path
        Model.length_neg    = length_neg
        Model.length_sw_neg = length_sw_neg
        Model.length_neu    = length_neu
        Model.length_sw_pos = length_sw_pos
        Model.length_pos    = length_pos
    
    def load(self):
        Model.model = Doc2Vec.load(Model.path)

        # The model is stored as a whole in the same sequence it is learned.
        # Each length has the range of it encoded indirectly: since counting
        # starts at zero it is it's length minus 1. All examples are subsequently
        # the sum minus 1.
        for i in range( Model.length_neg + Model.length_sw_neg + Model.length_neu + Model.length_sw_pos + Model.length_pos - 1):
            print(i)
            
            if i <= (Model.length_neg - 1):
                Model.vec_neg += [Model.model[i]]
            elif i <= (Model.length_neg + Model.length_sw_neg - 1):
                Model.vec_sw_neg += [Model.model[i]]
            elif i <= (Model.length_neg + Model.length_sw_neg + Model.length_neu - 1):
                Model.vec_neu += [Model.model[i]]
            elif i <= (Model.length_neg + Model.length_sw_neg + Model.length_neu + Model.length_sw_pos - 1):
                Model.vec_sw_pos += [Model.model[i]]
            elif i <= (Model.length_neg + Model.length_sw_neg + Model.length_neu + Model.length_sw_pos + Model.length_pos - 1):
                Model.vec_pos += [Model.model[i]]
            else:
                print("Something went wrong with index: " + i)
