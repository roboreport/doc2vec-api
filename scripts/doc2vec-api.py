#-*- coding: utf-8 -*-

'''
Simple web service wrapping a Word2Vec as implemented in Gensim
Example call: curl http://127.0.0.1:5000/wor2vec/n_similarity/ws1=Sushi&ws1=Shop&ws2=Japanese&ws2=Restaurant
'''

from flask import Flask, request, jsonify
from flask.ext.restful import Resource, Api, reqparse
from gensim.models.doc2vec import Doc2Vec as w
from gensim import utils, matutils
from numpy import exp, dot, zeros, outer, random, dtype, get_include, float32 as REAL,\
     uint32, seterr, array, uint8, vstack, argsort, fromstring, sqrt, newaxis, ndarray, empty, sum as np_sum
from konlpy.tag import Mecab
import cPickle
import argparse
import base64
import sys
import logging
import logging.handlers





reload(sys)
sys.setdefaultencoding('utf-8')

parser = reqparse.RequestParser()



# 로거 인스턴스를 만든다
logger = logging.getLogger('mylogger')

# 포매터를 만든다
fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

# 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
fileHandler = logging.FileHandler('./doc2vec-api.log')

# 각 핸들러에 포매터를 지정한다.
fileHandler.setFormatter(fomatter)

# 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
logger.addHandler(fileHandler)

logger.setLevel(logging.DEBUG)

def filter_words(words):
    if words is None:
        return
    return [word.decode('utf-8') for word in words if word.decode('utf-8') in model.vocab]

def tokenize(sentence):
    tagger = Mecab()
    s= " ".join(tagger.morphs(sentence))
    logger.info("tokenized:" + s)
    return s


class N_Similarity(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ws1', type=str, required=True, help="Word set 1 cannot be blank!", action='append')
        parser.add_argument('ws2', type=str, required=True, help="Word set 2 cannot be blank!", action='append')
        args = parser.parse_args()
        return model.n_similarity(filter_words(args['ws1']),filter_words(args['ws2']))


class Similarity(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('w1', type=str, required=True, help="Word 1 cannot be blank!")
        parser.add_argument('w2', type=str, required=True, help="Word 2 cannot be blank!")
        args = parser.parse_args()
        return model.similarity(args['w1'], args['w2'])


class MostSimilar(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        try:
           parser.add_argument('positive', type=str, required=False, help="Positive words.", action='append')
        except Exception, e:
           print e

        parser.add_argument('negative', type=str, required=False, help="Negative words.", action='append')
        parser.add_argument('topn', type=int, required=False, help="Number of results.")
        try:
           args = parser.parse_args()
           pos = filter_words(args.get('positive', []))
        except Exception, e:
           print e

        neg = filter_words(args.get('negative', []))
        t = args.get('topn', 10)
        pos = [] if pos == None else pos
        neg = [] if neg == None else neg
        t = 10 if t == None else t
        queryinfo = "positive: " + str(pos) + " negative: " + str(neg) + " topn: " + str(t)
        logger.info(queryinfo)
        logger.info("pos 0:"+ pos[0])

        try:
           ress = model.most_similar_cosmul(positive=pos,negative=neg,topn=t)
           logger.info(ress)
           res = [word[0].encode('utf-8') for word in ress]
           logger.info(type(res))
           return res
        except Exception, e:
           print e
           print res

class Infer(Resource):
    def get(self):
        logger.info("Infer class begins:")
        parser = reqparse.RequestParser()
        parser.add_argument('words', type=str, required=True, help="word to infer vector.")
        args = parser.parse_args()
        logger.info(args['words'])
        try:
            newsline = tokenize(args['words'])
            logger.info(newsline)
            ress = model.infer_vector(newsline.split(' '))
            logger.info(ress)
            logger.info(type(ress))
            res = ress.tolist()
            logger.info(type(res)) 
            return res 
        except Exception, e:
            print e
            return
 

class Model(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('word', type=str, required=True, help="word to query.")
        args = parser.parse_args()
        try:
            res = model[args['word']]
            res = base64.b64encode(res)
            return res
        except Exception, e:
            print e
            return

class ModelWordSet(Resource):
    def get(self):
        try:
            res = base64.b64encode(cPickle.dumps(set(model.index2word)))
            return res
        except Exception, e:
            print e
            return

app = Flask(__name__)
api = Api(app)
#csrf = CsrfProtect(app)
#csrf = CSRFProtect(app)

@app.errorhandler(404)
def pageNotFound(error):
    return "page not found"

@app.errorhandler(500)
def raiseError(error):
    return error

@app.errorhandler(400)
def raiseError(error):
    return error


#@app.errorhandler(CSRFError)
#def csrf_error(reason):
#    print reason

if __name__ == '__main__':
    global model

    #----------- Parsing Arguments ---------------
    p = argparse.ArgumentParser()
    p.add_argument("--model", help="Path to the trained model")
    p.add_argument("--binary", help="Specifies the loaded model is binary")
    p.add_argument("--host", help="Host name (default: localhost)")
    p.add_argument("--port", help="Port (default: 5000)")
    p.add_argument("--path", help="Path (default: /doc2vec)")
    args = p.parse_args()

    model_path = args.model if args.model else "./model.bin.gz"
    binary = True if args.binary else False
    host = args.host if args.host else "localhost"
    path = args.path if args.path else "/doc2vec"
    port = int(args.port) if args.port else 5000
    if not args.model:
        print "Usage: doc2vec-apy.py --model path/to/the/model [--host host --port 1234]"
    model = w.load(model_path)

    api.add_resource(N_Similarity, path+'/n_similarity')
    api.add_resource(Similarity, path+'/similarity')
    api.add_resource(MostSimilar, path+'/most_similar')
    api.add_resource(Model, path+'/model')
    api.add_resource(Infer, path+'/infer')
    api.add_resource(ModelWordSet, '/doc2vec/model_word_set')
    app.run(host=host, port=port)
