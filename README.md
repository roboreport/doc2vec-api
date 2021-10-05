# doc2vec-api

The repository contains some corpus(Korean), python scripts for training and inferring test document vectors using doc2vec.


Demo Site
=============
* [korean word2vec/doc2vec demo site](http://121.78.145.40/word2vec/)

Raw Corpus
=============
* [Korean Wikipedia / space tokenizer (467MB)](https://drive.google.com/file/d/0B38stK5a3ByqcGhuUE93YnIxN0U/view?resourcekey=0-YfafP3hxayjxBBXpy5RIsA)
* [Korean Wikipedia / mecab pos tokenizer / tag info (910MB)](https://drive.google.com/file/d/0B38stK5a3ByqZWRxS2lWMkhqQ2c/view?usp=sharing&resourcekey=0-c7VTtwcwcxapPrKSwYwivg)
* [Korean Wikipedia / mecab pos tokenizer / no tag info (535MB)](https://drive.google.com/file/d/0B38stK5a3ByqQWtBZ1pQWjFvWlU/view?usp=sharing&resourcekey=0-F__wBgRZg1nn6oJ5DUVbaw)

PreTrained Doc2vec Model
=============
* [Korean Wikipedia / mecab pos tokenizer / no tag info / 30 vectors(dmpv)](https://drive.google.com/file/d/0B9-yFnYCRJ-WUnpfYnd0S2Y1ZXM/view?usp=sharing&resourcekey=0-U3GKEwNwWH5Q3yEHi7sNxA)
* [Korean Wikipedia / mecab pos tokenizer / no tag info / 100 vectors(dmpv)](https://drive.google.com/file/d/0B9-yFnYCRJ-WZTBDNE5odGN5a0U/view?usp=sharing&resourcekey=0-pvmWQI-mgH4XWMVX3ZMg5g)
* [Korean Wikipedia / mecab pos tokenizer / no tag info / 300 vectors(dmpv)](https://drive.google.com/file/d/0B9-yFnYCRJ-WQlpUTk9wRDJ0d2c/view?usp=sharing&resourcekey=0-w88xtciCgmp4PcBKKjUwgw)
* [Korean Wikipedia / mecab pos tokenizer / no tag info / 1000 vectors(dmpv)](https://drive.google.com/file/d/0B9-yFnYCRJ-WSHB4TTBfb2I4REE/view?usp=sharing&resourcekey=0-TQ3rTx-aIVGiNy6eS5YdHw)

* [Korean Wikipedia + financial news / mecab pos tokenizer / no tag info / 30 vectors(dmpv)](https://drive.google.com/file/d/0B38stK5a3ByqZE1Wa3VGQlhJVFk/view?usp=sharing&resourcekey=0-Wc-yDyGR_4RtUeDwg3hS9w)
* [Korean Wikipedia + financial news / mecab pos tokenizer / no tag info / 100 vectors(dmpv)](https://drive.google.com/file/d/0B38stK5a3ByqSUFEQ3ktUlRRaWc/view?usp=sharing&resourcekey=0-eH9X8wwz9qu54uala6S2kA)


Korean word2vec-api / doc2vec-api
============

Simple web service providing a word embedding API. The methods are based on Gensim Word2Vec / Doc2Vec implementation. Models are passed as parameters and must be in the Word2Vec / Doc2Vec text or binary format. This web2vec-api script is forked from [this word2vec-api github](https://github.com/3Top/word2vec-api) and get minor update to support Korean word2vec models.  

* Install Dependencies
```
pip2 install -r requirements.txt
```

* Launching the service
```
python word2vec-api --model path/to/the/model [--host host --port 1234]
ex) python /home/word2vec-api.py --model /home/model/all_terms_50vectors --path /word2vec --host 0.0.0.0 --port 4000


python doc2vec-api --model path/to/the/model [--host host --port 1234]
ex) python /home/doc2vec-api.py --model /home/model/all_terms_50vectors --path /doc2vec --host 0.0.0.0 --port 4000


```

* Example calls
```
curl http://127.0.0.1:5000/word2vec/most_similar?positive=무증
```






