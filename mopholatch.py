
from random import *
import mido
from mido.ports import MultiPort
import array
from time import *
import os,glob
import threading


outp= mido.get_output_names()
inp = mido.get_input_names()

print "Midi inputs"
for n in inp:
	print n
	
print "\nMidi Outputs"
for n in outp:
	print n
	
MOPHO_CHANNEL=0x0

keyboard_input  = mido.open_input(inp[3])

sq1  = mido.open_output(outp[5])
tb3  = mido.open_output(outp[0])
midi_output	= mido.open_output(outp[4])
midi_input = keyboard_input

def MSG(msg):
	return mido.Message.from_bytes(msg)
	
def MIDI_NoteOn(note,chan=MOPHO_CHANNEL):
	msg = [0]*3
	msg[0] = 0x90 + chan
	msg[1] = note
	msg[2] = 100
	print msg
	midi_output.send(MSG(msg))

def MIDI_NoteOff(note,chan = MOPHO_CHANNEL):
	msg=[0]*3
	msg[0]  = 0x80 + chan
	msg[1] = note
	msg[2] = 127
	midi_output.send(MSG(msg))
				

def Loop():
	
	last_key = -1
	msg = mido.Message.from_bytes([0xFA])
	sq1.send(msg)
	tb3.send(msg)
	while 1:
		
		for msg in midi_input:
			key = msg.bytes()
		
			if(key[0] == 0x90 + MOPHO_CHANNEL):				
				if(last_key != -1):
					MIDI_NoteOff(last_key)
				MIDI_NoteOn(key[1])
				last_key = key[1]
			elif(key[0] == 248):
				sq1.send(msg)
				tb3.send(msg)
			elif(key[0] == 0xFA):
				sq1.send(msg)
				tb3.send(msg)
			elif(key[0] < 0x80 or key[0] >= 0x8F):
				midi_output.send(MSG(key))
			
			
if __name__ == "__main__":			
	Loop()	