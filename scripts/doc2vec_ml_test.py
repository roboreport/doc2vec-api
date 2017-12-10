#-*- coding: utf-8 -*-

import gensim 
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC


reload(sys)
sys.setdefaultencoding('utf-8')


def run_test(models, category, algorithm, foldnum=10):
        train_max = ( len(category) // foldnum ) * (foldnum-1)
        train_x = models[:train_max]
        train_y = category[:train_max]
        test_x = models[train_max+1:len(category)]
        test_y = category[train_max+1:len(category)]
        if algorithm == "logistic":
                classifier = LogisticRegression(random_state=1234)
        elif algorithm == "mlp":
                classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        else:
                classifier = SVC(kernel='linear')

        classifier.fit(train_x, train_y)
        accuracy = classifier.score(test_x, test_y)
        print "accuracy:"+str(accuracy)


if __name__ == '__main__':

	print len(sys.argv) 
	modelname = sys.argv[1]
	filename =  sys.argv[2]
	if len(sys.argv) == 4:
		algorithm = sys.argv[3]

	model = gensim.models.Doc2Vec.load(modelname)

	with open(filename, 'r') as f:
	    lines = f.readlines()
	results = [line.split('\t',1) for line in lines]
	category = [];
	models = [];

	for result in results:
		if len(result) == 2:
			category.append(result[0])
			newsline = result[1].strip().replace(',', ' ')
			modelline = model.infer_vector(newsline.split(' '))
			models.append(modelline)

	if len(sys.argv) == 4:
		run_test(models, category, algorithm)



