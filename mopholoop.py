
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

seq_select = NRPN_SEQ1_STEP1
cur_seq    = 0

MIDI_CHANNEL=0x0
MIDIKB_CHANNEL=0x0

PPQ_SIXTEENTH=6
PPQ_EIGTH=12
PPQ_QUARTER=24
PPQ_HALF=48
PPQ_WHOLE=96

PPQ_LEN=PPQ_SIXTEENTH

inp = mido.get_input_names()
print 'inputs:'
for n in inp:
	print n
print '\n outputs'
outp = mido.get_output_names()
for n in outp:
	print n
	
input = mido.open_input('Mopho Keyboard 0')
output = mido.open_output('Mopho Keyboard 1')

MIDI_SetInOut(input,input,output)


def Loop():
	global last_note,last_vel,CC_MULT,key_step,cur_patch,mopho_output
	ppq=0
	tetra_prog = 0
	root = 48
	cur_step = 0
	tcur_step = 0
	
	print 'Press Root key on keyboard...'
	while 1:
	
		key = input.receive().bytes()
		if(key[0] >= 0x90 and key[0] <= 0x9F):			
			root = key[1]
			print root
			break
		
	MOPHO_Sequencer(MIDI_CHANNEL)
	MIDI_NoteOn(root)
	
	while 1:
		
		for msg in input:
			key = msg.bytes()
			
			if(key[0] == 0x90+MIDI_CHANNEL):
				note = key[1] % 12 
				note = note * 2
				oct   = (key[1] -48) / 12
				if(oct < 0): oct = 0
				if(oct > 4): oct = 4
				note = oct*24+note
					
				MOPHO_SendSeqStep(NRPN_SEQ1_STEP1,cur_step,note,MIDI_CHANNEL)
				cur_step = cur_step+1
				cur_step = cur_step % 16
			
			elif(key[0] == 248):
				#ppq = ppq+1
				#if(ppq >= PPQ_LEN):
				#	cur_step = cur_step + 1
				#	cur_step = cur_step % 16
				output.send(MSG(key))
								
			elif(key[0] < 0x80 or key[0] > 0x8F):				
				output.send(MSG(key))
			

if __name__ == '__main__':			
	Loop()