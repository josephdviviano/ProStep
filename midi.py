import mido
import mido.backends.rtmidi
from mido.ports import MultiPort
import array
from time import *
import os,glob
import threading
from patterns import *
import mopho

outp= mido.get_output_names()
inp = mido.get_input_names()

MOPHO_CHANNEL=0x0
MOPHO2_CHANNEL = 0x1
MOPHOKB_CHANNEL  = 0x3
TETRA_CHANNEL = 0x4
TB3_CHANNEL = 0x0
TB32_CHANNEL = 0x1

midi_keys = None
midi_clock = None
midi_input = None
midi_output = None
sync_output = None

def MIDI_Shutdown():
	for i in range(16):
		cc = 0xB0 + i
		midi_output.send(MSG([cc,123,0]))
		sync_output.send(MSG([cc,123,0]))
		
	if(not midi_keys is None): midi_keys.close()
	if(not midi_clock is None): midi_clock.close()
	if(not midi_input is None): midi_input.close()
	if(not midi_output is None): midi_output.close()
	if(not sync_output is None): sync_output.close()
	
def MIDI_SetSyncPorts(ports):
	global sync_output
	sync_output = MultiPort(ports)
	
def MIDI_GetSyncPorts():
	return sync_output

open_outputs = []

def MIDI_Close():
	global open_outputs
	open_outputs = []
	
	try:
		midi_output.reset()
	except:
		pass
		
	try:
		midi_keys.close()
	except:
		pass
	
	try:
		sync_output.close()
	except:
		pass
			
	try:
		midi_clock.close()
	except:
		pass
		
	try:
		midi_output.close()
	except:
		pass

def MIDI_CloseOutput():
	global midi_output
	midi_output.close()
	midi_output = None
	
def MIDI_GetInOut():
	return midi_input,midi_output
	



def MIDI_SetInOut(key,clock,outp,out2=None,out3=None,out4=None):
	global midi_input,midi_output,midi_keys,midi_clock,open_outputs
	midi_input = MultiPort([key,clock])
	
	outs = []
	if(not outp is None):
		outs.append(outp)	
	if(not out2 is None):
		outs.append(out2)
	if(not out3 is None):
		outs.append(out3)
	if(not out4 is None):
		outs.append(out4)
	
	open_outputs = open_outputs+outs
	midi_output = MultiPort(outs)
	midi_keys = key
	midi_clock = clock
	
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
	for i in range(0,127):
		note = name_notes[i % 12]
		n = note + str(i / 12)
		
		notes[n] = i 
		
	return notes

notes = MIDI_GenerateNotes()

def MSG(msg):
	return mido.Message.from_bytes(msg)

def SendNRPN(nrpn,value,chan=MOPHO_CHANNEL):

	byte = 0xB0+chan
	msb = (nrpn >> 7 ) & 0x7F
	lsb   = (nrpn & 0x7F)
	nrpn1 = [byte,0x63,msb]
	nrpn2 = [byte,0x62,lsb]
	v1 = value >> 7
	nrpn3 = [byte,0x6,v1 & 0x7F]
	nrpn4 = [byte,0x26,value & 0x7F]
	
	midi_output.send(mido.Message.from_bytes(nrpn1))
	midi_output.send(mido.Message.from_bytes(nrpn2))
	midi_output.send(mido.Message.from_bytes(nrpn3))
	midi_output.send(mido.Message.from_bytes(nrpn4))
		
def SendCC(cc,val,chan=MOPHO_CHANNEL):
	msg = [0xB0+chan,cc,val]
	midi_output.send(MSG(msg))


#################################################################
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
		   

def MOPHO_SendNRPNSeq(chan):
	SendNRPN(98,0,chan) # Arp Off
	SendNRPN(99,0,chan) # Seq Trig = normal
	SendNRPN(101,1,chan) # Gated Seq
	SendNRPN(77,3,chan) # Seq 1 dest = osc freqs
	SendNRPN(78,44,chan) # Seq 1 Skew
	SendNRPN(79,9,chan) # Filter cutoff
	SendNRPN(80,12,chan) # VCA


def MOPHO_SendNRPNArp(chan):
	SendNRPN(98,1,chan) # Arp Off
	SendNRPN(99,0,chan) # Seq Trig = normal
	SendNRPN(101,0,chan) # Gated Seq
	SendNRPN(77,3,chan) # Seq 1 dest = osc freqs
	SendNRPN(78,44,chan) # Seq 1 Skew
	SendNRPN(79,9,chan) # Filter cutoff
	SendNRPN(80,12,chan) # VCA

