# Arps
# Chord Sequence
# Multiple sequences evolver

# SEQ1 - Notes
# SEQ2 - Skew
# SEQ3 - Low pass envelope
# SEQ4 - Volume Accent

from random import *

PATTERN_LEN=32
MOPHO_SEQUENCER=False
PROB1 = 0.1025
PROB2 = 0.05
PROB3 = 0.015
PROB4 = 0.005
PROB_CLEAR = 0.172
PROB_SLIDE = 0.185
PROB_ACCENT = 0.1625
PROB_OCT2=0.27
PROB_OCT3 = 0.2
PROB_OCT4 = 0.1
PROB_OCT5 = 0.05
PROB_NOTE = 0.1
PROB_REST = 0.0

# Sequencer Programming
###########################################
scale_major = [0,2,4,5,7,9,11]
scale_dorian = [0,2,3,5,7,9,10]
scale_phrygian = [0,1,3,5,7,8,10]
scale_phrygian_dom = [0,1,4,5,7,8,10]
scale_lydian = [0,2,4,6,7,9,11]
scale_mixolydian = [0,2,4,5,7,9,10]
scale_aeolian = [0,2,3,5,7,8,10]
scale_locrian = [0,1,3,5,6,8,10]
scale_melodic_minor = [0,2,3,5,7,9,11]
scale_harmonic_minor = [0,2,3,5,7,8,11]
scale_harmonic_major = [0,2,4,5,7,8,11]
scale_hungarian_minor = [0,2,3,6,7,8,11]
scale_hungarian_major = [0,3,4,6,7,9,10]
scale_neapolitan_minor = [0,1,3,5,7,8,11]
scale_neapolitan_major = [0,1,3,5,7,9,11]
scale_enigmatic_minor = [0,1,3,6,7,10,11]
scale_enigmatic = [0,1,4,6,8,10,11]
scale_composite2 = [0,1,4,6,7,8,11]
scale_ionian_flat5 = [0,2,4,5,6,9,11]
scale_locrian_nat7 = [0,1,3,5,6,8,11]
scale_persian = [0,1,4,5,6,8,11]
scale_pentatonic_minor = [0,3,5,7,10]
scale_kumoi = [0,2,3,7,9]
scale_hirojoshi = [0,2,3,7,8]
scale_whole_tone = [0,2,4,6,8,10]
scale_augmented = [0,3,4,7,8,11]
scale_pelog = [0,1,3,4,7,8]
scale_domsus = [0,2,5,7,9,10]
scale_dim = [0,2,3,5,6,8,9,11]
scale_spanish = [0,1,3,4,5,6,8,9]
scale_beboplocrian2 = [0,2,3,5,6,8,10,11]
scale_bebopdom = [0,2,4,5,7,9,10,11]
scale_bebopdorian = [0,2,3,5,7,9,10,11]
scale_bebopmaj = [0,2,4,5,7,9,10,11]

Scales={}
Scales['Major'] = scale_major
Scales['Dorian'] = scale_dorian
Scales['Phrygian'] = scale_phrygian
Scales['Phrygian Dom'] = scale_phrygian_dom
Scales['Lydian'] = scale_lydian
Scales['Mixolydian'] = scale_mixolydian
Scales['Minor'] = scale_aeolian
Scales['Locrian'] = scale_locrian
Scales['Melodic Minor'] = scale_melodic_minor
Scales['Harmonic Minor'] = scale_harmonic_minor
Scales['Harmonic Major'] = scale_harmonic_major
Scales['Hungarian Minor'] = scale_hungarian_minor
Scales['Hungarian Major'] = scale_hungarian_major
Scales['Neapolitan Minor'] = scale_neapolitan_minor
Scales['Neapolitan Major'] = scale_neapolitan_major
Scales['Enigmatic Minor'] = scale_enigmatic_minor
Scales['Composite 2'] = scale_composite2
Scales['ionian b5'] = scale_ionian_flat5
Scales['locrian nat6'] = scale_locrian_nat7
Scales['Persian'] = scale_persian

