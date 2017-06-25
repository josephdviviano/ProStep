from random import *
import mido
from mido.ports import MultiPort
import array
from time import *
import os,glob
import threading
from patterns import *
import mopho

outp= mido.get_output_names()
inp = mido.get_input_names()

MOPHO_CHANNEL = 0x2
TETRA_CHANNEL  = 0x3

print "Midi Outputs"
for x in outp:
	print x
	
print "Midi Inputs"
for y in inp:
	print y
	
tb3 = mido.open_input(inp[0])

while 1:
	msg = tb3.receive().bytes()
	if(msg[0] >= 0xB0 and msg[0] <= 0xBF):
		print msg[1]
	else: print msg