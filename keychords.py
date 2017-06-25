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
from midi import *


midi_gate = [1,0,0,1,1,0,0,0,1,0,0,0,0,0,1,1]

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

KEY_C = 0
KEY_D = 2
KEY_E = 4
KEY_F = 5
KEY_G = 7
KEY_A = 9
KEY_B = 11

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


chord_map = {}
chord_map[KEY_C] = chord_min
chord_map[KEY_C+1] = chord_min
chord_map[KEY_D] = chord_dim
chord_map[KEY_D+1] = chord_dim
chord_map[KEY_E] = chord_maj
chord_map[KEY_F] = chord_maj
chord_map[KEY_F+1] = chord_maj
chord_map[KEY_G] = chord_min
chord_map[KEY_G+1] = chord_min
chord_map[KEY_A] = chord_min
chord_map[KEY_A+1] = chord_min
chord_map[KEY_B] = chord_maj


notes = {}
name_notes = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

RESET = 126
REST=127


NRPN_SEQ1_STEP1 = 120
NRPN_SEQ2_STEP1 = 136
NRPN_SEQ3_STEP1 = 152
NRPN_SEQ4_STEP1 = 168

clock = 0
last_note = -1
cur_step = 0
use_gate = 0

while 1:
	
	for m in midi_input:
		msg = m.bytes()
		
		
		if(msg[0] == 0x90+MOPHOKB_CHANNEL):			
			note = msg[1]
			last_note = note
			TETRA_ChordOn(note+12)			
		elif(msg[0] == 0x80 + MOPHOKB_CHANNEL):
			note = msg[1]
			TETRA_ChordOff(note+12)
		elif(msg[0] == 176):
			MIDI_ProcessCC(msg)
		elif(msg[0] == 248):
			midi_output.send(m)
		else:
			midi_output.send(MSG(msg))
			
			