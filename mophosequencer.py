
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

PPQ_LEN=PPQ_SIXTEENTH


seq_select = NRPN_SEQ1_STEP1
cur_seq    = NRPN_SEQ1_STEP1
seq = 0
seq_assign=0
	
def MIDI_ProcessCC(msg):
	global keyboard,seq_select,cur_seq,seq,seq_assign
	cc = msg[1]
	val = msg[2]
	print cc
	chan = msg[0] & 0xF

	if(cc == 114 and msg[2] == 127):
		seq = not seq
		if(seq): seq_assign = 8
		else:seq_assign=0
		
	elif(cc == 117 and msg[2] == 127):
		cur_seq = cur_seq+1
		cur_seq = cur_seq % 4
		if(cur_seq == 0): cur_seq = NRPN_SEQ1_STEP1
		elif(cur_seq == 1): cur_seq = NRPN_SEQ2_STEP1
		elif(cur_seq == 2): cur_seq = NRPN_SEQ3_STEP1
		else: cur_seq = NRPN_SEQ4_STEP1
	
	elif(cc == 118 and msg[2] == 127):
		cur_seq = cur_seq-1
		if(cur_seq < 0): cur_seq = 3
		if(cur_seq == 0): cur_seq = NRPN_SEQ1_STEP1
		elif(cur_seq == 1): cur_seq = NRPN_SEQ2_STEP1
		elif(cur_seq == 2): cur_seq = NRPN_SEQ3_STEP1
		else: cur_seq = NRPN_SEQ4_STEP1
	elif(cc == 14):
		MOPHO_SendSeqStep(cur_seq,0+seq_assign,val,chan)
	elif(cc == 15 ):
		MOPHO_SendSeqStep(cur_seq,1+seq_assign,val,chan)
	elif(cc == 16 ):
		MOPHO_SendSeqStep(cur_seq,2+seq_assign,val,chan)
	elif(cc == 17 ):
		MOPHO_SendSeqStep(cur_seq,3+seq_assign,val,chan)
	elif(cc == 18 ):
		MOPHO_SendSeqStep(cur_seq,4+seq_assign,val,chan)
	elif(cc == 19 ):
		MOPHO_SendSeqStep(cur_seq,5+seq_assign,val,chan)
	elif(cc == 20 ):
		MOPHO_SendSeqStep(cur_seq,6+seq_assign,val,chan)
	elif(cc == 21 ):
		MOPHO_SendSeqStep(cur_seq,7+seq_assign,val,chan)
			
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
	ppq=0
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
	
	while 1:
		
		for msg in midi_input:
			key = msg.bytes()
			
			
			if(key[0] == 0x90+MOPHO_CHANNEL):
				if(key[1] < 24): note = 127
				else:
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
				else:
					MIDI_ProcessCC(key)
			
			elif(key[0] == 248):
				ppq = ppq+1
				if(ppq >= PPQ_LEN):
					cur_step = cur_step + 1
					cur_step = cur_step % 16
				midi_output.send(MSG(key))
								
			elif(key[0] < 0x80 or key[0] > 0x8F):
				midi_output.send(MSG(key))
			
Loop()