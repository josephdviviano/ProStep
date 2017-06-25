
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

keyboard_input  = mido.open_input(inp[0])
#clk  = mido.open_input(self.clocks.currentText())
midi_output	= mido.open_output(outp[1])

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
	buffer = [0]*127
	notes = [0]*127
	key_bit = 0
	last_key = -1
	while 1:
		
		for msg in keyboard_input:
			key = msg.bytes()
			
			
			if(key[0] == 0x90 + MOPHO_CHANNEL):
				keybit =0
				for i in range(127):
					if(buffer[i] == 1): 
						keybit=1
						break
				
				if(keybit == 0):
					for i in range(127):
						if(notes[i] == 1):
							print 'off'
							notes[i] = 0
							MIDI_NoteOff(i)
							
				
				buffer[key[1]] = 1
				MIDI_NoteOn(key[1])
				
			elif(key[0] == 0x80 +MOPHO_CHANNEL):				
				buffer[key[1]]=0
				notes[key[1]] = 1
				
			else:
				midi_output.send(MSG(key))
			

if __name__ == "__main__":			
	Loop()	