scales = [scale_major, scale_dorian,scale_phrygian, scale_lydian, scale_mixolydian,
		scale_aeolian, scale_locrian, scale_melodic_minor, scale_harmonic_minor,
		scale_harmonic_major, scale_hungarian_major, scale_hungarian_minor,
		scale_neapolitan_minor, scale_neapolitan_major, scale_enigmatic_minor,
		scale_enigmatic, scale_composite2, scale_phrygian_dom,
		scale_ionian_flat5, scale_locrian_nat7, scale_persian, scale_pentatonic_minor,
		scale_kumoi, scale_hirojoshi,scale_whole_tone,scale_augmented,
		scale_pelog,scale_domsus,scale_dim,scale_spanish,scale_beboplocrian2,
		scale_bebopdom, scale_bebopdorian, scale_bebopmaj]
		
chord_maj   = [0,4,7]
chord_maj7 = [0,4,7,11]
chord_min   = [0,3,7]
chord_dim   = [0,3,6]
chord_aug   = [0,4,8]
chord_sus2 =  [0,2,7]
chord_sus4 = [0,5,7]
chord_flat5 = [0,4,6]
chord_flat6 = [0,4,7,8]
chord_minflat6 = [0,3,7,8]
chord_M6 = [0,4,7,9]
chord_m6 = [0,3,7,9]
chord_dim7 = [0,3,6,9]
chord_dbl4 = [0,5,10]
chord_dom7 = [0,4,7,10]
chord_min7 = [0,3,7,10]
chord_7sus2 = [0,2,7,10]
chord_7sus = [0,5,7,10]
chord_7b5 = [0,4,6,10]
chord_halfdim = [0,3,6,10]
chord_7domaug = [0,4,8,10]
chord_delta = [0,4,7,11]
chord_mindelta = [0,3,7,11]
chord_deltasus2 = [0,2,7,11]
chord_deltasus = [0,5,7,11]
chord_deltaflat5 = [0,4,6,11]
chord_deltadim = [0,3,6,11]
chord_deltaaug = [0,4,8,11]
chord_minordeltaaug = [0,3,8,11]
chord_9 = [0,2,4,7,10]
chord_min9 = [0,2,3,7,10]
chord_flat9 = [0,1,4,7,10]
chord_sharp9 = [ 0,3,4,7,10]
chord_delta9 = [0,2,4,7,11]
chord_mindelta9 = [0,2,3,7,11]
chord_deltaflat9 = [0,1,4,7,11]
chord_mindeltaflat9 = [0,1,3,7,11]
chord_deltasharp9 = [0,3,4,7,11]
chord_altflat5sharp9 = [0,3,4,6,10]
chord_altflat5flat9 = [0,1,4,6,10]
chord_altsharp5flat9 = [0,1,4,8,10]
chord_altsharp5sharp9 = [0,3,4,8,10]
chord_11 = [0,2,4,5,7,10]
chord_min11 = [0,2,3,5,7,10]
chord_sharp11 = [0,2,4,6,7,10]
chord_minsharp11 = [0,2,3,6,7,10]
chord_delta11 = [0,2,4,5,7,11]
chord_mindelta11 = [0,2,4,6,7,11]
chord_mindeltasharp11 = [0,2,3,6,7,11]
chord_13 = [0,2,4,5,7,9,10]
chord_min13 = [0,2,3,5,7,9,10]

chords = [chord_maj, chord_maj7,chord_min,chord_dim,chord_aug,chord_sus2,
		chord_sus4,chord_flat5, chord_flat6,chord_minflat6,chord_M6,chord_m6,
		chord_dim7,chord_min7,chord_dbl4,chord_dom7,chord_7sus2,
		chord_7sus,chord_7b5,chord_halfdim,chord_7domaug,chord_delta,
		chord_mindelta,chord_deltasus2,chord_deltasus,chord_flat5,chord_deltadim,
		chord_deltaaug,chord_minordeltaaug,chord_9,chord_min9,chord_flat9,
		chord_sharp9,chord_delta9,chord_mindelta9,chord_deltaflat9,
		chord_mindeltaflat9,chord_deltasharp9,chord_altflat5sharp9,
		chord_altflat5flat9,chord_altsharp5flat9,chord_altsharp5sharp9,
		chord_11,chord_min11,chord_sharp11,chord_minsharp11,
		chord_delta11,chord_mindelta11,chord_mindeltasharp11,
		chord_13, chord_min13]
		
