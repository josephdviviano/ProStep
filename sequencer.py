
# Mopho Sequence Looper

# Record/Overdub
# Assign sequences to keyboard + play


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

MIDI_CHANNEL=MOPHO2_CHANNEL
MIDIKB_CHANNEL=MOPHO2_CHANNEL
#keyboard_input = mido.open_input('Mopho Keyboard 4')
clock = mido.open_input('5- TR-8 3')
midi_input = MultiPort([clock])
#midi_input = connect('localhost',8080)
mopho_output  = mido.open_output('USB Uno MIDI Interface 3')
#mopho2_output = mido.open_output('UM-ONE 3')
#mopho_keyboard = mido.open_output('Mopho Keyboard 5')

#keyboard_output = mido.open_output(outp[4])
#midi_output = MultiPort([keyboard_output,mopho_output])
midi_output = MultiPort([mopho_keyboard])


MIDI_SetInOut(midi_input,midi_output)

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
		

scale = scale_phrygian_dom[:]
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
chord_map[KEY_D+1] = chord_maj
chord_map[KEY_E] = chord_maj
chord_map[KEY_F] = chord_min
chord_map[KEY_F+1] = chord_min
chord_map[KEY_G] = chord_min
chord_map[KEY_G+1] = chord_min
chord_map[KEY_A] = chord_maj
chord_map[KEY_A+1] = chord_maj
chord_map[KEY_B] = chord_maj






seq_select = NRPN_SEQ1_STEP1
cur_seq    = 0

def MIDI_ProcessCC(msg):
	global keyboard,seq_select,cur_seq
	cc = msg[1]
	val = msg[2]
	print cc
	chan = msg[0] & 0xF
	if(cc == 114 and msg[2] == 127):
		cur_seq = cur_seq+1
		cur_seq = cur_seq % 4
		if(cur_seq == 0): cur_seq = NRPN_SEQ1_STEP1
		elif(cur_seq == 1): cur_seq = NRPN_SEQ2_STEP1
		elif(cur_seq == 2): cur_seq = NRPN_SEQ3_STEP1
		else: cur_seq = NRPN_SEQ4_STEP1
		

	elif(cc == 14):
		MOPHO_SendSeqStep(seq_select,0,val,chan)
	elif(cc == 15 ):
		MOPHO_SendSeqStep(seq_select,1,val,chan)
	elif(cc == 16 ):
		MOPHO_SendSeqStep(seq_select,2,val,chan)
	elif(cc == 17 ):
		MOPHO_SendSeqStep(seq_select,3,val,chan)
	elif(cc == 18 ):
		MOPHO_SendSeqStep(seq_select,4,val,chan)
	elif(cc == 19 ):
		MOPHO_SendSeqStep(seq_select,5,val,chan)
	elif(cc == 20 ):
		MOPHO_SendSeqStep(seq_select,6,val,chan)
	elif(cc == 21 ):
		MOPHO_SendSeqStep(seq_select,7,val,chan)
			
	elif(cc == 119 and msg[2] == 127):
		MOPHO_SendNRPNSeq(chan)
		keyboard=MOPHO_GenerateSequence()
		MOPHO_SendSequenceNotes(NRPN_SEQ1_STEP1,keyboard[0],chan)
		MOPHO_SendSequenceNotes(NRPN_SEQ2_STEP1,keyboard[1],chan)
		MOPHO_SendSequenceNotes(NRPN_SEQ3_STEP1,keyboard[2],chan)
		MOPHO_SendSequenceNotes(NRPN_SEQ4_STEP1,keyboard[3],chan)				
	else:
		midi_output.send(MSG(msg))			


		
def Loop():
	global last_note,last_vel,CC_MULT,key_step,cur_patch,mopho_output
	
	tetra_prog = 0
	root = 48
	cur_step = 0
	tcur_step = 0
	
	print 'Press Root key on keyboard...'
	while 1:
	
		key = keyboard_input.receive().bytes()
		if(key[0] >= 0x90 and key[0] <= 0x9F):			
			root = key[1]
			print root
			break
		
	MOPHO_Sequencer(MOPHO_CHANNEL)
	TETRA_Sequencer(TETRA_CHANNEL)
	
	while 1:
		
		for msg in midi_input:
			key = msg.bytes()
			
			if(key[0] == 0x90+MOPHO_CHANNEL):						
				note = key[1] % 12 
				note = note * 2
				oct   = (key[1] -24) / 12
				if(oct < 0): oct = 0
				if(oct > 4): oct = 4
				note = oct*24+note
				
				MOPHO_SendSeqStep(NRPN_SEQ1_STEP1,cur_step,note,MOPHO_CHANNEL)
				cur_step = cur_step+1
				cur_step = cur_step % 16
			
			elif(key[0] >= 0xB0 and key[0] <= 0xBF):
				if((key[0] & 0xF) == MOPHO_CHANNEL and key[1] == 115): 
					MIDI_NoteOn([0x90,root,100])
				elif(key[1] == 116):
					if(key[2] == 127): tetra_prog = not tetra_prog
				elif(key[1]== 117):
					if(tetra_prog == 0):
						MOPHO_SendSeqStep(NRPN_SEQ1_STEP1,cur_step,key[2])
						cur_step = cur_step+1
						cur_step = cur_step % 16

					else:
						MOPHO_SendSeqStep(NRPN_SEQ1_STEP1,cur_step,127)
						tcur_step = tcur_step+1
						tcur_step = tcur_step %16
					
				elif(key[1] == 118):
					if(tetra_prog == 0):
						MOPHO_SendSeqStep(NRPN_SEQ1_STEP1,cur_step,key[2])
						cur_step = cur_step+1
						cur_step = cur_step % 16

					else:
						MOPHO_SendSeqStep(NRPN_SEQ1_STEP1,cur_step,126)
						tcur_step = tcur_step+1
						tcur_step = tcur_step %16
					
				else:
					MIDI_ProcessCC(key)
			
			elif(key[0] == 248):
				midi_output.send(MSG(key))
								
			elif(key[0] < 0x80 or key[0] > 0x8F):
				midi_output.send(MSG(key))
			
Loop()