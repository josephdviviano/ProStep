from mido import Message, MidiFile, MidiTrack
from patterns import *
from random import *


PROB1 = 0.18
PROB2 = 0.18
PROB3 = 0.09

midi = MidiFile()


trp1 =[1,0,0,0]
trp2 =[1,1,0,0]
trp3 =[1,0,1,0]
trp4 = [1,0,0,1]
trp5 = [1,1,1,0]
trp6 = [1,0,1,1]

drum_patterns = [trp1,trp2,trp3,trp4,trp5,trp6]
measures         = 1

def DRUM_PickPattern():
	n = randint(0,5)
	return TR8_ToHex(drum_patterns[n])
	
def DRUM_GenPattern():
	pattern1 = TR8_PickPattern()
	pattern2 = TR8_PickPattern()
	pattern3 = TR8_PickPattern()
	pattern4 = TR8_PickPattern()
	out = pattern1 << 12 | pattern2 << 8| pattern3 << 4 | pattern4
	return out
	

def PATTERN_Octave(c,oct=36,shift=0):		
	if(c != -1):		
		if(random() < PROB1): oct -= 12
		elif(random() < PROB2): oct += 12
		elif(random() < PROB3): oct += 24
		c = oct + c + shift
	return c

def PATTERN_Octaves(seq,oct=36,shift=0):
	global scale
	o = []	
	shift = choice(scale)
	for i in range(len(seq)):
		c = PATTERN_Octave(seq[i],oct,shift)		
		o.append(c)
	return o

def MIDI_GenTrackPattern(chan):
	track = MidiTrack()
	midi.tracks.append(track)
	ticks = midi.ticks_per_beat
	oct = choice([24,36])
	p   = GEN_CreatePattern(GEN_TYPE_ARP) + GEN_CreatePattern(GEN_TYPE_ARP)
	p   = PATTERN_Octaves(p,oct)
	
	n = 0	
	while n < len(p):
		if(p[n] == -1):	p[n] = 24
		t = ticks/4
		track.append(Message('note_on',channel=chan,note=p[n],velocity=80+randint(0,47),time=0))						
		track.append(Message('note_off',channel=chan,note=p[n],velocity=127,time=t))
		
			
		n = n + 1

for i in range(128):		
	file = 'pattern'+str(i)+'.mid'
	
	for j in range(16):
		MIDI_GenTrackPattern(j)
	midi.save(file)
	