root    = 0
scale  = None
chord = None






def MUSIC_SetScaleChord(s,c):
	global scale,chord
	scale = s
	chord = c
	
def MUSIC_PickScaleChord():	
	global scale,chord
	if(scale == None):
		scale = choice(scales)
	if(chord == None):
		chord = choice(chords)
	return scale,chord

MUSIC_PickScaleChord()	
################################################
#
################################################
def SEQ_Split4(pat1):
	s = pat1[0:4]
	return s+s+s+s
	
def SEQ_Split2(pat1):
	s = pat1[0:2]
	return s+s+s+s+s+s+s+s
	
def SEQ_Split8(pat1):
	s = pat1[0:8]
	return s+s
	
def SEQ_Arp1(chord,length=16):
	o = []
	for i in range(length/len(chord)):
		o = o + chord
	if((length % len(chord)) > 0):
		o = o + chord[0:length % len(chord)]
	return o

def SEQ_ArpUp(chord,length=16):
	return SEQ_Arp1(chord)
	
def SEQ_ArpDown(chord,length=16):
	arp = chord[:]
	temp = arp[0]
	arp[0] = arp[-1]
	arp[-1] = temp
	return SEQ_Arp1(arp,length)
	
def SEQ_ArpUpDown(chord,length=16):
	s1 = SEQ_ArpUp(chord)
	s2 = SEQ_ArpDown(chord)
	out = s1[0:length/2] + s2[0:length/2]
	if(length % 2 != 0): out = out + s1[0]	
	return out
	
	
	
def SEQ_ArpUp2(chord,length=16):	
	s1 = SEQ_ArpUp(chord,length)
	temp = chord[:]
	for i in range(len(temp)):
		temp[i] = temp[i] + 12
	s2 = SEQ_ArpUp(temp,length)	
	out = s1[0:length/2] + s2[0:length/2]
	if(length % 2 != 0): out = out + s1[0]	
	return out
	


def SEQ_ArpUp3(chord,length=16):
	
	s1 = SEQ_ArpUp(chord,length)
	temp = chord[:]
	for i in range(len(temp)):
		temp[i] = temp[i] + 12
	s2 = SEQ_ArpUp(temp,length)
	temp = chord[:]
	for i in range(len(temp)):
		temp[i] = temp[i] + 24
	s3 = SEQ_ArpUp(temp,length)
	
	out = s1[0:x] + s2[0:x] + s3[0:x]
	if(length % 2 != 0): out = out + s1[0]	
	return out
	


def SEQ_ArpDown2(chord,length=16):
	
	s1 = SEQ_ArpDown(chord,length)
	temp = chord[:]
	for i in range(len(temp)):
		temp[i] = temp[i] - 12
		if(temp[i] < 0): temp[i] = 0
	s2 = SEQ_ArpDown(temp,length)
	
	out = s1[0:length/2] + s2[0:length/2]
	if(length % 2 != 0): out = out + s1[0]	
	return out
	


def SEQ_ArpUp3(chord,length=16):
	s1 = SEQ_ArpDown(chord,length)
	temp = chord[:]
	for i in range(len(temp)):
		temp[i] = temp[i] -12
		if(temp[i] < 0): temp[i] = 0
	s2 = SEQ_ArpDown(temp,length)
	temp = chord[:]
	for i in range(len(temp)):
		temp[i] = temp[i] - 24
		if(temp[i] < 0): temp[i] = 0
	s3 = SEQ_ArpDown(temp,length)
	
	out = s1[0:x] + s2[0:x] + s3[0:x]
	if(length % 2 != 0): out = out + s1[0]	
	return out
	

