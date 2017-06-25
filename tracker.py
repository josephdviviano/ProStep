from random import *
import mido
from mido.ports import MultiPort
import array
from time import *
import os,glob
import threading
from patterns import *
import mopho
from midi import *


PPQ_SIXTEENTH=6
PPQ_EIGTH=12
PPQ_QUARTER=24
PPQ_HALF=48
PPQ_WHOLE=96
PPQ_QUARTER_TRIPLETS=8
PPQ_EIGTH_TRIPLETS=4
PPQ_THIRTY2ND = 3

NOTE_C = 0
NOTE_D = 2
NOTE_E = 4
NOTE_F = 5
NOTE_G = 7
NOTE_A = 9
NOTE_B = 11

def Sharp(note):
	x = note+1
	if(x > 127): x = 127
	return x
	
def Flat(note):
	x = note - 1
	if(x < 0): x = 11
	return x
	
def Octave(oct,note):
	o = oct*12
	n = o + note
	return n
	
PROB1 = 0.05
PROB2 = 0.075
PROB3 = 0.08

def ScaleSequence(seq,oct=36):
	out = []
	for note in seq:
		if(random() < PROB1):
			out.append(note+oct+12)
		elif(random() < PROB2):
			x = note+(oct-12)
			out.append(x)
		elif(random() < PROB3):
			out.append(-1)
		else:
			out.append(note+oct)
	return out

gt1 = [4,4,-1,-1]
gt2 = [4,2,2,-1]
gt3 = [4,2,1,1]
gt4 = [2,2,2,2,2,2,2]
gt5 = [2,2,4,-1]
gt6 = [2,4,2,-1]
gt7 = [1,1,2,4]
gt8 = [2,1,1,4]
gt9 = [2,4,1,1]
gt10 = [1,1,1,1]
timings = [gt1,gt2,gt3,gt4,gt5,gt6,gt7,gt8,gt9,gt10]

def GenTiming():
	t = choice(timings)
	out = []
	for x in t:
		if( x == 1): out.append(PPQ_SIXTEENTH)
		if( x == 2): out.append(PPQ_EIGTH)
		if( x == 4): out.append(PPQ_QUARTER)
		if( x == -1): out.append(-1)
	return out
	
def GenTiming4():
	return GenTiming() + GenTiming() + GenTiming() + GenTiming()
	
def GEN_CreateSequence():
	return GEN_CreatePattern(GEN_TYPE_BASS)
	


num_patterns = 4
cur_step = 0
cur_pattern = 0
ppq=0

###########################################
# Encapsulate pattern data
###########################################
class Pattern:
	
	def __init__(self):
		self.pattern = []
		self.timing  = []
		
	def AddNoteTime(self,note,time):
		self.pattern.append((note,time))
	
	def GetNote(self,step):
		return self.pattern[step][0]
		
	def GetTime(self,step):
		return self.pattern[step][1]
		
	def UnfoldNotes(self):
		out = []
		for i in range(len(self.pattern)):
			out.append(self.pattern[i][0])
		return out
		
	def UnfoldTime(self):
		out = []
		for i in range(len(self.pattern)):
			out.append(self.pattern[i][1])
		return out
		
	def Steps(self):
		return len(self.pattern)
		
