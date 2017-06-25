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

PPQ_LEN = 6 
BUFFER_SIZE=16
midi_buffer = [-1]*BUFFER_SIZE
cur_step = 0
ppq = 0
	

			
while 1:
	
	for msg in midi_input:
		key = msg.bytes()
		if(key[0] == 248):
			midi_output.send(MSG(key))
			ppq = ppq + 1
			if(ppq >= PPQ_LEN):
				if(midi_buffer[cur_step] != -1): MIDI_NoteOff(midi_buffer[cur_step])
				cur_step = cur_step + 1
				cur_step = cur_step % BUFFER_SIZE
				ppq = 0
				if(midi_buffer[cur_step] != -1): MIDI_NoteOn(midi_buffer[cur_step])
			
		elif(key[0] == 0x90 + MOPHO_CHANNEL):
			if(key[1] < 36 or key[1] > 96): n = -1
			else: n = key[1]
			midi_buffer[cur_step] = n
		else:
			midi_output.send(MSG(key))