def SEQ_Arp(chord,length=16):
	n = randint(0,3)
	if(MOPHO_SEQUENCER==True):
		if(n >= 3): n = 0
		
	if(n == 0):
		seq = SEQ_ArpUp(chord,length)
	elif(n == 1):
		seq = SEQ_ArpUpDown(chord,length)
	elif(n == 2):
		seq = SEQ_ArpDown(chord,length)
	elif(n == 3):
		seq = SEQ_ArpUp2(chord,length)
	else:
		seq = SEQ_ArpUp3(chord,length)
	return seq
	
def SEQ_ProbScale(scale,length=16):
	o = []
	for i in range(length):
		c = choice(scale)
		if(random() > 0.1):
			c = c*2
		if(random() > 0.85):
			c = c + randint(1,4)*24
		o.append(c)
	return o
	
def SEQ_ScaleToMopho(seq):
	
	#scale,chord = MUSIC_PickScaleChord()
	o = []
	last = 0
	for i in range(len(seq)):
		n = seq[i]*2
		
		if(n == -1):
			n = choice(scale)*2
			
		if(random() < PROB3):
			n = n + 1
			
		oct = 0
		x = random()
		if(x < PROB2): oct = 48
		elif(x < PROB1): oct = 24
		
		
		
		o.append(n)
	return o
	
def SEQ_Bass1(chord,length=16):
	o = []
	for i in range(length/4):
		c = chord[0]
		o.append(c)
		o.append(c)
		c = chord[1]
		o.append(c)
		c = chord[2]
		o.append(c)
	if(length % 2 != 0): o.append(chord[0])
	return o

def SEQ_Bass2(chord,length=16):
	o = []
	for i in range(length/4):
		c = chord[0]
		o.append(c)
		c = chord[1]
		o.append(c)		
		c = chord[2]
		o.append(c)
		c = chord[0]
		o.append(c)
	if(length % 2 != 0): o.append(chord[0])
	return o

def SEQ_Bass3(chord,length=16):
	o = []
	for i in range(length/4):
		c = chord[0]
		o.append(c)
		c = chord[1]
		o.append(c)		
		c = chord[0]
		o.append(c)
		c = chord[2]
		o.append(c)	
	if(length % 2 != 0): o.append(chord[0])
	return o

def SEQ_Bass4(chord,length=16):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		c = chord[2]
		o.append(c)		
		c = chord[0]
		o.append(c)
		c = chord[1]
		o.append(c)	
	return o

def SEQ_Bass5(chord,length=16):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		c = chord[2]
		o.append(c)		
		c = chord[1]
		o.append(c)
		c = chord[0]
		o.append(c)
	if(length % 2 != 0): o.append(chord[0])
	return o

def SEQ_Bass6(chord,length=16):
	o = []
	for i in range(4):
		c = chord[0]
		o.append(c)
		o.append(c)
		c = chord[2]
		o.append(c)
		c = chord[1]
		o.append(c)
	if(length % 2 != 0): o.append(chord[0])
	return o

def SEQ_Merge(s1,s2,length=16):
	o = []
	for i in range(length):
		if(random() < 0.5):
			c = choice(s1)
		else:
			c = choice(s2)
		o.append(c)
	if(length % 2 != 0): o.append(chord[0])
	return o
	


def SEQ_Gen1(scale,chord):
	
	root      = chord[0]
	second  = choice(scale)
	third      = choice(scale)
	
	n = randint(0,5)
	if(n == 0):		
		p = [root,-1,-1,-1]		
	elif(n == 1):
		p = [root,-1,root,-1]				
	elif(n == 2):
		p = [root,-1,-1,root]	
	elif(n == 3):
		p = [root,-1,root,root]
	elif(n == 4):
		p = [root,root,-1,root]
	elif(n == 5):
		p = [root,root,root,-1]
	
		
	if(random() < PROB1):
		n = randint(0,3)
		p[n] = second
		
	if(random() < PROB2):
		n = randint(0,3)
		p[n] = third
		
	return p

