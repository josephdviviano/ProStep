
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities           import percentError
from mopho import *
import pickle


net_osc1 = buildNetwork(6,12,6)
net_osc2 = buildNetwork(6,12,6)
net_oscmisc = buildNetwork(8,16,8)
net_filter = buildNetwork(12,24,12)
net_vca = buildNetwork(9,18,9)
net_lfo1 = buildNetwork(5,10,5)
net_lfo2 = buildNetwork(5,10,5)
net_lfo3 = buildNetwork(5,10,5)
net_lfo4 = buildNetwork(5,10,5)
net_env3 = buildNetwork(9,18,9)
net_mod1= buildNetwork(3,8,3)
net_mod2= buildNetwork(3,8,3)
net_mod3= buildNetwork(3,8,3)
net_mod4= buildNetwork(3,8,3)
net_misc= buildNetwork(28,56,28)
net_mods= buildNetwork(13,26,13)
net_clock= buildNetwork(2,4,2)
net_arp= buildNetwork(2,4,2)
net_seq1= buildNetwork(16,32,16)
net_seq2= buildNetwork(16,32,16)
net_seq3= buildNetwork(16,32,16)
net_seq4= buildNetwork(16,32,16)

ds_osc1 = SupervisedDataSet(6,6)
ds_osc2 = SupervisedDataSet(6,6)
ds_oscmisc = SupervisedDataSet(8,8)
ds_filter = SupervisedDataSet(12,12)
ds_vca = SupervisedDataSet(9,9)
ds_lfo1 = SupervisedDataSet(5,5)
ds_lfo2 = SupervisedDataSet(5,5)
ds_lfo3 = SupervisedDataSet(5,5)
ds_lfo4 = SupervisedDataSet(5,5)
ds_env3 = SupervisedDataSet(9,9)
ds_mod1= SupervisedDataSet(3,3)
ds_mod2= SupervisedDataSet(3,3)
ds_mod3= SupervisedDataSet(3,3)
ds_mod4= SupervisedDataSet(3,3)
ds_misc = SupervisedDataSet(28,28)
ds_mods = SupervisedDataSet(13,13)
ds_clock = SupervisedDataSet(2,2)
ds_arp = SupervisedDataSet(2,2)
ds_seq1 = SupervisedDataSet(16,16)
ds_seq2= SupervisedDataSet(16,16)
ds_seq3= SupervisedDataSet(16,16)
ds_seq4= SupervisedDataSet(16,16)

name = ['B','R','A','I','N','I','A','C',32,32,32,32,32,32,32,32]
files = os.listdir('./Patches')
for i in files:
	print i
	data = OpenFile('./Patches/'+i)
	if(len(data) == 298):
		n = 4
	else:
		n = 6
		
	data = UnpackBits(data[n:-1])	
	for j in range(len(data)):
		x = data[j] / 256.0
		data[j] = x
	osc1 = GET_Osc1(data)
	
	ds_osc1.addSample(osc1,osc1)
	osc2 = GET_Osc2(data)
	ds_osc2.addSample(osc2,osc2)
	oscmisc = GET_OscMisc(data)
	ds_oscmisc.addSample(oscmisc,oscmisc)
	filt = GET_Filter(data)
	ds_filter.addSample(filt,filt)
	vca = GET_VCA(data)
	ds_vca.addSample(vca,vca)
	lfo1 = GET_LFO1(data)
	ds_lfo1.addSample(lfo1,lfo1)
	lfo2 = GET_LFO2(data)
	ds_lfo2.addSample(lfo2,lfo2)
	lfo3 = GET_LFO3(data)
	ds_lfo3.addSample(lfo3,lfo3)
	lfo4 = GET_LFO4(data)
	ds_lfo4.addSample(lfo4,lfo4)
	env3 = GET_ENV3(data)
	ds_env3.addSample(env3,env3)
	mod1 = GET_MOD1(data)
	ds_mod1.addSample(mod1,mod1)
	mod2 = GET_MOD2(data)
	ds_mod2.addSample(mod2,mod2)
	mod3 = GET_MOD3(data)
	ds_mod3.addSample(mod3,mod3)
	mod4 = GET_MOD4(data)
	ds_mod4.addSample(mod4,mod4)
	mods = GET_MODULATORS(data)
	ds_mods.addSample(mods,mods)
	clock = GET_Clock(data)
	ds_clock.addSample(clock,clock)
	arp = GET_Arp(data)
	ds_arp.addSample(arp,arp)
	misc = GET_MISC(data)
	ds_misc.addSample(misc,misc)
	seq1 = GET_Seq1(data)
	ds_seq1.addSample(seq1,seq1)
	seq2 = GET_Seq2(data)
	ds_seq2.addSample(seq2,seq2)
	seq3 = GET_Seq3(data)
	ds_seq3.addSample(seq3,seq3)
	seq4 = GET_Seq4(data)
	ds_seq4.addSample(seq4,seq4)
	
	
def Train(net,data):
	trainer = BackpropTrainer(net,data)
	for i in range(20):
		trainer.trainEpochs(25)
		
		print 'epoch %i' % i
		  
Train(net_osc1,ds_osc1)
Train(net_osc2,ds_osc2)
Train(net_oscmisc,ds_oscmisc)
Train(net_filter,ds_filter)
Train(net_vca,ds_vca)
Train(net_lfo1,ds_lfo1)
Train(net_lfo2,ds_lfo2)
Train(net_lfo3,ds_lfo3)
Train(net_lfo4,ds_lfo4)
Train(net_env3,ds_env3)
Train(net_mod1,ds_mod1)
Train(net_mod2,ds_mod2)
Train(net_mod3,ds_mod3)
Train(net_mod4,ds_mod4)
Train(net_mods,ds_mods)
Train(net_clock,ds_clock)
Train(net_arp,ds_arp)
Train(net_misc,ds_misc)
Train(net_seq1,ds_seq1)
Train(net_seq2,ds_seq2)
Train(net_seq3,ds_seq3)
Train(net_seq4,ds_seq4)

pickle.dump(net_osc1,open('osc1.net','w'))
pickle.dump(net_osc2,open('osc2.net','w'))
pickle.dump(net_oscmisc,open('oscmisc.net','w'))
pickle.dump(net_filter,open('filter.net','w'))
pickle.dump(net_vca,open('vca.net','w'))
pickle.dump(net_lfo1,open('lfo1.net','w'))
pickle.dump(net_lfo2,open('lfo2.net','w'))
pickle.dump(net_lfo3,open('lfo3.net','w'))
pickle.dump(net_lfo4,open('lfo4.net','w'))
pickle.dump(net_env3,open('env3.net','w'))
pickle.dump(net_mod1,open('mod1.net','w'))
pickle.dump(net_mod2,open('mod2.net','w'))
pickle.dump(net_mod3,open('mod3.net','w'))
pickle.dump(net_mod4,open('mod4.net','w'))
pickle.dump(net_clock,open('clock.net','w'))
pickle.dump(net_arp,open('arp.net','w'))
pickle.dump(net_misc,open('misc.net','w'))
pickle.dump(net_mods,open('mods.net','w'))
pickle.dump(net_seq1,open('seq1.net','w'))
pickle.dump(net_seq2,open('seq2.net','w'))
pickle.dump(net_seq3,open('seq3.net','w'))
pickle.dump(net_seq4,open('seq4.net','w'))