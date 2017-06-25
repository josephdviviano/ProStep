
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QMainWindow,QApplication
from mido.sockets import PortServer,connect
import pickle
import math
import sys

from midi import *
from mopho import *
from patterns import *
from mido import Message,MidiFile,MidiTrack

SEQ_STEPS=16

class Sequencer:

	def __init__(self):
		self.notes = [0]*SEQ_STEPS
		self.cur_step = 0
		self.ppq = [0]*SEQ_STEPS
		self.repeats = [0]*SEQ_STEPS
		self.rests = [0]*SEQ_STEPS
		self.num_steps = SEQ_STEPS
		self.mainwindow = None
		
	def SaveTrack(self,mid,ch):
		track = MidiTrack()
		track.type=1
		mid.tracks.append(track)
		
		for i in range(self.num_steps):
			
			if(self.rests[i] == 1): 
				delta_time = delta_time + self.ppq[i]
			else:
				delta_time = 0.0
				
			if(self.repeats[i] > 0):
				for j in range(self.repeats[i]):
					if(self.rests[i] == 1):
						delta_time = delta_time + self.ppq[i]
					else:	
						track.append(Message('note_on',note=self.notes[i],channel=ch,velocity=100,time=1))
						track.append(Message('note_off',note=self.notes[i],channel=ch,velocity=127,time=int(delta_time+self.ppq[i]-1)))
						
				if(rests[i] == 1):
					track.append(Message('note_off',note=self.notes[i],channel=ch,velocity=127,time=int(delta_time)))
			else:
				track.append(Message('note_on',note=self.notes[i],channel=ch,velocity=100,time=1))
				track.append(Message('note_off',note=self.notes[i],channel=ch,velocity=127,time=int(self.ppq[i]-1)))
		
		
	def Save(self,filename):
		mid = MidiFile()
		mid.ticks_per_beat = 24
		for i in range(16):
			self.Randomize()
			self.SaveTrack(mid,i)
		
		mid.save(filename)
		
			
	def Randomize(self):
		seq = GEN_CreatePattern()
		
		for i in range(self.num_steps):
			seq[i] = seq[i] + 24
			if(seq[i] < 24): seq[i] = 24
			if(seq[i] > 80): seq[i] = 80
			self.notes[i] = seq[i]
			self.ppq[i] = 6
			

class DrumSequencer:
	
	def __init__(self):
		self.bd = [0]*SEQ_STEPS
		self.sd = [0]*SEQ_STEPS
		self.sd = [0]*SEQ_STEPS
		self.cur_step = 0
		self.ppq = [0]*SEQ_STEPS
		self.repeats = [0]*SEQ_STEPS
		self.rests = [0]*SEQ_STEPS
		self.num_steps = SEQ_STEPS
		self.mainwindow = None
		
	def AddTrack(self,note,track,i):
			
		if(self.repeats[i] > 0):
			for j in range(self.repeats[i]):
				if(self.rests[i] == 1):
					self.delta_time = self.delta_time + self.ppq[i]
				else:	
					track.append('note_on',note=notes,velocity=100,time=0)
					track.append('note_off',note=note,velocity=127,time=int(self.delta_time+self.ppq[i]))
					
			if(rests[i] == 1):
				track.append('note_off',note=note,velocity=127,time=int(self.delta_time))
		else:
			track.append(Message('note_on',note=self.note,velocity=100,time=0))
			track.append(Message('note_off',note=self.note,velocity=127,time=int(self.ppq[i])))
	
	def Save(self,filename):
		mid = MidiFile()
		mid.ticks_per_beat = 24
		track = MidiTrack()
		mid.tracks.append(track)
		
		for i in range(self.num_steps):
			if(self.rests[i] == 1): 
				self.delta_time = self.delta_time + self.ppq[i]
			else:
				self.delta_time = 0.0
		
			self.AddTrack(self.bd[i],track,i)
			self.AddTrack(self.sd[i],track,i)
			self.AddTrack(self.lt[i],track,i)
			self.AddTrack(self.mt[i],track,i)
			self.AddTrack(self.ht[i],track,i)
			self.AddTrack(self.rs[i],track,i)
			self.AddTrack(self.ch[i],track,i)
			self.AddTrack(self.oh[i],track,i)
			self.AddTrack(self.cc[i],track,i)
			self.AddTrack(self.rc[i],track,i)
			
		mid.save(filename)
			
	def Randomize(self):
		seq = GEN_CreatePattern()
		
		for i in range(16):
			seq[i] = seq[i] + 24
			if(seq[i] < 24): seq[i] = 24
			if(seq[i] > 80): seq[i] = 80
			self.notes[i] = seq[i]
			self.ppq[i] = 6
	
Seq = Sequencer()
os.chdir('.\mid')
for i in range(200):
	Seq.Randomize()
	filename = 'test_'+str(i)+'.mid'
	Seq.Save(filename)
			