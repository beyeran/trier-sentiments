# Trier Sentiments
Trier Sentiments is a small web application for automatically rating movie reviews. It was used as a
small presentation for advertising the computational linguistics depatement in Trier, Germany. 

## Getting Started

* Install
    * `npm install`

* Build
    * `brunch build`
    
* Run
    * `python server.py`

## Classification
The training corpus was the sentiment analysis corpus of kaggle's movie review challenge. The following categories are used:

  - positive
  - somewhat positive
  - neutral
  - somewhat neutral
  - negative

Two different models were used (both with linear SVM, one-vs-one classifier):
    - TF-IDF word vectors
    - doc2vec word vectors
    
The results for the TF-IDF based model were better - so it was used. Both models can be found inside
the `ai` directory.