def SEQ_Gen2(scale,chord):	
	root      = chord[0]
	second  = choice(scale)
	third      = choice(scale)
	
	n = randint(0,4)
	
	if(n == 0):
		p = [-1,root,-1,-1]
		
	elif(n == 1):
		p = [-1,root,root,-1]
		
	elif(n  == 2):
		p = [-1,root,-1,root]
		
	elif(n == 3):
		p = [-1,-1,root,root]
	
	elif(n == 4):
		p = [-1,root,root,root]
	
	if(random() < PROB1):
		n = randint(0,3)
		p[n] = second
		
	if(random() < PROB2):
		n = randint(0,3)
		p[n] = third
		
	return p
	
	

def SEQ_Octaves(seq,shift=0):
	return SEQ_ScaleToMopho(seq)


def SEQ_BuildArp(chord,length=16):
	a = SEQ_Arp(chord,length)
	return a

def SEQ_BuildProbScale(scale,length=16):	
	s = SEQ_ProbScale(scale,length)
	return s

def SEQ_BuildBass(length=16):
	seqo = []
	#scale,chord = MUSIC_PickScaleChord()
	n = randint(0,5)
	if(n == 0):
		seqb = SEQ_Bass1(chord,length)
	elif(n == 1):
		seqb = SEQ_Bass2(chord,length)
	elif(n == 2):
		seqb = SEQ_Bass3(chord,length)
	elif(n == 3):
		seqb = SEQ_Bass4(chord,length)
	elif(n == 4):
		seqb = SEQ_Bass5(chord,length)
	else:
		seqb = SEQ_Bass6(chord,length)
	
	s =  seqb
	return s
		
def SEQ_ScalePick(scale,length=16):
	out = []
	for i in range(length):
		n = choice(scale)
		out.append(n)
	return out
	
def SEQ_GenPattern(length=16):
	global scale,chord
	
	#scale,chord = MUSIC_PickScaleChord()
	out = []
	for i in range(length):
		p1 = SEQ_Gen1(scale,chord)
		p2 = SEQ_Gen2(scale,chord)
		p3 = SEQ_Gen1(scale,chord)
		p4 = SEQ_Gen2(scale,chord)
			
		
		n = randint(0,10)
		if(n == 0):
			s = p1+p1+p1+p1
		elif(n == 1):
			s = p1+p2+p1+p2
		elif(n == 2):
			s = p1+p2+p3+p2
		elif(n == 3):
			s = p1+p1+p2+p2
		elif(n == 4):
			s = p1+p2+p3+p4
		elif(n == 5):
			s = p3+p2+p1+p2
		elif(n == 6):
			s = p3+p2+p1+p4
		elif(n == 7):
			s = p1+p3+p1+p4
		elif(n == 8):
			s = p1+p4+p3+p2
		elif(n == 9):
			s = p1+p4+p3+p2
		else:
			s = p3+p2+p4+p1
			
		
		
		if(random() < 0.25): scale = chord
		for i in range(len(s)):
			c = s[i]
			if(c == -1):
				c = choice(scale)
			out.append(c)
			
	return out[0:length]
	
	
def PAT_Pattern(length=16):
	n = randint(0,4)
	if(n == 0):
		#scale,chord = MUSIC_PickScaleChord()
		if(randint(0,1) == 0):
			p = SEQ_ProbScale(scale,length)
		else:
			p = SEQ_ProbScale(chord,length)
	else:
		p = SEQ_GenPattern(length)
	return p
	
				
def PAT_BuildPattern(seq,length=16):
	p1 = PAT_Pattern(length)
	p2 = PAT_Pattern(length)
	p   = p1+p2
	print len(p1)
	for i in range(len(seq)):
		if(p[i] != -1):
			p[i] = seq[i]
		elif(random() < PROB1):
			p[i] = seq[i]
		elif(random() < PROB2):
			p[i] = seq[i]
			
	return p
	
