#-*- coding: utf-8 -*-

import gensim 
import sys
from konlpy.utils import pprint


reload(sys)
sys.setdefaultencoding('utf-8')



if __name__ == '__main__':
	print len(sys.argv) 
	modelname = sys.argv[1]
	model = gensim.models.Doc2Vec.load(modelname)
	print "정조와 가장 비슷한 단어들"
	pprint(model.most_similar(u'과징금', topn=20))
	print "배당과 비슷한 단어들"
	pprint(model.most_similar(u'배당', topn=20))
	print "왕 - 남자 + 여자 = 여왕"
	pprint(model.most_similar(positive=[u'여자', u'왕'], negative=[u'남자']))
	print "한국 - 서울 + 파리 = 프랑스"
	pprint(model.most_similar(positive=[u'파리', u'한국'], negative=[u'서울']))
	
		
	

