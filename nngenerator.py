from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.utilities           import percentError
from pybrain.structure import TanhLayer
from pybrain.structure import SoftmaxLayer
from mopho import *
import pickle

LMULT=1
net_osc1 = buildNetwork(6,LMULT*18,6)
net_osc2 = buildNetwork(6,LMULT*18,6)
net_oscmisc = buildNetwork(8,LMULT*24,8)
net_filter = buildNetwork(12,LMULT*24,12)
net_vca = buildNetwork(9,LMULT*18,9)
net_lfo1 = buildNetwork(5,LMULT*15,5)
net_lfo2 = buildNetwork(5,LMULT*15,5)
net_lfo3 = buildNetwork(5,LMULT*15,5)
net_lfo4 = buildNetwork(5,LMULT*15,5)
net_env3 = buildNetwork(9,LMULT*18,9)
net_mod1= buildNetwork(3,LMULT*9,3)
net_mod2= buildNetwork(3,LMULT*9,3)
net_mod3= buildNetwork(3,LMULT*9,3)
net_mod4= buildNetwork(3,LMULT*9,3)
net_misc= buildNetwork(28,LMULT*56,28)
net_mods= buildNetwork(13,LMULT*26,13)
net_clock= buildNetwork(2,LMULT*6,2)
net_arp= buildNetwork(2,LMULT*6,2)
net_seq1= buildNetwork(16,LMULT*32,16)
net_seq2= buildNetwork(16,LMULT*32,16)
net_seq3= buildNetwork(16,LMULT*32,16)
net_seq4= buildNetwork(16,LMULT*32,16)


net_osc1 = pickle.load(open('osc1.net'))
net_osc1.sorted = False
net_osc1.sortModules()

net_osc2 = pickle.load(open('osc2.net'))
net_osc2.sorted = False
net_osc2.sortModules()

net_oscmisc = pickle.load(open('oscmisc.net'))
net_oscmisc.sorted = False
net_oscmisc.sortModules()

net_filter = pickle.load(open('filter.net'))
net_filter.sorted = False
net_filter.sortModules()

net_vca = pickle.load(open('vca.net'))
net_vca.sorted = False
net_vca.sortModules()

net_lfo1 = pickle.load(open('lfo1.net'))
net_lfo1.sorted = False
net_lfo1.sortModules()

net_lfo2 = pickle.load(open('lfo2.net'))
net_lfo2.sorted = False
net_lfo2.sortModules()

net_lfo3 = pickle.load(open('lfo3.net'))
net_lfo3.sorted = False
net_lfo3.sortModules()

net_lfo4 = pickle.load(open('lfo4.net'))
net_lfo4.sorted = False
net_lfo4.sortModules()

net_env3 = pickle.load(open('env3.net'))
net_env3.sorted = False
net_env3.sortModules()


net_mod1 = pickle.load(open('mod1.net'))
net_mod1.sorted = False
net_mod1.sortModules()

net_mod2 = pickle.load(open('mod2.net'))
net_mod2.sorted = False
net_mod2.sortModules()

net_mod3 = pickle.load(open('mod3.net'))
net_mod3.sorted = False
net_mod3.sortModules()

net_mod4 = pickle.load(open('mod4.net'))
net_mod4.sorted = False
net_mod4.sortModules()

net_misc = pickle.load(open('misc.net'))
net_misc.sorted = False
net_misc.sortModules()

net_mods = pickle.load(open('mods.net'))
net_mods.sorted = False
net_mods.sortModules()

net_clock = pickle.load(open('clock.net'))
net_clock.sorted = False
net_clock.sortModules()

net_arp = pickle.load(open('mod1.net'))
net_arp.sorted = False
net_arp.sortModules()


net_seq1 = pickle.load(open('seq1.net'))
net_seq1.sorted = False
net_seq1.sortModules()

net_seq2= pickle.load(open('seq2.net'))
net_seq2.sorted = False
net_seq2.sortModules()

net_seq3 = pickle.load(open('seq3.net'))
net_seq3.sorted = False
net_seq3.sortModules()

net_seq4 = pickle.load(open('seq4.net'))
net_seq4.sorted = False
net_seq4.sortModules()