def PAT_ShiftRoot(seq,note):
	o = []
	for i in range(len(seq)):
		n = seq[i] + note
		o.append(n)
	return o

	
###############################################
# [----]
# [-1--]
# [--1-]
# [---1]
# [-11-]
# [-1-1]
# [--11]
# [-111]
# [1---]
# [11--]
# [1-1-]
# [1--1]
# [111-]
# [11-1]
# [1-11]
# [1111]
################################################

nLead = -1
nFollow = -1

def GEN_SetLeadFollow(l,f):
	global nLead,nFollow
	nLead = l
	nFollow = f
	
def GEN_Lead():
	n = nLead
	if(n == -1): n = randint(0,7)
	if( n == 0) : return [1,-1,-1,-1]
	elif(n ==1): return [1,1,-1,-1]
	elif(n ==2): return [1,-1,1,-1]
	elif(n ==3): return [1,-1,-1,1]
	elif(n == 4): return [1,1,1,-1]
	elif(n == 5): return [1,1,-1,1]
	elif(n == 6): return [1,-1,1,1]
	return [1,1,1,1]
	
def GEN_Follow():
	n = nFollow
	if(n == -1): n = randint(0,7)
	if(n == 0): return [-1,1,-1,-1]
	elif(n == 1): return [-1,-1,1,-1]
	elif(n == 2): return [-1,1,1,-1]
	elif(n == 3): return [-1,1,-1,1]
	elif(n == 4): return [-1,-1,1,1]
	elif(n == 5): return [-1,1,1,1,]
	return [-1,-1,-1,-1]
	
def GEN_CreateSkew(length=16):
	seq = []
	for i in range(length/16):
		p1 = GEN_Lead()
		p2 = GEN_Follow()
		s1  = p1 + p2
		for i in range(len(s1)):
			n = s1[i] 
			if(n == -1): n = randint(0,12)
			else: n = 12*randint(0,5)
			s1[i] = n
		
		
		p1 = GEN_Lead()
		p2 = GEN_Follow()
		s2   = p1 + p2
		for i in range(len(s2)):
			n = s2[i] 
			if(n == -1): n = randint(0,12)
			else: n = 12*randint(0,5)
			s2[i] = n
		
		seq = seq + s1 + s2
	return seq

	
def GEN_Fill(chord,seq):
	root = chord[0]
	o  = []
	for n in seq:
		if(n == 1):
			n = root
			if(random() < PROB1): n = choice(chord)
			elif(random() < PROB2): n = choice(chord)
		o.append(n)
	return o
	
def GEN_BasicPattern(length=16):
	
	scale,chord = MUSIC_PickScaleChord()
	o = []
	for i in range(length):
		p1 = GEN_Lead()
		p2 = GEN_Follow()
		p3 = GEN_Lead()
		p4 = GEN_Follow()
		
		seq= p1+p2+p3+p4
		if(random() < 0.5):
			seq= GEN_Fill(scale,seq)
		else:
			seq= GEN_Fill(chord,seq)
		
		o = o + seq
	return o[0:length]

def SEQ_BuildSequence(s1,s2):
	
	if(random() < PROB1): return s1
	if(random() < PROB1): return s2
	if(random() < PROB1): return s1[0:8] + s2[0:8]
	if(random() < PROB1): return s1[8:16] + s2[0:8]
	if(random() < PROB1): return s1[0:8] + s2[8:16]
	if(random() < PROB1): return s1[8:16] + s2[8:16]
	
	if(random() < PROB2): return SEQ_Split4(s1)
	if(random() < PROB2): return SEQ_Split2(s1)
	if(random() < PROB2): return SEQ_Split8(s1)

	if(random() < PROB3): return SEQ_Split4(s2)
	if(random() < PROB3): return SEQ_Split2(s2)
	if(random() < PROB3): return SEQ_Split8(s2)

	return SEQ_Merge(s1,s2)

