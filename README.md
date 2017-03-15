# Trier Sentiments
Trier Sentiments is a small web application for automatically rating movie reviews. It was used as a
small presentation for advertising the computational linguistics depatement in Trier, Germany. 

## Screenshot
<p align="center">
    <img src="https://github.com/beyeran/trier-sentiments/blob/master/screen.png?raw=true" alt="screenshot"/>
</p>

## Getting Started

* Install
    * `npm install`

* Build
    * `brunch build`
    
* Run
    * `python server.py`

## Classification
The training corpus was the sentiment analysis corpus of [kaggle's movie review challenge](https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews). These files were transformed for better usage and can be found at `ai/data`. 

The following categories are used:

  - positive
  - somewhat positive
  - neutral
  - somewhat neutral
  - negative

Two different models were used (both with linear SVM, one-vs-one classifier):
    - TF-IDF word vectors
    - doc2vec word vectors
    
The results for the TF-IDF based model were better - so it was used. Both models can be found inside
the `ai` directory. The `doc2vec` files can still be found at `ai/doc2vec_depricated` for lagacy reasons.
