from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities           import percentError
from mopho import *
import pickle


from patterns import *

nn_net = BuildNetwork(7,32,7,bias=True)
ds_net = SupervisedDataSet(7,7)

def Train(net,data):
	trainer = BackpropTrainer(net,data)
	for i in range(20):
		trainer.trainEpochs(25)
		
		print 'epoch %i' % i
		  
	
for scale in scales:
	s = [0]*7
	for i in range(len(scale)):
		if(i > 6): break
		s[i] = scale[i]
	
	y = []
	for x in s:
		t = (x/12.0)
		y.append(x)
	
	ds_net.addSample(y,y)