def SEQ_BuildSequenceI(seq):
	if(random() < 0.4): 
		return seq
	
	if(random() < 0.5):
		n = randint(0,2)
		if(n == 0):
			s = SEQ_Split2(seq)
			return s
		elif(n == 1):
			s = SEQ_Split4(seq)
			return s
		else:
			s= SEQ_Split8(seq)
			return s
	
		
	
	
	if(random() < 0.4):
		a = SEQ_Arp1(chord)
		return a
		
	elif(random() < 0.5):
		s = SEQ_ProbScale(scale)
		return s
	else:
		s =  SEQ_BuildBass()
		return s
		
def GEN_ComplexPattern(length=16):	
	o = []
	for i in range(length):
		s1 = PAT_Pattern(length)
		s2 = PAT_Pattern(length)
		s3 = PAT_Pattern(length)
		s4 = PAT_Pattern(length)	
		s5 = SEQ_ScalePick(scale)
		s6 = SEQ_ScalePick(scale)
		
		seq1 = SEQ_BuildSequence(s1,s2)
		seq2 = SEQ_BuildSequence(s3,s4)
		seq3 = SEQ_BuildSequence(s5,s6)
		
		seqA = SEQ_BuildSequence(seq1,seq2)
		seqB = SEQ_BuildSequence(seq1,seq3)
		seqC = SEQ_BuildSequence(seq2,seq3)
		seq   = SEQ_BuildSequence(seqA,seqB) 
		o = o + seq
	return o[0:length]
	
def GEN_SimplePattern(length=16):		
	s1 = PAT_Pattern(length)
	seq = s1
	return seq

def GEN_BassPattern(length=16):		
	o = []
	for i in range(length):
		s1 = SEQ_BuildBass(length)
		s2 = SEQ_BuildBass(length)
		seq1 = SEQ_BuildSequence(s1,s2)
		s1 = SEQ_BuildBass(length)
		s2 = SEQ_BuildBass(length)
		seq2 = SEQ_BuildSequence(s1,s2)
		x = SEQ_BuildSequence(seq1,seq2)
		o = o + x
	return o[0:length]
	

ud1 = [0,0,0,0]
ud2 = [0,1,0,0]
ud3 = [0,0,1,0]
ud4 = [0,0,0,1]
ud5 = [1,0,0,0]
ud6 = [1,1,0,0]
ud7 = [1,0,1,0]
ud8 = [1,0,0,1]
ud9 = [1,1,1,0]
ud10 = [1,0,1,1]
ud11 = [1,1,0,1]
ud12 = [0,1,0,1]
ud13 = [0,1,1,0]
ud14 = [0,1,1,1]
ud15 = [0,0,1,1]
ud16 = [1,1,1,1]
ud = [ud1,ud2,ud3,ud4,ud5,ud6,ud7,ud8,ud9,ud10,ud11,ud12,ud13,ud14,ud15,ud16]

def PAT_UD1(length=16):
	
	for i in range(length):
		z = z + choice(ud)
		
	out = []
	for n in z:
		if(n == 1):
			if(random() > 0.5):
				n = -1
		out.append(n)
		
	return out[0:length]
	
