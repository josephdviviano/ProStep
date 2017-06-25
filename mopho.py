

from random import *
import array
import os
from patterns import *


MUT_RATE = 0.05



RESET = 126
REST=127


###########################################
# Sequencer Programming
###########################################
scale_major = [0,2,4,5,7,9,11,12]
scale_minor = [0,2,3,5,7,8,10,12]
chord_maj   = [0,4,7]
chord_maj7 = [0,4,7,11]
chord_min   = [0,3,7]
chord_dim   = [0,3,6]
chord_aug   = [0,4,8]

def Split4(pat1):
	s = pat1[0:4]
	return s+s+s+s
	
def Split2(pat1):
	s = pat1[0:2]
	return s+s+s+s+s+s+s+s
	
def Split8(pat1):
	s = pat1[0:8]
	return s+s
	
def Arp1(chord):
	o = []
	for i in range(16/len(chord)):
		o = o + chord
	if((16 % len(chord)) > 0):
		o = o + chord[0:16 % len(chord)]
	return o
	
def ProbScale(scale):
	o = []
	for i in range(16):
		c = choice(scale)
		if(random() > 0.1):
			c = c*2
		if(random() > 0.85):
			c = c + randint(1,4)*24
		o.append(c)
	return o
	
def ScaleToMopho(seq):
	o = []
	for i in range(16):
		n = seq[i]
		if(random() > 0.1):
			n = n*2		
		if(random() > 0.85):
			n = n + randint(1,4)*24
		o.append(n)
	return o
	
