#python example to infer document vectors from trained doc2vec model
import gensim
import codecs
import sys

print len(sys.argv)
if len(sys.argv) < 4:
	model="model/doc2vec.model"
	test_docs="data/sample.txt"
	output_file="data/test_vectors.txt"
else:
	model = sys.argv[1]
	test_docs = sys.argv[2]
	output_file= sys.argv[3]

#inference parameters
start_alpha=0.01
infer_epoch=1000

#load model
m = gensim.models.Doc2Vec.load(model)
test_docs = [ x.strip().split() for x in codecs.open(test_docs, "r", "utf-8").readlines() ]

#infer test vectors
output = codecs.open(output_file, "w", "utf-8")
for d in test_docs:
    output.write( " ".join([str(x) for x in m.infer_vector(d, alpha=start_alpha, steps=infer_epoch)]) + "\n" )
output.flush()
output.close()