def PAT_UD2(c,s):
	n=0
	if(s == 0):
		if(c == 0): n = 0
		elif(c == 1): n = 0
		elif(c == 2): n = 0
	elif(s==1):
		if(c == 0): n = 0
		elif(c == 1): n = 1
		elif(c == 2): n = 0
	elif(s == 2):
		if(c == 0): n = 0
		elif(c == 1): n = 0
		elif(c == 2): n = 1
	elif(s == 3):
		if(c == 0): n = 0
		elif(c == 1): n = 1
		elif(c == 2): n = 1
	elif(s == 4):
		if(c == 0): n = 1
		elif(c == 1): n = 0
		elif(c == 2): n = 0
	elif(s == 5):
		if(c == 0): n = 1
		elif(c == 1): n = 0
		elif(c == 2): n = 1
	elif(s == 6):
		if(c == 0): n = 1
		elif(c == 1): n = 1
		elif(c == 2): n = 0
	elif(s == 7):
		if(c == 0): n = 1
		elif(c == 1): n = 1
		elif(c == 2): n = 1
	elif(s == 8):
		if(c == 0): n = -1
		elif(c == 1): n = 0
		elif(c == 2): n = 0
	elif(s == 9):
		if(c == 0): n = -1
		elif(c == 1): n = -1
		elif(c == 2): n = 0
	elif(s == 10):
		if(c == 0): n = -1
		elif(c == 1): n = 0
		elif(c == 2): n = -1
	elif(s == 11):
		if(c == 0): n = -1
		elif(c == 1): n = -1
		elif(c == 2): n = -1
	elif(s == 12):
		if(c == 0): n = -1
		elif(c == 1): n = 0
		elif(c == 2): n = 1
	elif(s == 13):
		if(c == 0): n = -1
		elif(c == 1): n = 1
		elif(c == 2): n = 0
	elif(s == 14):
		if(c ==0): n = 1
		elif(c == 1): n = -1
		elif(c == 2): n = 0
	elif(s == 16):
		if(c == 0): n = 1
		elif(c == 1): n = 0
		elif(c == 2): n = -1
	
	return n
	
	
def PAT_UpDown1(length=16):
	ud = PAT_UD1(length)
	return ud
	
def PAT_UpDown2(length=16):
	u = PAT_UpDown1(length)	
	
	out = []
	for i in range(len(u)):
		c = PAT_UD2(randint(0,16),u[i])
		out.append(c)
		
		
	
	return out
	

def SEQ_UpDownH(seq):
	u = []
	l = len(seq)
	for i in range(l/16):		
		if(random() < 0.5): ud = PAT_UpDown1()
		else: ud = PAT_UpDown2()
		u = u + ud
	out = []
	for i in range(l):
		x = u[i]
		n = seq[i]
		oct = 12
		if(random() < PROB_OCT2):
			oct = oct*2
		elif(random() < PROB_OCT3):
			oct = oct*3
		
		if(x == -1): 			
			n = n - oct
			if(n<0):n=0
		elif(x == 1):
			n = n + oct
			if(n>127):n=127
		out.append(n)
	return out
		
def SEQ_UpDown(seq,length=16):
	o = []
	for i in range(length):
		o = o + SEQ_UpDownH(seq)
	return o[0:length]
	
GEN_TYPE_BASIC = 0
GEN_TYPE_SIMPLE = 1
GEN_TYPE_BASS = 2
GEN_TYPE_COMPLEX = 3
GEN_TYPE_ARP = 4
GEN_TYPE_PROB = 5
GEN_TYPE_RANDOM = 6

def GEN_CreatePattern(type = -1,length=16):
	
	global scale,chord
	if(type == -1):
		scale,chord = MUSIC_PickScaleChord()
		n = randint(0,6)
	elif(type == GEN_TYPE_RANDOM):
		n = randint(0,6)
	else:
		n = type
	
	
	if(n == GEN_TYPE_BASIC):
		seq = GEN_BasicPattern(length)
	elif(n == GEN_TYPE_SIMPLE):
		seq = GEN_SimplePattern(length)
	elif(n == GEN_TYPE_BASS):
		seq = GEN_BassPattern(length)
	elif(n == GEN_TYPE_COMPLEX):
		seq = GEN_ComplexPattern(length)
	elif( n == GEN_TYPE_ARP):
		seq = SEQ_Arp(chord,length)
	else:
		seq = SEQ_ProbScale(scale,length)
	
	
	return seq
	
def GEN_ProbPattern(length=16):
	p1 = GEN_CreatePattern(length)
	p2 = GEN_CreatePattern(length)
	
	seq = []
	for i in range(len(p1)):
		if(random() < 0.5): n = p1[i]
		else: n = p2[i]
		seq.append(n)
	return seq
	
