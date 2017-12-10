#-*- coding: utf-8 -*-

#import gensim 
import sys
import argparse
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.externals import joblib
from konlpy.utils import pprint
import logging
import logging.handlers




reload(sys)
sys.setdefaultencoding('utf-8')

# 로거 인스턴스를 만든다
logger = logging.getLogger('mylogger')

# 포매터를 만든다
fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

# 스트림과 파일로 로그를 출력하는 핸들러를 각각 만든다.
fileHandler = logging.FileHandler('./ml_test.log')

# 각 핸들러에 포매터를 지정한다.
fileHandler.setFormatter(fomatter)

# 로거 인스턴스에 스트림 핸들러와 파일핸들러를 붙인다.
logger.addHandler(fileHandler)

logger.setLevel(logging.DEBUG)


def run_test(train_x, train_y, test_x, test_y, algorithm):
	save_infervec(train_y, train_x, "trainvecfile.txt")
	save_infervec(test_y, test_x, "testvecfile.txt")
        if algorithm == "linear":
		train_y = map(float, train_y)
		test_y = map(float, test_y)
		classifier = LinearRegression()
	elif algorithm == "logistic":
                classifier = LogisticRegression(random_state=1234)
        elif algorithm == "mlp":
                classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        else:
                classifier = SVC(kernel='linear')
		algorithm = "svm"
        classifier.fit(train_x, train_y)
        accuracy = classifier.score(test_x, test_y)
        print "algorith:"+algorithm+" accuracy:"+str(accuracy)
	clsfile = algorithm + ".pkl"
	joblib.dump(classifier, clsfile) 

	predicted_y = classifier.predict(test_x)
	print_prediction(test_y, predicted_y)
	return predicted_y

def print_prediction(test_y, predicted_y):
	for i,test_y_unit in enumerate(test_y):
		print str(test_y[i]) + ":" + str(predicted_y[i])

def print_testaccuracy(test_y, predicted_y):
        i = 0
	correct = 0
	incorrect = 0
	threshold = -0.0001 
        for result in predicted_y:
                print str(test_y[i]) + ":" + str(predicted_y[i])
		if threshold <= predicted_y[i] <= abs(threshold):
			print "predicted_y is close to 0" + str(predicted_y[i])
		else:
			if test_y[i] > 0 and predicted_y[i] > 0:
				correct = correct + 1
			elif test_y[i] < 0 and predicted_y[i] < 0:
				correct = correct + 1
			else:
				incorrect = incorrect + 1
		i = i + 1
	total = float(correct + incorrect)	
	correct_per = float(correct/total) * 100
	incorrect_per = float(incorrect/total) * 100
	print "correct:" + str(correct) + " incorrect:" + str(incorrect) + "\n"
	print "correct:" + str(correct_per) + " incorrect:" + str(incorrect_per) + "\n"

def split_dataset(models, category, foldnum=10):
	train_max = ( len(category) // foldnum ) * (foldnum-1)
        train_x = models[:train_max]
        train_y = category[:train_max]
        test_x = models[train_max+1:len(category)]
        test_y = category[train_max+1:len(category)]
        save_infervec(train_y, train_x, "trainvecfile.txt")
        save_infervec(test_y, test_x, "testvecfile.txt")
	return (train_x, train_y, test_x, test_y) 


def save_infervec(category, models, filename):
	#save_arff_header(filename, 20)
	with open(filename, 'a') as fout:
		for index,item in enumerate(category):
			model_unit = ','.join(str(e) for e in models[index])
			line = str(model_unit) + "," + str(category[index]) + "\n"
        		fout.write(line)


def infer_features(lines, args):
	category = [];
	results = [line.strip().split('\t') for line in lines]
	infercollist = args.infercols.split(',')

        len_of_features = len(results[0]) -1
	features = []
	if args.infercols is None:
		features = [result[1:len_of_features] for result in lines]
	else:
		import gensim
		model = gensim.models.Doc2Vec.load(args.modelname)
		for result in results:
			if(len(result) < 2): 
				continue;
			else:
                        	category.append(float(result[0]))

			for i in range(1,len(results[0])):    
				if str(i) in infercollist:
					logger.debug(result[i])
					models = model.infer_vector(result[i])
				else:
					models = result[i]
				if i == 1:
					feature = models
				else:
					feature = np.hstack((feature, models))
			features.append(feature)
	logger.debug(features)
	features = np.array(features, dtype=np.float32)
	return (category, features)


def infer_vectors(lines, modelname):
        import gensim
        models = [];
        model = gensim.models.Doc2Vec.load(modelname)
        for unit in lines:
                print "unit" + str(unit)
                line = unit.strip().replace(',', ' ')
                vectors = model.infer_vector(line.split(' '))
                models.append(vectors)
	print "doc2vec size:" + str(len(models))
        return models


def get_dataset(lines, args):
	category = [];
        models = [];
	results = [line.split('\t') for line in lines]
	colnum = len(results[0])
	for result in results:
		if args.classcol == "last":
			models.append(result[0:colnum-1])
			category.append(result[-1])
		else:
			models.append(result[1:colnum])
			category.append(result[0])
	return (category, models)

		

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	# all argument are optional now --
	parser.add_argument("-f", "--filename", help="input file for training and test")
	parser.add_argument("-m", "--modelname", help="doc2vec model file name")
	parser.add_argument("-a", "--algorithm", help="choose ML algorithm among linear/logistic/mlp/svm")
	parser.add_argument("-o", "--option", help="infer(infer document vectors)or test(ml test) or all(infer+ml test)")
	parser.add_argument("-t", "--testfile", help="separate test file" )
	parser.add_argument("-c", "--classcol", help="first or last")
	parser.add_argument("-s", "--save", help="save train model file")
	parser.add_argument("-p", "--predict", help="print predicted result of test file")
	parser.add_argument("-i", "--infercols", help="colum nums to be infered ex) -i=2,4")
	parser.add_argument("-d", "--delimiter", help="delimiter of files ex) -d=,")
	#python ml_test.py -f  /home/data/marketeye/marketeye_1day_train.txt  -o test -c first -a logistic -s y

	args = parser.parse_args()
    	predict = True if args.predict else False
	skip = True if args.save else False 
	
	
	category = [];
	models = [];

	with open(args.filename, 'r') as f:
		lines = f.read().splitlines()		
	
	if args.testfile is not None:
		with open(args.testfile, 'r') as tf:
			testlines = tf.readlines()
		
	if (args.option == "infer"):
		(category, models) = infer_vectors(lines, args.modelname)
		save_infervec(category, models, "infferedvec.txt")

	elif (args.option == "test"):
		(category, models) = get_dataset(lines, args)	
		models = np.array(models, dtype=np.float32)
		(train_x, train_y, test_x, test_y) = split_dataset(models, category)
		run_test(train_x, train_y, test_x, test_y , args.algorithm)
	elif (args.option == "all"):
		if args.testfile is None:
			(category, models) = infer_vectors(lines, args.modelname)
                        (train_x, train_y, test_x, test_y) = split_dataset(models, category)
		else:
			(train_y, train_x) = infer_features(lines, args)			 	
			(test_y, test_x) = infer_features(testlines, args)			 	
		run_test(train_x, train_y, test_x, test_y , args.algorithm)