############################################
# Encapsulate track around instrument
############################################
class Instrument:
	
	def __init__(self,chan):
		
		self.chan = chan
		self.cur_step = 0
		self.cur_pattern = 0
		self.total_patterns = 0
		self.patterns = []
		self.chords = []
		self.total_chords = 0
		self.ppq = 0
		
	def AddChord(self,chord):
		self.chords[self.total_chords] = chord
		self.total_chords = self.total_chords+1
		
	def AddPattern(self,pattern):
		self.patterns.append(pattern)
		self.total_patterns = self.total_patterns+1

	def AddTiming(self,timing):
		self.pattern_timing[self.total_timing] = timing
		self.total_timing = self.total_timing+1
		
	def Start(self):
		note = self.patterns[self.cur_pattern].GetNote(cur_step)
		if(note  != -1): MIDI_NoteOn(note)
		
	def Tick(self):
		
		self.ppq = self.ppq+1
		ctime = self.patterns[self.cur_pattern].GetTime(self.cur_step)
		
			
		if(self.ppq >= ctime):
			note = self.patterns[self.cur_pattern].GetNote(self.cur_step)
			
			if(note  != -1): MIDI_NoteOff(note)
			
			if( ctime != -1):
				self.ppq = 0
			
			
			self.cur_step = self.cur_step + 1
			if(self.cur_step >= self.patterns[self.cur_pattern].Steps()):
				self.cur_step = 0
				self.cur_pattern = self.cur_pattern + 1
				self.cur_pattern = self.cur_pattern % self.total_patterns
			
			note = self.patterns[self.cur_pattern].GetNote(self.cur_step)			
			if( note != -1):			
				MIDI_NoteOn(note)
			
			
class Track:
	
	def __init__(self):
		self.track = []
		self.midi_msg =  {}
		self.cur_step = 0
		self.cur_measure = 0
		self.ppq = 0
		
	def AddInstrument(self,instrument):
		self.track.append(instrument)
	
	
	def AddMidiMsg(self,measure, msg):
		self.midi_msg[measure] = msg
		
	def Tick(self):
		self.track[self_cur_step].Tick()
		self.ppq = self.ppq + 1
		if(self.ppq >= PPQ_WHOLE):
			self.cur_step = self.cur_step + 1
			self.cur_step = self.cur_step % len(self.track)
			self.cur_measure = self.cur_measure + 1
			

def CreatePattern(pattern1,pattern,ptime):
	for j in range(4):
		for i in range(len(pattern[j])):
			note = pattern[j][i]
			if(i >= len(ptime[j])):
				ntime = -1
			else:
				ntime = ptime[j][i]
			pattern1.AddNoteTime(note,ntime)

mopho = Instrument(MOPHO_CHANNEL)
tetra    = Instrument(TETRA_CHANNEL)


pattern = {}
pattern[0] = [ notes['C3'],notes['C3'],notes['C2'],notes['C3'] ]
pattern[1] = [ notes['C3'],notes['C3'],notes['C2'],notes['C3'] ]
pattern[2] = [ notes['C3'],notes['C3'],notes['C2'],notes['C3'] ]
pattern[3] = [ notes['C3'],notes['C3'],notes['C2'],notes['C4'] ]


ptime = {}

ptime[0] = [PPQ_QUARTER,PPQ_EIGTH,PPQ_EIGTH,-1]
ptime[1] = [PPQ_EIGTH,PPQ_EIGTH,PPQ_QUARTER,-1]
ptime[2] = [PPQ_QUARTER,PPQ_EIGTH,PPQ_EIGTH,-1]
ptime[3] = [PPQ_EIGTH,PPQ_EIGTH,PPQ_EIGTH,PPQ_EIGTH]

pattern1 = Pattern()

CreatePattern(pattern1,pattern,ptime)

pattern[0] = GEN_CreateSequence()
pattern[1] = GEN_CreateSequence()
pattern[2] = GEN_CreateSequence()
pattern[3] = GEN_CreateSequence()
pattern[0] = ScaleSequence(pattern[0])
pattern[1] = ScaleSequence(pattern[1])
pattern[2] = ScaleSequence(pattern[2])
pattern[3] = ScaleSequence(pattern[3])

ptime[0] = GenTiming4()
ptime[1] = GenTiming4()
ptime[2] = GenTiming4()
ptime[3] = GenTiming4()
pattern2 = Pattern()
CreatePattern(pattern2,pattern,ptime)
mopho.AddPattern(pattern2)


mopho.Start()		
while 1:
	
	for msg in midi_input:
		key = msg.bytes()
		if(key[0] == 248):
			mopho.Tick()
			midi_output.send(MSG(key))
			
			