def Bass1(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		o.append(c)
		c = chord[1]
		o.append(c)
		c = chord[2]
		o.append(c)
	return o

def Bass2(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		c = chord[1]
		o.append(c)		
		c = chord[2]
		o.append(c)
		c = chord[0]
		o.append(c)
	return o

def Bass3(chord):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		c = chord[1]
		o.append(c)		
		c = chord[0]
		o.append(c)
		c = chord[2]
		o.append(c)	
	return o
	
def BuildSequenceI(seq):
	if(random() < 0.4): 
		return seq
	
	if(random() < 0.5):
		n = randint(0,2)
		if(n == 0):
			s = Split2(seq)
			return s
		elif(n == 1):
			s = Split4(seq)
			return s
		else:
			return Split8(seq)
	
		
	if(random() < 0.5): 
		chord = chord_min
		scale = scale_minor
		
	else: 
		chord = chord_maj
		scale = scale_major
	
	if(random() < 0.4):
		a = Arp1(chord)
		a = ScaleToMopho(a)
		return a
		
	if(random() < 0.5):
		s = ProbScale(scale)
		s = ScaleToMopho(s)
		return s
	
	
	seqo = []
	
	n = randint(0,2)
	if(n == 0):
		seqb = Bass1(chord)
	elif(n == 1):
		seqb = Bass2(chord)
	else:
		seqb = Bass3(chord)
	
	s =  seqb+seqb+seqb+seqb+seqb+seqb[0:1]
	s = ScaleToMopho(s)
	
	return s
	
def Merge(s1,s2):
	o = []
	for i in range(16):
		if(random() < 0.5):
			c = choice(s1)
		else:
			c = choice(s2)
		o.append(c)
	return o
	
def BuildSequence(seq):
	s1 = BuildSequenceI(seq)
	s2 = BuildSequenceI(seq)
	
	if(random() < 0.5): return s1
	if(random() < 0.5): return s2
	if(random() < 0.5): return s1[0:8] + s2[0:8]
	if(random() < 0.5): return s1[8:16] + s2[0:8]
	if(random() < 0.5): return s1[0:8] + s2[8:16]
	if(random() < 0.5): return s1[8:16] + s2[8:16]
	
	if(random() < 0.5): return Split4(s1)
	if(random() < 0.5): return Split2(s1)
	if(random() < 0.5): return Split8(s1)

	if(random() < 0.5): return Split4(s2)
	if(random() < 0.5): return Split2(s2)
	if(random() < 0.5): return Split8(s2)

	return Merge(s1,s2)

############################################
# Mutation Stuff
############################################
def Mutate(p):
	if(random() < MUT_RATE):
		return int(random()*255)
	return p
	
	
def Splice(p1,p2):	
	n = randint(1,len(p1)-1)
	o = p1[0:n] + p2[n:]
	for i in range(len(o)):
		o[i] = Mutate(o[i])
	return o

def Interp(p1,p2,amt=0.5):
	o = []
	for i in range(len(p1)):
		x = (1.0-amt)*p1[i] + amt*p2[i]
		x = int(x)
		o.append(Mutate(x))
	return o



############################################
# Files
############################################
def OpenFile(filename):
	f = open(filename,'rb')
	a = array.array('B')
	statinfo = os.stat(filename)
	a.fromfile(f,statinfo.st_size)
	f.close()

	return a.tolist()


############################################
# Pack/Unpack data
############################################
def PackBits(data):

	out = []
	
	for i in range(0,252,7):
		a7 = (data[i+0] & 0x80) >> 7
		b7 = (data[i+1] & 0x80) >> 6
		c7 = (data[i+2] & 0x80) >> 5
		d7 = (data[i+3] & 0x80) >> 4
		e7 = (data[i+4] & 0x80) >> 3
		f7 = (data[i+5] & 0x80) >> 2
		g7 = (data[i+6] & 0x80) >> 1
	
		d1 = a7 | b7 | c7 | d7 | e7 | f7 | g7
		d2 = data[i+0] & 0x7f
		d3 = data[i+1] & 0x7f
		d4 = data[i+2] & 0x7f
		d5 = data[i+3] & 0x7f
		d6 = data[i+4] & 0x7f
		d7 = data[i+5] & 0x7f
		d8 = data[i+6] & 0x7f
	
		out = out + [d1,d2,d3,d4,d5,d6,d7,d8]
		
	i = 252
	a7 = (data[i+0] & 0x80) >> 7
	b7 = (data[i+1] & 0x80) >> 6
	c7 = (data[i+2] & 0x80) >> 5
	d7 = (data[i+3] & 0x80) >> 4
	
	d1 = a7 | b7 | c7 | d7 
	d2 = data[i+0] & 0x7f
	d3 = data[i+1] & 0x7f
	d4 = data[i+2] & 0x7f
	d5 = data[i+3] & 0x7f
		
	out = out + [d1,d2,d3,d4,d5]
	return out	
		
def UnpackBits(data):
	out = []
	
	for i in range(0,288,8):
		
		g7 = (data[i+0] & 0x40) << 1
		f7 = (data[i+0]  & 0x20) << 2
		e7 = (data[i+0] & 0x10) << 3
		d7 = (data[i+0] & 0x8) << 4
		c7 = (data[i+0] & 0x4) << 5
		b7 = (data[i+0] & 0x2) << 6
		a7 = (data[i+0] & 0x01) << 7
	
		o1 = data[i+1] | a7
		o2 = data[i+2] | b7
		o3 = data[i+3] | c7
		o4 = data[i+4] | d7
		o5 = data[i+5] | e7
		o6 = data[i+6] | f7
		o7 = data[i+7] | g7
	
		out = out + [o1,o2,o3,o4,o5,o6,o7]
		
	
	i = 288
	e7 = (data[i+0] & 0x10) << 1
	d7 = (data[i+0] & 0x8) << 2
	c7 = (data[i+0] & 0x4) << 3
	b7 = (data[i+0] & 0x2) << 4
	a7 = (data[i+0] & 0x01) << 5
	
	o1 = data[i+1] | a7
	o2 = data[i+2] | b7
	o3 = data[i+3] | c7
	o4 = data[i+4] | d7

	out = out + [o1,o2,o3,o4]
	return out



############################################
# Sysex Data list funcs
############################################
def GET_Osc1(data):
	osc1 = data[0:6][:]
	return osc1

def SET_OSC1(data,o):
	data[0:6] = o + data[6:]
	return data
	
def GET_Osc2(data):
	osc2 = data[6:12][:]
	return osc2

def SET_OSC2(data,o):
	data = data[0:6]+o+data[12:]
	return data
	
def GET_OscMisc(data):
	return data[12:20][:]
	
def SET_OSCMISC(data,m):
	data = data[0:12] + m + data[20:]
	return data
	
def GET_Sync(data):
	return data[12][:]
	
def SET_Sync(data,sync):
	data[12] = sync
	return data
	
def GET_GlideMode(data):
	return data[13]
	
def SET_GlideMode(data,g):
	data[13] = g
	return data
	
def GET_OscSlop(data):
	return data[14]
	
def SET_OscSlop(data,slop):
	data[14] = slop
	return data
	
def GET_PBR(data):
	return data[15]
	
def SET_PBR(data,pbr):
	data[15] = pbr 
	return data
	
def GET_OscMix(data):
	return data[17] 
	
def SET_OscMix(data,mix):
	data[17] = mix
	return data
	
def GET_KeyAssign(data):
	return data[16]
	
def SET_KeyAssign(data,ka):
	data[16] = ka
	return data
	
def GET_ExtAudio(data):
	return data[18]
	
def SET_ExtAudio(data,lvl):
	data[18] = lvl
	return data
	
def GET_Oscillators(data):
	return data[0:20][:]
	
def GET_Filter(data):
	return data[20:32][:]
		
def SET_FILTER(data,f):
	data = data[0:20] + f + data[32:]
	return data
	
def GET_VCA(data):
	return data[32:41][:]

def SET_VCA(data,v):
	data = data[0:32] + v + data[41:]
	return data
	
def GET_LFO1(data):
	return data[41:46][:]

def SET_LFO1(data,l):
	data = data[0:41] + l + data[46:]
	return data
	
def GET_LFO2(data):
	return data[46:51][:]

def SET_LFO2(data,l):
	data = data[0:46] + l + data[51:]
	return data
	
def GET_LFO3(data):
	return data[51:56][:]

def SET_LFO3(data,l):
	data = data[0:51] + l + data[56:]
	return data
	
def GET_LFO4(data):
	return data[56:61][:]
	
def SET_LFO4(data,l):
	data = data[0:56] + l + data[61:]
	return data

def GET_ENV3(data):
	return data[61:70][:]
	
def SET_ENV3(data,e):
	data = data[0:61] + e + data[70:]
	return data
	
def GET_MOD1(data):
	return data[70:73][:]

def SET_MOD1(data,m):
	data = data[0:70] + m + data[73:]
	return data
	
def GET_MOD2(data):
	return data[73:76][:]

def SET_MOD2(data,m):
	data = data[0:73] + m + data[76:]
	return data

def GET_MOD3(data):
	return data[76:79][:]

def SET_MOD3(data,m):
	data = data[0:76] + m + data[79:]
	return data

def GET_MOD4(data):
	return data[79:82][:]

def SET_MOD4(data,m):	
	data = data[0:79] + m + data[82:]
	return data

def GET_MISC(data):
	return data[82:110][:]
	
def SET_MISC(data,m):
	data = data[0:82] + m + data[110:]
	return data

def GET_MODULATORS(data):
	return data[82:95][:]
	
def SET_MODULATORS(data,m):
	data = data[0:82] + m + data[95:]
	return data

def GET_Clock(data):
	return data[95:97][:]
	
def SET_CLOCK(data,m):
	data = data[0:95] + m + data[97:]
	return data

def GET_Arp(data):
	return data[97:99][:]
	
def SET_ARP(data,m):
	data = data[0:97] + m + data[99:]
	return data

def GET_SeqTrig(data):
	return data[99:101][:]
	
def GET_SeqDest(data):
	return data[101:105][:]
	
def GET_Assign(data):
	return data[105:109][:]
	
def GET_Seq1(data):
	return data[120:136][:]
	
def SET_SEQ1(data,m):
	data = data[0:120] + m + data[136:]
	return data

def GET_Seq2(data):
	return data[136:152][:]

def SET_SEQ2(data,m):
	data = data[0:136] + m + data[152:]
	return data
	
def GET_Seq3(data):
	return data[152:168][:]
	
def SET_SEQ3(data,m):
	data = data[0:152] + m + data[168:]
	return data

	
def GET_Seq4(data):
	return data[168:184][:]
	
def SET_SEQ4(data,m):
	data = data[0:168] + m + data[184:]
	return data

def GET_NAME(data):
	return data [184:200][:]
	
def BuildLFOs(lfo1,lfo2,lfo3,lfo4):
	return lfo1+lfo2+lfo3+lfo4
	
def BuildMod(env3,mod1,mod2,mod3,mod4,modulators):
	return env3+mod1+mod2+mod3+mod4+modulators
	
def BuildArp(clock,arp):
	return clock+arp
	
def BuildSeqAssign(seqtrig,seqdest,assign):
	return seqtrig+seqdest+assign
	
def BuildSeq(seq1,seq2,seq3,seq4):
	return seq1+seq2+seq3+seq4
	
def BuildData(osc1,osc2,oscmisc, filter,vca,lfos,mod,misc,seq,name):
	data = osc1 + osc2 + oscmisc + filter + vca + lfos + mod + misc 
	data = data + [0]*10
	data = data + seq + name + [0]*56
	return data


############################################
# 'Gen' Operators
############################################
def OpOSC1(p1,p2,amt=0.5):
	p1o1 = GET_Osc1(p1)
	p2o1 = GET_Osc1(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o1
	elif(n == 1):
		return Splice(p1o1,p2o1)
	elif(n == 2):
		return Interp(p1o1,p2o1,amt)
	else:
		return p2o1

def OpOSC2(p1,p2,amt=0.5):
	p1o2 = GET_Osc2(p1)
	p2o2 = GET_Osc2(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2
		
def OpOscMisc(p1,p2,amt=0.5):
	p1o2 = GET_OscMisc(p1)
	p2o2 = GET_OscMisc(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpFilter(p1,p2,amt=0.5):
	p1o2 = GET_Filter(p1)
	p2o2 = GET_Filter(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2


def OpVCA(p1,p2,amt=0.5):
	p1o2 = GET_VCA(p1)
	p2o2 = GET_VCA(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2


def OpLFO1(p1,p2,amt=0.5):
	p1o2 = GET_LFO1(p1)
	p2o2 = GET_LFO1(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2


def OpLFO2(p1,p2,amt=0.5):
	p1o2 = GET_LFO2(p1)
	p2o2 = GET_LFO2(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpLFO3(p1,p2,amt=0.5):
	p1o2 = GET_LFO3(p1)
	p2o2 = GET_LFO3(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpLFO4(p1,p2,amt=0.5):
	p1o2 = GET_LFO4(p1)
	p2o2 = GET_LFO4(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpEnv3(p1,p2,amt=0.5):
	p1o2 = GET_ENV3(p1)
	p2o2 = GET_ENV3(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2


def OpMOD1(p1,p2,amt=0.5):
	p1o2 = GET_MOD1(p1)
	p2o2 = GET_MOD1(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpMOD2(p1,p2,amt=0.5):
	p1o2 = GET_MOD2(p1)
	p2o2 = GET_MOD2(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpMOD3(p1,p2,amt=0.5):
	p1o2 = GET_MOD3(p1)
	p2o2 = GET_MOD3(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2
		
def OpMOD4(p1,p2,amt=0.5):
	p1o2 = GET_MOD4(p1)
	p2o2 = GET_MOD4(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpMOD4(p1,p2,amt=0.5):
	p1o2 = GET_MOD4(p1)
	p2o2 = GET_MOD4(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2


def OpMods(p1,p2,amt=0.5):
	p1o2 = GET_MODULATORS(p1)
	p2o2 = GET_MODULATORS(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpClock(p1,p2,amt=0.5):
	p1o2 = GET_Clock(p1)
	p2o2 = GET_Clock(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpArp(p1,p2,amt=0.5):
	p1o2 = GET_Arp(p1)
	p2o2 = GET_Arp(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2


def OpMisc(p1,p2,amt=0.5):
	p1o2 = GET_MISC(p1)
	p2o2 = GET_MISC(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpSEQ1(p1,p2,amt=0.5):
	p1o2 = GET_Seq1(p1)
	p2o2 = GET_Seq1(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpSEQ2(p1,p2,amt=0.5):
	p1o2 = GET_Seq2(p1)
	p2o2 = GET_Seq2(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpSEQ3(p1,p2,amt=0.5):
	p1o2 = GET_Seq3(p1)
	p2o2 = GET_Seq3(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpSEQ4(p1,p2,amt=0.5):
	p1o2 = GET_Seq4(p1)
	p2o2 = GET_Seq4(p2)
	n = randint(0,3)
	if(n == 0):
		return p1o2
	elif(n == 1):
		return Splice(p1o2,p2o2)
	elif(n == 2):
		return Interp(p1o2,p2o2,amt)
	else:
		return p2o2

def OpNAME(p1,p2,amt=0.5):
	p1o2 = GET_NAME(p1)
	p2o2 = GET_NAME(p2)
	return Splice(p1o2,p2o2)


trp1 =[1,0,0,0]
trp2 =[1,1,0,0]
trp3 =[1,0,1,0]
trp4 = [1,0,0,1]
trp5 = [1,1,1,0]
trp6 = [1,0,1,1]
trp7 = [1,1,1,1]

patterns = [trp1,trp2,trp3,trp7,trp4,trp5,trp6]

PROB_PAT1 = 0.8
PROB_PAT2 = 0.7
PROB_PAT3 = 0.6
PROB_PAT4 = 0.4
PROB_PAT3 = 0.5
PROB_PAT2 = 0.5
PROB_PAT1 = 0.1

def PATTERN_ProbPick():
	x = random()
	if(x < PROB_PAT1):  return trp7
	elif(x < PROB_PAT2):  return trp6
	elif(x < PROB_PAT3): return trp5
	elif(x < PROB_PAT3): return trp4
	elif(x < PROB_PAT3): return trp3
	elif(x < PROB_PAT3): return trp2
	elif(x < PROB_PAT3): return trp1
	return trp7

def PATTERN_Pick():
	return PATTERN_ProbPick()+ PATTERN_ProbPick()+  PATTERN_ProbPick()+  PATTERN_ProbPick()
		   

def MOPHO_GenerateSequence():
	keyboard = [0]*4
	pattern = GEN_CreatePattern(GEN_TYPE_ARP)
	keyboard[0] = SEQ_ScaleToMopho(pattern[0:16])
	rests = PATTERN_Pick()
	for n in range(len(keyboard[0])):
		if(rests[n] == 0): keyboard[0][n] = REST
	pattern = GEN_CreateSkew()
	keyboard[1] = pattern[0:16]
	pattern = GEN_CreateSkew()
	keyboard[2] = pattern[0:16]
	pattern = GEN_CreateSkew()
	keyboard[3] = pattern[0:16]
	return keyboard
	


###########################################
# Generation with Sequencer Mods
###########################################
def MOPHO_DoGeneration(data1,data2,num,filebase):

	for i in range(num):		
		x = random()
		osc1 = OpOSC1(data1,data2,x)
		osc2 = OpOSC2(data1,data2,x)
		oscmisc = OpOscMisc(data1,data2,x)
		filt = OpFilter(data1,data2,x)
		vca = OpVCA(data1,data2,x)
		lfo1 = OpLFO1(data1,data2,x)
		lfo2 = OpLFO2(data1,data2,x)
		lfo3 = OpLFO3(data1,data2,x)
		lfo4 = OpLFO4(data1,data2,x)
		env3 = OpEnv3(data1,data2,x)
		mod1 = OpMOD1(data1,data2,x)
		mod2 = OpMOD2(data1,data2,x)
		mod3 = OpMOD3(data1,data2,x)
		mod4 = OpMOD4(data1,data2,x)
		modulators = OpMods(data1,data2,x)
		clock  = OpClock(data1,data2,x)
		arp    = OpArp(data1,data2,x)
		misc = OpMisc(data1,data2,x)
		
		seq = MOPHO_GenerateSequence()
		seq1 = seq[0]
		seq2 = seq[1]
		seq3 = seq[2]
		seq4 = seq[3]
		
		name = OpNAME(data1,data2,x)


		clock[0] = 120
		clock[1] = 6
		arp[1] = 0
		misc[0] = 0
		misc[1] = 1
		misc[2] = 3
		misc[3] = 44
		misc[4] = 9
		misc[5] = 12

		up = osc1+osc2+oscmisc+filt+vca+lfo1+lfo2+lfo3+lfo4
		up = up + env3 + mod1 + mod2 + mod3 + mod4 + misc
		up = up + [0]*10
		up = up + seq1+seq2+seq3+seq4+name+[0]*56		
		pk = PackBits(up)
		sysx_hdr = [0xF0,0x01,0x25,0x02,0,0]
		a = array.array('B')
		a.fromlist(sysx_hdr+pk+[0xF7])
		f = open(filebase+str(i)+'.syx','wb')
		a.tofile(f)
		f.close()
	
###########################################
# Single Cross Mutation
###########################################
def MOPHO_DoMutation(data1,data2):
	x = random()
	osc1 = OpOSC1(data1,data2,x)
	osc2 = OpOSC2(data1,data2,x)
	oscmisc = OpOscMisc(data1,data2,x)
	filt = OpFilter(data1,data2,x)
	vca = OpVCA(data1,data2,x)
	lfo1 = OpLFO1(data1,data2,x)
	lfo2 = OpLFO2(data1,data2,x)
	lfo3 = OpLFO3(data1,data2,x)
	lfo4 = OpLFO4(data1,data2,x)
	env3 = OpEnv3(data1,data2,x)
	mod1 = OpMOD1(data1,data2,x)
	mod2 = OpMOD2(data1,data2,x)
	mod3 = OpMOD3(data1,data2,x)
	mod4 = OpMOD4(data1,data2,x)
	modulators = OpMods(data1,data2,x)
	clock  = OpClock(data1,data2,x)
	arp    = OpArp(data1,data2,x)
	misc = OpMisc(data1,data2,x)		
	
	seq = MOPHO_GenerateSequence()
	seq1 = seq[0]
	seq2 = seq[1]
	seq3 = seq[2]
	seq4 = seq[3]
		
	name = OpNAME(data1,data2,x)
	
	clock[0] = 120
	clock[1] = 6
	arp[1] = 0
	misc[0] = 0
	misc[1] = 1
	misc[2] = 3
	misc[3] = 44
	misc[4] = 9
	misc[5] = 12

	up = osc1+osc2+oscmisc+filt+vca+lfo1+lfo2+lfo3+lfo4
	up = up + env3 + mod1 + mod2 + mod3 + mod4 + misc
	up = up + [0]*10
	up = up + seq1+seq2+seq3+seq4+name+[0]*56		
	return up



############################################
# Breed Children + Grand children
############################################
def MOPHO_Breed(p1,p2,p3,p4,num,gsc='gc1',ps1='p1',ps2='p2'):
	
	for j in range(num):
		c1 = MOPHO_DoMutation(p1,p2)
		c2 = MOPHO_DoMutation(p3,p4)
		MOPHO_DoGeneration(c1,c2,num,gsc+str(j))
	MOPHO_DoGeneration(p1,p2,num,ps1)
	MOPHO_DoGeneration(p3,p4,num,ps2)

def MOPHO_GenOP(filename1,filename2,filename3,filename4,gsc,ps1,ps2):
	
	

	d1 = OpenFile(filename1)
	d2 = OpenFile(filename2)
	d3 = OpenFile(filename3)
	d4 = OpenFile(filename4)

	
	if(len(d1) == 298):
		n = 4
	else:
		n = 6
		
	data1 = UnpackBits(d1[n:-1])		
	
	if(len(d2) == 298):
		n = 4
	else:
		n = 6
	
	data2 = UnpackBits(d2[n:-1])
	
	if(len(d3) == 298):
		n = 4
	else:
		n = 6
	
	data3 = UnpackBits(d3[n:-1])
	
	if(len(d4) == 298):
		n = 4
	else:
		n = 6
	
	data4 = UnpackBits(d4[n:-1])

	MOPHO_Breed(data1,data2,data3,data4,20,gsc,ps1,ps2)
	
############################################
# Used to split bank file (contigous sysex patches) into individual patch syx
# Eg - The Presets come as a 'bank' file of 3x128 patches 
############################################
def MOPHO_SplitPresets():
	data = OpenFile('./Mopho_Programs_v1.0.syx')		
	for i in range(0,3):
		for j in range(0,128):
			n1 = i*127+j			
			n1 = n1 * 300
			p = data[n1:n1+300]
			a = array.array('B')
			a.fromlist(p)
			f = open('data_b'+str(i)+'p'+str(j)+'.syx','wb')
			a.tofile(f)
			f.close()
			



def MOPHO_generate():	
	files = os.listdir('../Patches')
	d = '../Patches/'
	for i in range(0,len(files),4):
		filename1 = d+files[i]
		filename2 = d+files[i+1]
		filename3 = d+files[i+2]
		filename4 = d+files[i+3]

		MOPHO_GenOP(filename1,filename2,filename3,filename4,
			'cross'+str(i),
			'mp1'+str(i),
			'mp2'+str(i))
			


###############################################
# Real time
###############################################

	
###########################################
# Single Cross Mutation
###########################################
def realtime_DoMutation(data1,data2):
	x = random()
	osc1 = OpOSC1(data1,data2,x)
	osc2 = OpOSC2(data1,data2,x)
	oscmisc = OpOscMisc(data1,data2,x)
	filt = OpFilter(data1,data2,x)
	vca = OpVCA(data1,data2,x)
	lfo1 = OpLFO1(data1,data2,x)
	lfo2 = OpLFO2(data1,data2,x)
	lfo3 = OpLFO3(data1,data2,x)
	lfo4 = OpLFO4(data1,data2,x)
	env3 = OpEnv3(data1,data2,x)
	mod1 = OpMOD1(data1,data2,x)
	mod2 = OpMOD2(data1,data2,x)
	mod3 = OpMOD3(data1,data2,x)
	mod4 = OpMOD4(data1,data2,x)
	modulators = OpMods(data1,data2,x)
	clock  = OpClock(data1,data2,x)
	arp    = OpArp(data1,data2,x)
	misc = OpMisc(data1,data2,x)		
	seq1 = OpSEQ1(data1,data2,x)
	seq2 = OpSEQ2(data1,data2,x)
	seq3 = OpSEQ3(data1,data2,x)
	seq4 = OpSEQ4(data1,data2,x)
	name = OpNAME(data1,data2,x)


	up = osc1+osc2+oscmisc+filt+vca+lfo1+lfo2+lfo3+lfo4
	up = up + env3 + mod1 + mod2 + mod3 + mod4 + misc
	up = up + [0]*10
	up = up + seq1+seq2+seq3+seq4+name+[0]*56		
	return up


###########################################
# Breed a generation
###########################################
def realtime_DoGeneration(data1,data2,num):
	gens = []
	for i in range(num):		
		x = random()
		osc1 = OpOSC1(data1,data2,x)
		osc2 = OpOSC2(data1,data2,x)
		oscmisc = OpOscMisc(data1,data2,x)
		filt = OpFilter(data1,data2,x)
		vca = OpVCA(data1,data2,x)
		lfo1 = OpLFO1(data1,data2,x)
		lfo2 = OpLFO2(data1,data2,x)
		lfo3 = OpLFO3(data1,data2,x)
		lfo4 = OpLFO4(data1,data2,x)
		env3 = OpEnv3(data1,data2,x)
		mod1 = OpMOD1(data1,data2,x)
		mod2 = OpMOD2(data1,data2,x)
		mod3 = OpMOD3(data1,data2,x)
		mod4 = OpMOD4(data1,data2,x)
		modulators = OpMods(data1,data2,x)
		clock  = OpClock(data1,data2,x)
		arp    = OpArp(data1,data2,x)
		misc = OpMisc(data1,data2,x)		
		seq1 = OpSEQ1(data1,data2,x)
		seq2 = OpSEQ2(data1,data2,x)
		seq3 = OpSEQ3(data1,data2,x)
		seq4 = OpSEQ4(data1,data2,x)
		name = OpNAME(data1,data2,x)


		up = osc1+osc2+oscmisc+filt+vca+lfo1+lfo2+lfo3+lfo4
		up = up + env3 + mod1 + mod2 + mod3 + mod4 + misc
		up = up + [0]*10
		up = up + seq1+seq2+seq3+seq4+name+[0]*56		
		
		gens.append(up)
	
	return choice(gens)
	
		
def realtime_Breed(p1,p2,p3,p4,num):		
	c1 = realtime_DoMutation(p1,p2)
	c2 = realtime_DoMutation(p3,p4)
	return realtime_DoGeneration(c1,c2,num)
	
def realtime_GenOP(filename1,filename2,filename3,filename4):
	
	p = './Patches/'
	d1 = OpenFile(p+filename1)
	d2 = OpenFile(p+filename2)
	d3 = OpenFile(p+filename3)
	d4 = OpenFile(p+filename4)

	
	if(len(d1) == 298):
		n = 4
	else:
		n = 6
		
	data1 = UnpackBits(d1[n:-1])		
	
	if(len(d2) == 298):
		n = 4
	else:
		n = 6
	
	data2 = UnpackBits(d2[n:-1])
	
	if(len(d3) == 298):
		n = 4
	else:
		n = 6
	
	data3 = UnpackBits(d3[n:-1])
	
	if(len(d4) == 298):
		n = 4
	else:
		n = 6
	
	data4 = UnpackBits(d4[n:-1])

	syx = realtime_Breed(data1,data2,data3,data4,20)
	return syx

def realtime_gen():	
	files = os.listdir('./Patches')
	filename1 = choice(files)
	filename2 = choice(files)
	filename3 = choice(files)
	filename4 = choice(files)

	return realtime_GenOP(filename1,filename2,filename3,filename4)
	
	