name = [ord('B'),ord('R'),ord('A'),ord('I'),ord('N'),ord('I'),ord('A'),ord('C'),32,32,32,32,32,32,32,32]

dosc1 = []
for i in range(6):
	dosc1.append(random())
osc1 = net_osc1.activate(dosc1)

dosc2 = []
for i in range(6):
	dosc2.append(random())
osc2 = net_osc2.activate(dosc2)

doscmisc = []
for i in range(8):
	doscmisc.append(random())
oscmisc = net_oscmisc.activate(doscmisc)

dfilt = []
for i in range(12):
	dfilt.append(random())
filt = net_filter.activate(dfilt)

dvca = []
for i in range(9):
	dvca.append(random())
vca = net_vca.activate(dvca)

dlfo1 = []
for i in range(5):
	dlfo1.append(random())
lfo1 = net_lfo1.activate(dlfo1)

dlfo2 = []
for i in range(5):
	dlfo2.append(random())
lfo2 = net_lfo2.activate(dlfo2)

dlfo3 = []
for i in range(5):
	dlfo3.append(random())
lfo3 = net_lfo3.activate(dlfo3)

dlfo4 = []
for i in range(5):
	dlfo4.append(random())
lfo4 = net_lfo4.activate(dlfo4)

denv3 = []
for i in range(9):
	denv3.append(random())
env3 = net_env3.activate(denv3)

dmod1 = []
for i in range(3):
	dmod1.append(random())
mod1 = net_mod1.activate(dmod1)

dmod2 = []
for i in range(3):
	dmod2.append(random())
mod2 = net_mod2.activate(dmod2)

dmod3 = []
for i in range(3):
	dmod3.append(random())
mod3 = net_mod3.activate(dmod3)

dmod4 = []
for i in range(3):
	dmod4.append(random())
mod4 = net_mod4.activate(dmod4)

dmisc = []
for i in range(28):
	dmisc.append(random())
misc = net_misc.activate(dmisc)

dseq1 = []
for i in range(16):
	dseq1.append(random())
seq1 = net_seq1.activate(dseq1)

dseq2 = []
for i in range(16):
	dseq2.append(random())
seq2 = net_seq2.activate(dseq2)

dseq3 = []
for i in range(16):
	dseq3.append(random())
seq3 = net_seq3.activate(dseq3)

dseq4 = []
for i in range(16):
	dseq4.append(random())
seq4 = net_seq4.activate(dseq4)

def ToBytes(data):
	out = []
	for d in data:
		d = ((d-0.1)/0.8)
		d = d*0.5+1.0
		x =abs(int(d*127.0))
		out.append(x)
	return out
	
osc1 = ToBytes(osc1)
osc2 = ToBytes(osc2)
oscmisc = ToBytes(oscmisc)
filt = ToBytes(filt)
vca = ToBytes(vca)
lfo1 = ToBytes(lfo1)
lfo2 = ToBytes(lfo2)
lfo3 = ToBytes(lfo3)
lfo4 = ToBytes(lfo4)
env3 = ToBytes(env3)
mod1 = ToBytes(mod1)
mod2 = ToBytes(mod2)
mod3 = ToBytes(mod3)
mod4 = ToBytes(mod4)
misc = ToBytes(misc)
seq1 = ToBytes(seq1)
seq2 = ToBytes(seq2)
seq3 = ToBytes(seq3)
seq4 = ToBytes(seq4)

up = list(osc1)+list(osc2)+list(oscmisc)+list(filt)+list(vca)+list(lfo1)+list(lfo2)+list(lfo3)+list(lfo4)
up = up + list(env3) + list(mod1) + list(mod2) + list(mod3) + list(mod4) + list(misc)
up = up + [0]*10
up = up + list(seq1)+list(seq2)+list(seq3)+list(seq4)+name+[0]*56	

print up
filebase='brainiac.syx'
pk = PackBits(up)
sysx_hdr = [0xF0,0x01,0x25,0x02,0,0]
a = array.array('B')
a.fromlist(sysx_hdr+pk+[0xF7])
f = open(filebase,'wb')
a.tofile(f)
f.close()