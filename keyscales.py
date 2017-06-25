import mido
from mido.ports import MultiPort
from random import *
import math
import array
from time import *
import os,glob
import threading
from patterns import *
import mopho

outp= mido.get_output_names()
inp = mido.get_input_names()

MOPHO_CHANNEL = 0x2

print "Midi Outputs"
for x in outp:
	print x
	
print "\nMidi Inputs"
for y in inp:
	print y
	
keyboard_input = mido.open_input(inp[6])
clock = mido.open_input(inp[0])
mopho_output  = mido.open_output(outp[9])
midi_input = MultiPort([keyboard_input,clock])

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
		
scale = scale_aeolian[:]
black_keys = scale_pentatonic_minor[:]

keyboard_map = {}
keyboard_map[0] = scale[0]
keyboard_map[1] = black_keys[0] 
keyboard_map[2] = scale[1]
keyboard_map[3] = black_keys[1]
keyboard_map[4] = scale[2]
keyboard_map[5] = scale[3]
keyboard_map[6] = black_keys[2]
keyboard_map[7] = scale[4]
keyboard_map[8] = black_keys[3]
keyboard_map[9] = scale[5]
keyboard_map[10] = black_keys[4]
keyboard_map[11] = scale[6]


notes = {}
name_notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

RESET = 126
REST=127


NRPN_SEQ1_STEP1 = 120
NRPN_SEQ2_STEP1 = 136
NRPN_SEQ3_STEP1 = 152
NRPN_SEQ4_STEP1 = 168

def MIDI_GenerateNotes():
	x = 0
	y = 0
	notes = {}
	for i in range(0,125,2):
		
		note = name_notes[x]
		s1 = note + str(y)
		s2 = note + str(y) + '+'
		
		notes[s1] = i
		notes[s2] = i+1
		
		x = x + 1
		x = x % len(name_notes)
		
		if x == 0: y = y + 1
		notes[i] = i
		notes[i+1] = i+1
		
	notes[126] = 126
	notes[127] = 127
	notes['REST'] = 127
	notes['RESET'] = 126
	return notes

notes = MIDI_GenerateNotes()

def MSG(msg):
	return mido.Message.from_bytes(msg)

def SendNRPN(nrpn,value):
	byte = 0xB0+MOPHO_CHANNEL	
	msb = (nrpn >> 7 ) & 0x7F
	lsb   = (nrpn & 0x7F)
	nrpn1 = [byte,0x63,msb]
	nrpn2 = [byte,0x62,lsb]
	v1 = value >> 7
	nrpn3 = [byte,0x6,v1 & 0x7F]
	nrpn4 = [byte,0x26,value & 0x7F]
	
	mopho_output.send(mido.Message.from_bytes(nrpn1))
	mopho_output.send(mido.Message.from_bytes(nrpn2))
	mopho_output.send(mido.Message.from_bytes(nrpn3))
	mopho_output.send(mido.Message.from_bytes(nrpn4))
	
def SendCC(cc,val):
	msg = [0xB0+MOPHO_CHANNEL,cc,val]
	mopho_output.send(MSG(msg))

def MOPHO_SendNRPNSeq():
	SendNRPN(98,0) # Arp Off
	SendNRPN(99,0) # Seq Trig = normal
	SendNRPN(100,1) # Gated Seq
	SendNRPN(101,3) # Seq 1 dest = osc freqs
	SendNRPN(102,44) # Seq 1 Skew
	SendNRPN(103,9) # Filter cutoff
	SendNRPN(104,12) # VCA

def MOPHO_SendNRPNArp():
	SendNRPN(98,1) # Arp Off
	SendNRPN(99,0) # Seq Trig = normal
	SendNRPN(100,0) # Gated Seq
	SendNRPN(101,3) # Seq 1 dest = osc freqs
	SendNRPN(102,44) # Seq 1 Skew
	SendNRPN(103,9) # Filter cutoff
	SendNRPN(104,12) # VCA

def MOPHO_SendNRPNOff():
	SendNRPN(98,1) # Arp Off
	SendNRPN(99,0) # Seq Trig = normal
	SendNRPN(100,0) # Gated Seq
	SendNRPN(101,3) # Seq 1 dest = osc freqs
	SendNRPN(102,44) # Seq 1 Skew
	SendNRPN(103,9) # Filter cutoff
	SendNRPN(104,12) # VCA

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
	return PATTERN_ProbPick()+ PATTERN_ProbPick()+  PATTERN_ProbPick()+		   PATTERN_ProbPick()
		   
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
	
# nrpn = first step of sequence
# step  = 0..15 for step
# value = 0..127
def MOPHO_SendSeqStep(nrpn, step,value):
	byte = 0xB0+MOPHO_CHANNEL
	nrpn_step  = nrpn+step
	msb = (nrpn_step >> 7 ) & 0x7F
	lsb   = (nrpn_step & 0x7F)
	nrpn1 = [byte,0x63,msb]
	nrpn2 = [byte,0x62,lsb]
	nrpn3 = [byte,0x6,0]
	nrpn4 = [byte,0x26,value]
	
	mopho_output.send(mido.Message.from_bytes(nrpn1))
	mopho_output.send(mido.Message.from_bytes(nrpn2))
	mopho_output.send(mido.Message.from_bytes(nrpn3))
	mopho_output.send(mido.Message.from_bytes(nrpn4))
	
def MOPHO_SendSequenceNotes(sequence_step1, seq):
	
	for i in range(len(seq)):
		MOPHO_SendSeqStep(sequence_step1,i,notes[seq[i]])

def GEN_CreateSkew():
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
	
	seq = s1 + s2
	return seq

	
def GenerateNote(note):
	x = note % 12
	y = note / 12
	
	out = keyboard_map[x] 
	return y*12+out

def MIDI_ProcessCC(msg):
	global keyboard
	cc = msg[1]
	print msg
	if(cc == 114):
		MOPHO_SendNRPNOff()	
	elif(cc == 119):
		if(msg[2] == 127):
			MOPHO_SendNRPNSeq()
			keyboard=MOPHO_GenerateSequence()
			MOPHO_SendSequenceNotes(NRPN_SEQ1_STEP1,keyboard[0])
			MOPHO_SendSequenceNotes(NRPN_SEQ2_STEP1,keyboard[1])
			MOPHO_SendSequenceNotes(NRPN_SEQ3_STEP1,keyboard[2])
			MOPHO_SendSequenceNotes(NRPN_SEQ4_STEP1,keyboard[3])				
	else:
		mopho_output.send(MSG(msg))		

def MIDI_NoteOn(msg):
	note = msg[1]
	msg[0] = 0x90 + MOPHO_CHANNEL
	msg[1] = note
	msg[2] = msg[2]
	mopho_output.send(MSG(msg))

def MIDI_NoteOff(note):
	note = msg[1]
	msg[0]  = 0x80 + MOPHO_CHANNEL
	msg[1] = note
	msg[2] = 127
	mopho_output.send(MSG(msg))

		
while 1:
	
	for m in midi_input:
		msg = m.bytes()
#		print msg
		if(msg[0] >= 0x90 and msg[0] <= 0x9F):		
			note = msg[1]
			note = GenerateNote(note)
			msg[1] = note
			MIDI_NoteOn(msg)			
		elif(msg[0] >= 0x80 and msg[0] <= 0x8F):					
			MIDI_NoteOff(msg)
			note = GenerateNote(msg[1])
			msg[1] = note
			MIDI_NoteOff(msg)
		elif(msg[0] == 176):
			MIDI_ProcessCC(msg)
		else:
			mopho_output.send(MSG(msg))
			
			