def MOPHO_SendNRPNOff(chan):
	SendNRPN(98,1,chan) # Arp Off!
	SendNRPN(99,0,chan) # Seq Trig = normal
	SendNRPN(101,0,chan) # Gated Seq
	SendNRPN(77,3,chan) # Seq 1 dest = osc freqs
	SendNRPN(78,44,chan) # Seq 1 Skew
	SendNRPN(79,9,chan) # Filter cutoff
	SendNRPN(80,12,chan) # VCA

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
def MOPHO_SendSeqStep(nrpn, step,value,chan=MOPHO_CHANNEL):
	byte = 0xB0+chan
	nrpn_step  = nrpn+step
	msb = (nrpn_step >> 7 ) & 0x7F
	lsb   = (nrpn_step & 0x7F)
	nrpn1 = [byte,0x63,msb]
	nrpn2 = [byte,0x62,lsb]
	nrpn3 = [byte,0x6,0]
	nrpn4 = [byte,0x26,value]
	
	
	midi_output.send(mido.Message.from_bytes(nrpn1))
	midi_output.send(mido.Message.from_bytes(nrpn2))
	midi_output.send(mido.Message.from_bytes(nrpn3))
	midi_output.send(mido.Message.from_bytes(nrpn4))
	
def MOPHO_SendSequenceNotes(sequence_step1, seq, chan=MOPHO_CHANNEL):
	
	for i in range(8):
		MOPHO_SendSeqStep(sequence_step1,i,seq[i],chan)
	for i in range(8):
		MOPHO_SendSeqStep(sequence_step1,i+8,RESET,chan)

	

def GenerateNote(note):
	x = note % 12
	y = note / 12
	
	out = keyboard_map[x] 
	return y*12+out


def MOPHO_Sequencer(chan):
	MOPHO_SendNRPNSeq(chan)
	keyboard=MOPHO_GenerateSequence()
	MOPHO_SendSequenceNotes(NRPN_SEQ1_STEP1,keyboard[0],chan)
	MOPHO_SendSequenceNotes(NRPN_SEQ2_STEP1,keyboard[1],chan)
	MOPHO_SendSequenceNotes(NRPN_SEQ3_STEP1,keyboard[2],chan)
	MOPHO_SendSequenceNotes(NRPN_SEQ4_STEP1,keyboard[3],chan)				

def MIDI_GenerateNote(note):
	x = note % 12
	y = note / 12
	
	out = keyboard_map[x] 
	return y*12+out
	
def MIDI_NoteOn(note,chan=MOPHO_CHANNEL):
	msg = [0]*3
	msg[0] = 0x90 + chan
	msg[1] = note
	msg[2] = 100
	midi_output.send(MSG(msg))

def MIDI_NoteOff(note,chan = MOPHO_CHANNEL):
	msg=[0]*3
	msg[0]  = 0x80 + chan
	msg[1] = note
	msg[2] = 127
	midi_output.send(MSG(msg))

def TETRA_SendNRPNSeq(chan):
	SendNRPN(100,0,chan) # Arp Off
	SendNRPN(94,0,chan) # Seq Trig = normal
	SendNRPN(101,1,chan) # Gated Seq
	SendNRPN(77,3,chan) # Seq 1 dest = osc freqs
	SendNRPN(78,44,chan) # Seq 1 Skew
	SendNRPN(79,9,chan) # Filter cutoff
	SendNRPN(80,12,chan) # VCA

def TETRA_Sequencer(chan):
	TETRA_SendNRPNSeq(chan)
	keyboard=MOPHO_GenerateSequence()
	MOPHO_SendSequenceNotes(NRPN_SEQ1_STEP1,keyboard[0],chan)
	MOPHO_SendSequenceNotes(NRPN_SEQ2_STEP1,keyboard[1],chan)
	MOPHO_SendSequenceNotes(NRPN_SEQ3_STEP1,keyboard[2],chan)
	MOPHO_SendSequenceNotes(NRPN_SEQ4_STEP1,keyboard[3],chan)				

def TETRA_ChordOn(note):
	chord = chord_map[note % 12]
	oct     = note/12
	for n in chord:
		midi_output.send(MSG([0x90+TETRA_CHANNEL,n+oct*12,100]))
	
def TETRA_ChordOff(note):
	chord = chord_map[note % 12]
	
	oct = note/12
	for n in chord:
		midi_output.send(MSG([0x80+TETRA_CHANNEL,n+oct*12,127]))
