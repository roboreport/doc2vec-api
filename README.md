# doc2vec-api

The repository contains some corpus(Korean), python scripts for training and inferring test document vectors using doc2vec.


Demo Site
=============
* [korean word2vec demo site](http://stockprediction.co.kr/word2vec/)

Raw Corpus
=============
* [Korean Wikipedia / space tokenizer (467MB)](https://drive.google.com/open?id=0B38stK5a3ByqcGhuUE93YnIxN0U)
* [Korean Wikipedia / mecab pos tokenizer / tag info (910MB)](https://drive.google.com/open?id=0B38stK5a3ByqZWRxS2lWMkhqQ2c)
* [Korean Wikipedia / mecab pos tokenizer / no tag info (535MB)](https://drive.google.com/open?id=0B38stK5a3ByqQWtBZ1pQWjFvWlU)

PreTrained Doc2vec Model
=============
* [Korean Wikipedia / mecab pos tokenizer / no tag info / 30 vectors(dmpv)](https://drive.google.com/open?id=0B9-yFnYCRJ-WUnpfYnd0S2Y1ZXM)
* [Korean Wikipedia / mecab pos tokenizer / no tag info / 100 vectors(dmpv)](https://drive.google.com/open?id=0B9-yFnYCRJ-WZTBDNE5odGN5a0U)
* [Korean Wikipedia / mecab pos tokenizer / no tag info / 300 vectors(dmpv)](https://drive.google.com/open?id=0B9-yFnYCRJ-WQlpUTk9wRDJ0d2c)
* [Korean Wikipedia / mecab pos tokenizer / no tag info / 1000 vectors(dmpv)](https://drive.google.com/open?id=0B9-yFnYCRJ-WSHB4TTBfb2I4REE)


Korean word2vec-api
============

Simple web service providing a word embedding API. The methods are based on Gensim Word2Vec implementation. Models are passed as parameters and must be in the Word2Vec text or binary format. This web2vec-api script is forked from [this word2vec-api github](https://github.com/3Top/word2vec-api) and get minor update to support Korean word2vec models.  

* Install Dependencies
```
pip2 install -r requirements.txt

* Launching the service
```
python word2vec-api --model path/to/the/model [--host host --port 1234]
```

* Example calls
```
curl http://127.0.0.1:5000/word2vec/most_similar?positive=무증
```






