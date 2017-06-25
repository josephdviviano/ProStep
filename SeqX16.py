# Jump to Pattern
# Delete Pattern
# Pattern Tracker
# Pattern Names
# Tracker - Pattern, num_measures
# start/stop drums/bass
# sync ports dialog - set ports to sync clock to (SQ-1, TB3, etc)

from PyQt4 import QtCore, QtGui,Qt
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



TEMPO=145.0

PPQ_WHOLE=96
PLAY_LEN=4*PPQ_WHOLE
TX_DELAY=0.01

MIDI_CHANNEL=1
MIDIKB_CHANNEL=1

fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

MUSIC_SetScaleChord(scale_phrygian_dom,chord_min)

# maximum voice sequencers
MAX_SEQS=16
MAX_TRACKERS=16

def NoteToMopho(n):
	n = n % 12
	o = n / 12
	if(o > 4): o = 4
	
	return o*24+n*2
	
def MophoToNote(n):
	n = n % 24
	o = o / 24
	note = 24+n+o*12

scaling = {}
for i in range(0,125):
	x = scale_minor[i % len(scale_minor)]
	oct = i/12
	n = NoteToMopho(oct*12+x)
	scaling[i] = n
scaling[126] = 126
scaling[127] = 127

note_names = {}
for i in range(0,127):
	n = i % 12
	s = name_notes[n]
	note_names[i] = s + str(i / 12)
	
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# Encapuslate a Sequencer voice bank (usually 16x8 steps)
class Seq:
	
	def __init__(self, steps=16):
		self.seq_length = steps
		self.notes = [0]*self.seq_length
		self.cur_step = 0
		self.ppq = [0]*self.seq_length
		self.repeats = [0]*self.seq_length
		self.rests = [0]*self.seq_length
		self.num_steps = steps
		self.cur_ppq = 0
		self.cur_repeats = 0
		self.rest = 0
		self.note = 0
		self.midi_output = None
		self.midi_channel = 0
		self.Randomize()
		
	def SetNote(self,note,step):
		self.notes[step] = note
		
	def SetCurStep(self,val):
		self.cur_step = val
		
	def IncCurStep(self):
		self.cur_step = self.cur_step + 1
		self.cur_step = self.cur_step % self.seq_length
		
	def Resize(self,steps):
		
		self.SetNumSteps(steps)
		self.Randomize()
		
	def SetNumSteps(self,num):
		self.num_steps = num
		self.seq_length = num
		self.notes = [0]*num
		self.ppq   = [0]*num
		self.repeats = [0]*num
		self.rests = [0]*num

		
	def Update(self,ppq,midi_channel):
		self.midi_channel=midi_channel
		midi_input,midi_output = MIDI_GetInOut()
		ret = 0
		if(self.cur_ppq == 0): self.cur_ppq = self.ppq[self.cur_step]
		
		try:
			if(ppq % self.cur_ppq == 0):			
				self.cur_repeats = self.cur_repeats - 1
				if(self.cur_repeats < 0):
					self.cur_step = self.cur_step + 1
					self.cur_step = self.cur_step % 16						
					if(self.cur_step >= self.num_steps):
						ret = -1
						self.cur_step = 0
					if(self.rest == 0):
						midi_output.send(MSG([0x80+self.midi_channel,self.note,127]))
					self.rest  = self.rests[self.cur_step]
					self.note = self.notes[self.cur_step]
					self.cur_repeats = self.repeats[self.cur_step]
					self.cur_ppq = self.ppq[self.cur_step]
				else:
					if(self.rest == 0):
						midi_output.send(MSG([0x80+self.midi_channel,self.note,127]))
					
					
				if(self.rest != 1):
					midi_output.send(MSG([0x90+self.midi_channel,self.note,127]))
		except:
			
			return -1
			
		return ret
	
	def Save(self,mid):
		track = MidiTrack()
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
						track.append('note_on',note=self.notes[i],velocity=100,time=0)
						track.append('note_off',note=self.notes[i],velocity=127,time=int(delta_time+self.ppq[i]))
						
				if(rests[i] == 1):
					track.append('note_off',note=self.notes[i],velocity=127,time=int(delta_time))
			else:
				track.append(Message('note_on',note=self.notes[i],velocity=100,time=0))
				track.append(Message('note_off',note=self.notes[i],velocity=127,time=int(self.ppq[i])))
				
			

	def Transpose(self,value):
		for i in range(self.num_steps):
			self.notes[i] = self.notes[i] + value
			if(self.notes[i] < 0): self.notes[i] = 0
			if(self.notes[i] > 127): self.notes[i] = 127
			
	def Load(self):
		pass
			
	def Randomize(self):
		seq = []
		for i in range(self.num_steps/16):
			seq = seq + GEN_CreatePattern(GEN_TYPE_RANDOM)
		
		for i in range(self.num_steps):			
			seq[i] = seq[i] + 36
			if(seq[i] < 24): seq[i] = 24
			if(seq[i] > 80): seq[i] = 80
			self.notes[i] = seq[i]
			self.ppq[i] = 6
			self.repeats[i] = 0
			self.rests[i] = 0
			
	def RandomizePPQ(self):
		for i in range(self.num_steps):
			self.ppq[i] = choice([1,3,6,12,24])
		
	def RandomizeRests(self):
		for i in range(self.num_steps):
			self.rests[i] = randint(0,1)
			
	def RandomizeRepeats(self):
		for i in range(self.num_steps):
			self.repeats[i] = randint(0,7)
	
	def Pickle(self,filename):
		pickle.dump( self, open(filename,'wb') )
		
	def Unpickle(self,filename):
		self = pickle.load( open(filename,'rb'))

	def Copy(self, c):
		self.notes = c.notes[:]
		self.ppq = c.ppq[:]
		self.repeats = c.repeats[:]
		self.rests = c.rests[:]		
		self.seq_length = c.seq_length
		self.cur_step = c.cur_step
		self.num_steps = c.num_steps
		self.cur_ppq = c.cur_ppq
		self.cur_repeats = c.cur_repeats
		self.rest = c.rest
		self.note = c.note
		self.midi_channel = c.midi_channel
		
		
# thread for handling MIDI i/o		
class Worker(QThread):
	
	def __init__(self,mainwindow,parent=None):
		QThread.__init__(self,parent)
		self.exiting = False
		self.mainwindow = mainwindow
		self.scene_len = PLAY_LEN
		self.ppq = -1
		self.cur_ppq = -1
		self.input_buffer = [0]*256
		self.cur_step = 0
		self.note = 0
		self.repeats = 0
		self.cur_note = 0
		self.rest = 0
		self.midi_channel = MIDI_CHANNEL
		self.kb_channel    = MIDIKB_CHANNEL
		self.midi_input = None
		self.midi_output = None
		self.num_steps = 16
		
	def __del__(self):
		self.exiting = True
		self.wait()
	
			
	def run(self):
		print 'running'
		while not self.exiting:
			if(self.midi_input is None):
				continue
				
			for msg in self.midi_input:
				key = msg.bytes()
				if(self.mainwindow.bStopped == True): continue
				
				if(key[0] == 248):
					self.ppq = self.ppq+1
					seq = self.mainwindow.GetSequencer()
					seq.Update(self.ppq)
							
							
				elif(key[0] >= 0x90 and key[0] <= 0x9F):
					
					if(key[0] == 0x90 + self.kb_channel):
						note = key[1] 
						if(note < 0): note = 0
						seq = self.mainwindow.GetSequencer()						
						seq.sequencers[seq.cur_seq].notes[self.cur_note] = note
						self.cur_note = self.cur_note + 1
						self.cur_note = self.cur_note % self.num_steps 
						self.emit(QtCore.SIGNAL("UpdateUi()"))
						
				self.midi_output.send(msg)

# Config Dialog
class Ui_ConfigDialog(object):
	def setupUi(self, Dialog):
		self.dlg = Dialog
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(400, 192)
		self.buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.buttonBox.setGeometry(QtCore.QRect(30, 120, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
		self.sbBanks = QtGui.QSpinBox(Dialog)
		self.sbBanks.setGeometry(QtCore.QRect(70, 30, 42, 22))
		self.sbBanks.setObjectName(_fromUtf8("sbBanks"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(10, 30, 46, 13))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(10, 70, 46, 13))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.sbVoices = QtGui.QSpinBox(Dialog)
		self.sbVoices.setGeometry(QtCore.QRect(70, 70, 42, 22))
		self.sbVoices.setObjectName(_fromUtf8("sbVoices"))
		self.cbInputs = QtGui.QComboBox(Dialog)
		self.cbInputs.setGeometry(QtCore.QRect(140, 60, 69, 22))
		self.cbInputs.setObjectName(_fromUtf8("cbInputs"))
		self.label_3 = QtGui.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(140, 30, 61, 16))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(Dialog)
		self.label_4.setGeometry(QtCore.QRect(230, 30, 46, 13))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.cbClocks = QtGui.QComboBox(Dialog)
		self.cbClocks.setGeometry(QtCore.QRect(230, 60, 69, 22))
		self.cbClocks.setObjectName(_fromUtf8("cbClocks"))
		self.label_5 = QtGui.QLabel(Dialog)
		self.label_5.setGeometry(QtCore.QRect(310, 30, 46, 13))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.cbOutputs = QtGui.QComboBox(Dialog)
		self.cbOutputs.setGeometry(QtCore.QRect(310, 60, 69, 22))
		self.cbOutputs.setObjectName(_fromUtf8("cbOutputs"))

		outp= mido.get_output_names()
		inp = mido.get_input_names()

		for i in inp:
			self.cbInputs.addItem(i)
			self.cbClocks.addItem(i)
		self.outputs = QtGui.QComboBox()
		for i in outp:
			self.cbOutputs.addItem(i)

		self.sbChannel = QtGui.QSpinBox(Dialog)
		self.sbChannel.setMinimum(1)
		self.sbChannel.setMaximum(16)
		self.sbChannel.setValue(1)
		self.sbChannel.setGeometry(140,84,69,22)
		self.sbChannel.setObjectName(_fromUtf8("sbChannel"))

		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accepted)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.rejected)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label.setText(_translate("Dialog", "Banks", None))
		self.label_2.setText(_translate("Dialog", "Voices", None))
		self.label_3.setText(_translate("Dialog", "Keyboard", None))
		self.label_4.setText(_translate("Dialog", "Clock", None))
		self.label_5.setText(_translate("Dialog", "Output", None))


	def accepted(self):
		MIDI_Close()
		
		key = mido.open_input(self.cbInputs.currentText())
		if(self.cbInputs.currentText() == self.cbClocks.currentText()):
			clk = key
		else:
			clk  = mido.open_input(self.cbClocks.currentText())
		out = mido.open_output(self.cbOutputs.currentText())
		
		MIDI_SetInOut(key,clk,out)
		channel = self.sbChannel.value()-1
		banks = self.sbBanks.value()
		self.parent.num_banks = banks
		self.parent.input_channel = channel
		self.parent.midi_channel = channel
		self.parent.num_seqs = self.sbVoices.value()
		self.parent.num_banks = banks
		
		self.dlg.close()
		
	def rejected(self):
		self.dlg.close()
	

# transpose dialog
class Ui_TransposeDialog(object):
	
	def setupUi(self, Dialog):
		self.dlg = Dialog
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(385, 114)
		self.buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.buttonBox.setGeometry(QtCore.QRect(10, 50, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(20, 20, 71, 16))
		self.label.setObjectName(_fromUtf8("label"))
		self.spinBox = QtGui.QSpinBox(Dialog)
		self.spinBox.setGeometry(QtCore.QRect(100, 20, 42, 22))
		self.spinBox.setObjectName(_fromUtf8("spinBox"))
		self.spinBox.setMinimum(-80)
		self.spinBox.setMaximum(80)
		
		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label.setText(_translate("Dialog", "Semitones", None))

	def accept(self):
		self.mainwindow.Transpose(self.spinBox.value())
		self.dlg.close()
		
	def reject(self):
		self.dlg.close()
		

# Tracker
# handles playback of seq voices/banks
class Tracker:
	
	def __init__(self):
		
		self.patterns = {}
		self.cur_pattern = ""
		self.pattern_chain = []
		self.chain  = 0
		self.repeats = 0
		self.midi_output = 0
		self.midi_channel = 0
		self.bStopped = False
		
	def AddPattern(self,name,seq):
		self.patterns[name] = seq
		
	def Chain(self,name,repeats):
		self.pattern.chain.append([repeats,name])
			
	def RemovePattern(self,name):
		del self.patterns[name]
		
	def Update(self,ppq):
		x = self.patterns[self.cur_pattern].Update(ppq)
		if(x == -1):
			self.repeats = self.repeats - 1
			if(self.repeats <= 0):
				self.repeats = self.pattern_chain[self.chain][0]
				self.cur_pattern = self.patterns[self.pattern_chain[self.chain][1]]
				
				self.chain = self.chain+1
				if(self.chain >= len(self.pattern_chain)): self.chain = 0
		
	
	def Save(self):
		pass
		
	def Load(self):
		pass
	
# sequencer holds all sequence data
class Sequencer:

	def __init__(self):
		self.sequencers = [0]*MAX_SEQS
		self.patterns = []
		self.trackers = [0]*MAX_TRACKERS
		self.open_trackers = 0
		self.num_sequencers = 1
		self.num_banks = 1
		self.mainwindow = None
		self.cur_seq = 0
		self.cur_bank = 0
		self.cur_pattern = 0
		self.bStopped = False
		self.num_seqs = 0
		self.midi_channel = 0
		
		for i in range(MAX_SEQS):
			self.sequencers[i] = Seq()
			
		for i in range(MAX_TRACKERS):
			self.trackers[i] = Tracker()
	
	def SaveMidi(self, filename):		
		mid = MidiFile()
		mid.ticks_per_beat = 24
		for i in range(self.num_sequencers):
			for j in range(self.sequencers[i].num_voices):
				self.sequencers[i].voices[j].SaveMidi(mid)
		mid.save(str(filename))
		
	def LoadPickle(self,filename):
		self = pickle.load(open(filename,'rb'))
		
	def SavePickle(self, filename):
		pickle.dump(self, open(filename,'wb'))
		
	def LoadPatterns(self,filename):		
		self.patterns = pickle.load(open(filename,'rb'))
		
	def GetCurrentVoice(self):
		return self.sequencers[self.cur_seq]
		
	def Resize(self,num_voices):
		self.num_banks = num_voices
		for i in range(MAX_SEQS):
			self.sequencers[i].Resize(self.num_banks*16)
		
	def NextPattern(self):
		self.cur_pattern = self.cur_pattern + 1
		self.cur_pattern = self.cur_pattern % len(self.patterns)

	def PrevPattern(self):
		self.cur_pattern = self.cur_pattern - 1
		if(self.cur_pattern < 0): self.cur_pattern = len(self.patterns)-1
	
	def Transpose(self,value):
		self.sequencers[self.cur_seq].Transpose(value)

		
	def Randomize(self):
		self[seq.cur_seq].Randomize()			
		
	def Copy(self):
		self.copy_seq = Seq()
		self.copy_seq.Copy(seq.sequencers[self.cur_seq])
		
	def Paste(self):
		self.sequencers[self.cur_seq].Copy(self.copy_seq)
		
	def RandomizePPQ(self):
		self.sequencers[self.cur_seq].RandomizePPQ()
		
	def RandomizeRests(self):
		self.sequencers[self.cur_seq].RandomizeRests()

	def RandomizeRepeats(self):
		seq.sequencers[self.cur_seq].RandomizeRepeats()
		
	def SetNote(self,n,value):
		self.sequencers[self.cur_seq].notes[n+self.cur_bank*16] = value
		
	def SetPPQ(self,n,value):
		self.sequencers[self.cur_seq].ppq[n+self.cur_bank*16] = value
		
	def SetRest(self,n,value):
		self.sequencers[self.cur_seq].rests[n+self.cur_bank*16] = value
	
	def SetRepeat(self,n,value):
		self.sequencers[self.cur_seq].repeats[n+self.cur_bank*16] = value	
		
	def GetNote(self,n):
		return int((self.sequencers[self.cur_seq].notes[n+self.cur_bank*16]/127.0)*1024)
		
	def GetPPQ(self,n):
		return self.sequencers[self.cur_seq].ppq[n+self.cur_bank*16]
		
	def GetRepeat(self,n):
		return self.sequencers[self.cur_seq].repeats[n+self.cur_bank*16]
		
	def GetRest(self,n):
		return self.sequencers[self.cur_seq].rests[n+self.cur_bank*16]
		
		
	def Update(self,ppq):
		for j in range(self.num_seqs):
			self.sequencers[j].Update(ppq,self.midi_channel)
	
	def AddPattern(self):
		self.Copy()		
		self.patterns.append(self.copy_seq)
		
	def RemovePattern(self,num):
		del self.patterns[num]
	
class Ui_MainWindow(object):
	
	def __init__(self):
		
		self.sequencer = Sequencer()
		self.bStopped = False
		
	def GetSequencer(self):
		return self.sequencer
	
	def Save(self):
		pass
		
	def Load(self):
		pass
		
	# save as a midi file
	def SaveMidi(self):		
		filename = QtGui.QFileDialog.getSaveFileName(self.mainwindow, 'Save File', '.')
		seq = self.GetSequencer()				
		seq.SaveMidi(filename)
		
	def SavePickle(self):
		filename = QtGui.QFileDialog.getSaveFileName(self.mainwindow, 'Save File', '.')
		seq = self.GetSequencer()				
		seq.SavePickle(filename)
		
	def LoadPickle(self):
		filename = QtGui.QFileDialog.getOpenFileName(self.mainwindow, 'Open File', '.')
		seq = self.GetSequencer()				
		seq.LoadPickle(filename)
		
				
	def SaveSequencer(self):
		filename = QtGui.QFileDialog.getSaveFileName(self.mainwindow, 'Save File', '.')		
		seq = self.GetSequencer()				
		pickle.dump( seq.sequencers, open(filename,'wb') )
		
	
	def SavePatterns(self):
		filename = QtGui.QFileDialog.getSaveFileName(self.mainwindow, 'Save File', '.')		
		seq = self.GetSequencer()				
		pickle.dump( seq.patterns, open(filename,'wb') )
	
	def LoadPatterns(self):
		filename = QtGui.QFileDialog.getOpenFileName(self.mainwindow, 'Open File', '.')
		seq = GetSequencer()		
		seq.LoadPatterns(filename)
		

	def AddPattern(self):
		seq = self.GetSequencer()				
		seq.AddPattern()
	
	def RemovePattern(self, num):
		seq = self.GetSequencer()				
		seq.RemovePattern(num)
		
	def JumpPattern(self):
		pass
		
	def DelPattern(self):
		pass
		
	def NextPattern(self):
		seq = self.GetSequencer()				
		seq.NextPattern()
		
		
	def PrevPattern(self):
		seq = GetSequencer()		
		seq.PrevPattern()
		
	def Stop(self):
		self.bStopped = True
		
	def Play(self):
		self.bStopped = False
		
	def Options(self):
		dlg = QtGui.QDialog()
		qdlg = Ui_ConfigDialog()		
		qdlg.setupUi(dlg)
		qdlg.parent = self
		dlg.show()
		dlg.exec_()
							
		self.thread.midi_input, self.thread.midi_output = MIDI_GetInOut()
		self.thread.kb_channel = self.input_channel 
		self.thread.midi_channel = self.midi_channel
		self.thread.num_steps = self.num_banks*16
		
		self.curBank.setMaximum(self.num_banks-1)
		self.curSeq.setMaximum(self.num_seqs-1)
		
		seq = self.GetSequencer()		
		seq.num_banks = self.num_banks
		seq.num_seqs = self.num_seqs
		seq.Resize(self.num_banks)
		seq.midi_channel = self.midi_channel
		
		
	def TransposeDlg(self):
		dlg = QtGui.QDialog()
		qdlg = Ui_TransposeDialog()		
		qdlg.mainwindow = self
		qdlg.setupUi(dlg)
		qdlg.parent = self
		dlg.show()
		dlg.exec_()
					
				
	def Copy(self):
		seq = self.GetSequencer()				
		seq.Copy()
		
	def Paste(self):
		seq = self.GetSequencer()				
		seq.Paste()
		
		
	def PrevStep(self):
		self.thread.cur_step = self.thread.cur_step - 1
		if(self.thread.cur_step < 0): self.cur_step = 15
		
	def NextStep(self):
		self.thread.cur_step = self.thread.cur_step + 1
		self.thread.cur_step = self.thread.cur_step % 16
	
	def Transpose(self,value):
		seq = self.GetSequencer()				
		seq.Transpose(value)		
		self.UpdateUi()
		
	def Randomize(self):		
		seq = self.GetSequencer()				
		seq.Randomize()
		self.UpdateUi()
	
	def RandomPPQ(self):
		seq = self.GetSequencer()				
		seq.RandomizePPQ()
		
	
	def RandomRests(self):
		seq = self.GetSequencer()				
		seq.RandomizeRests()
		
			
	def RandomRepeats(self):
		seq = self.GetSequencer()				
		seq.RandomizeRepeats()
		
		
	def SetSteps(self,value):
		seq = self.GetSequencer()						
		seq.num_steps = value
	
	def CurSeq(self,value):
		seq = self.GetSequencer()								
		seq.cur_seq = value
		self.UpdateUi()
	
	def CurBank(self,value):
		seq = self.GetSequencer()								
		seq.cur_bank = value
		self.UpdateUi()
		
		
	###########################################################
	def SetNote(self,n,value):
		seq = self.GetSequencer()						
		seq.SetNote(n,value)
		self.lcdNumber.display(note_names[value])
		
	def Note1(self,value):
		value = int(math.ceil((value/1024.0)*127))
		self.SetNote(0,value)
		
	def Note2(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(1,value)
		
	def Note3(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(2,value)
		
	def Note4(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(3,value)		
		
	def Note5(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(4,value)
		
	def Note6(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(5,value)
		
	def Note7(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(6,value)
		
	def Note8(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(7,value)
		
	def Note9(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(8,value)
		
	def Note10(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(9,value)
		
	def Note11(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(10,value)
		
	def Note12(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(11,value)
		
	def Note13(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(12,value)
		
	def Note14(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(13,value)
		
	def Note15(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(14,value)
		
	def Note16(self,value):
		value=int(math.ceil((value/1024.0)*127))
		self.SetNote(15,value)
	
	#################################################################
	def SetPPQ(self,n,value):
		seq = self.GetSequencer()
		seq.SetPPQ(n,value)
		
		
	def ppq1(self,value):
		self.SetPPQ(0,value)
		
	def ppq2(self,value):
		self.SetPPQ(1,value)
			
	def ppq3(self,value):
		self.SetPPQ(2,value)
		
	def ppq4(self,value):
		self.SetPPQ(3,value)
		
	def ppq5(self,value):
		self.SetPPQ(4,value)
		
	def ppq6(self,value):
		self.SetPPQ(5,value)
		
	def ppq7(self,value):
		self.SetPPQ(6,value)
		
	def ppq8(self,value):
		self.SetPPQ(7,value)
		
	def ppq9(self,value):
		self.SetPPQ(8,value)
		
	def ppq10(self,value):
		self.SetPPQ(9,value)
		
	def ppq11(self,value):
		self.SetPPQ(10,value)
		
	def ppq12(self,value):
		self.SetPPQ(11,value)
		
	def ppq13(self,value):
		self.SetPPQ(12,value)
		
	def ppq14(self,value):
		self.SetPPQ(13,value)
		
	def ppq15(self,value):
		self.SetPPQ(14,value)
		
	def ppq16(self,value):
		self.SetPPQ(15,value)
		
	def SetRest(self,n,value):
		seq = self.GetSequencer()
		seq.SetRest(n,value)
		
	def rest1(self,value):
		self.SetRest(0,value)
		
	def rest2(self,value):
		self.SetRest(1,value)
		
	def rest3(self,value):
		self.SetRest(2,value)
		
	def rest4(self,value):
		self.SetRest(3,value)
		
	def rest5(self,value):
		self.SetRest(4,value)
		
	def rest6(self,value):
		self.SetRest(5,value)
		
	def rest7(self,value):
		self.SetRest(6,value)
		
	def rest8(self,value):
		self.SetRest(7,value)
		
	def rest9(self,value):
		self.SetRest(8,value)
		
	def rest10(self,value):
		self.SetRest(9,value)
		
	def rest11(self,value):
		self.SetRest(10,value)
		
	def rest12(self,value):
		self.SetRest(11,value)
		
	def rest13(self,value):
		self.SetRest(12,value)
		
	def rest14(self,value):
		self.SetRest(13,value)
		
	def rest15(self,value):
		self.SetRest(14,value)
		
	def rest16(self,value):
		self.SetRest(15,value)
		
	
	def SetRepeat(self,n,value):
		seq = self.GetSequencer()
		seq.SetRepeat(n,value)
		
	def Repeat1(self,value):
		self.SetRepeat(0,value)
	def Repeat2(self,value):
		self.SetRepeat(1,value)
	def Repeat3(self,value):
		self.SetRepeat(2,value)
	def Repeat4(self,value):
		self.SetRepeat(3,value)
	def Repeat5(self,value):
		self.SetRepeat(4,value)
	def Repeat6(self,value):
		self.SetRepeat(5,value)
	def Repeat7(self,value):
		self.SetRepeat(6,value)
	def Repeat8(self,value):
		self.SetRepeat(7,value)
	def Repeat9(self,value):
		self.SetRepeat(8,value)
	def Repeat10(self,value):
		self.SetRepeat(9,value)
	def Repeat11(self,value):
		self.SetRepeat(10,value)
	def Repeat12(self,value):
		self.SetRepeat(11,value)
	def Repeat13(self,value):
		self.SetRepeat(12,value)
	def Repeat14(self,value):
		self.SetRepeat(13,value)
	def Repeat15(self,value):
		self.SetRepeat(14,value)
	def Repeat16(self,value):
		self.SetRepeat(15,value)
		
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(940, 600)

		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

		self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
		self.lcdNumber.setGeometry(QtCore.QRect(450, 20, 101, 23))
		self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
		
		self.numSteps = QtGui.QSpinBox(self.centralwidget)
		self.numSteps.setGeometry(QtCore.QRect(400,20,50,25))
		self.numSteps.setObjectName(_fromUtf8("numSteps"))
		self.numSteps.setValue(16)
		self.numSteps.valueChanged.connect(self.SetSteps)
		
		self.curSeq = QtGui.QSpinBox(self.centralwidget)
		self.curSeq.setGeometry(QtCore.QRect(350,20,50,25))
		self.curSeq.setObjectName(_fromUtf8("curSeq"))
		self.curSeq.setValue(0)
		self.curSeq.valueChanged.connect(self.CurSeq)
		
		self.curBank = QtGui.QSpinBox(self.centralwidget)
		self.curBank.setGeometry(QtCore.QRect(300,20,50,25))
		self.curBank.setObjectName(_fromUtf8("curBank"))
		self.curBank.setValue(0)		
		self.curBank.valueChanged.connect(self.CurBank)
		
		self.layoutWidget = QtGui.QWidget(self.centralwidget)
		self.layoutWidget.setGeometry(QtCore.QRect(20, 320, 901, 181))
		self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))

		self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))

		self.repeat1 = QtGui.QSlider(self.layoutWidget)
		self.repeat1.setOrientation(QtCore.Qt.Vertical)
		self.repeat1.setObjectName(_fromUtf8("repeat1"))
		self.repeat1.setMaximum(7)
		self.repeat1.valueChanged.connect(self.Repeat1)
		
		self.thread = Worker(self)
		MainWindow.connect(self.thread, QtCore.SIGNAL("finished()"), self.UpdateUi)
		MainWindow.connect(self.thread, QtCore.SIGNAL("terminated()"), self.UpdateUi)
		MainWindow.connect(self.thread, QtCore.SIGNAL("UpdateUi()"), self.UpdateUi)
		self.mainwindow = MainWindow
		
		self.thread.start()
		
		self.horizontalLayout_3.addWidget(self.repeat1)
		self.repeat2 = QtGui.QSlider(self.layoutWidget)
		self.repeat2.setOrientation(QtCore.Qt.Vertical)
		self.repeat2.setObjectName(_fromUtf8("repeat2"))
		self.repeat2.setMaximum(7)
		self.repeat2.valueChanged.connect(self.Repeat2)
		
		self.horizontalLayout_3.addWidget(self.repeat2)
		self.repeat3 = QtGui.QSlider(self.layoutWidget)
		self.repeat3.setOrientation(QtCore.Qt.Vertical)
		self.repeat3.setObjectName(_fromUtf8("repeat3"))
		self.repeat3.setMaximum(7)
		self.repeat3.valueChanged.connect(self.Repeat3)
		
		self.horizontalLayout_3.addWidget(self.repeat3)
		self.repeat4 = QtGui.QSlider(self.layoutWidget)
		self.repeat4.setOrientation(QtCore.Qt.Vertical)
		self.repeat4.setObjectName(_fromUtf8("repeat4"))
		self.repeat4.setMaximum(7)
		self.horizontalLayout_3.addWidget(self.repeat4)
		self.repeat4.valueChanged.connect(self.Repeat4)
		
		self.repeat5 = QtGui.QSlider(self.layoutWidget)
		self.repeat5.setOrientation(QtCore.Qt.Vertical)
		self.repeat5.setObjectName(_fromUtf8("repeat5"))
		self.repeat5.setMaximum(7)
		self.repeat5.valueChanged.connect(self.Repeat5)
		
		self.horizontalLayout_3.addWidget(self.repeat5)
		self.repeat6 = QtGui.QSlider(self.layoutWidget)
		self.repeat6.setOrientation(QtCore.Qt.Vertical)
		self.repeat6.setObjectName(_fromUtf8("repeat6"))
		self.repeat6.setMaximum(7)
		self.repeat6.valueChanged.connect(self.Repeat6)
		
		self.horizontalLayout_3.addWidget(self.repeat6)
		self.repeat7 = QtGui.QSlider(self.layoutWidget)
		self.repeat7.setOrientation(QtCore.Qt.Vertical)
		self.repeat7.setObjectName(_fromUtf8("repeat7"))
		self.repeat7.valueChanged.connect(self.Repeat7)		
		self.repeat7.setMaximum(7)
		
		self.horizontalLayout_3.addWidget(self.repeat7)
		self.repeat8 = QtGui.QSlider(self.layoutWidget)
		self.repeat8.setOrientation(QtCore.Qt.Vertical)
		self.repeat8.setObjectName(_fromUtf8("repeat8"))
		self.repeat8.setMaximum(7)
		self.repeat8.valueChanged.connect(self.Repeat8)		
		self.horizontalLayout_3.addWidget(self.repeat8)
		
		self.repeat9 = QtGui.QSlider(self.layoutWidget)
		self.repeat9.setOrientation(QtCore.Qt.Vertical)
		self.repeat9.setObjectName(_fromUtf8("repeat9"))
		self.repeat9.setMaximum(7)
		self.repeat9.valueChanged.connect(self.Repeat9)
		
		self.horizontalLayout_3.addWidget(self.repeat9)
		self.repeat10 = QtGui.QSlider(self.layoutWidget)
		self.repeat10.setOrientation(QtCore.Qt.Vertical)
		self.repeat10.setObjectName(_fromUtf8("repeat10"))
		self.repeat10.setMaximum(7)
		self.repeat10.valueChanged.connect(self.Repeat10)
		
		self.horizontalLayout_3.addWidget(self.repeat10)
		self.repeat11 = QtGui.QSlider(self.layoutWidget)
		self.repeat11.setOrientation(QtCore.Qt.Vertical)
		self.repeat11.setObjectName(_fromUtf8("repeat11"))
		self.repeat11.setMaximum(7)
		self.repeat11.valueChanged.connect(self.Repeat11)
		
		self.horizontalLayout_3.addWidget(self.repeat11)
		self.repeat12 = QtGui.QSlider(self.layoutWidget)
		self.repeat12.setOrientation(QtCore.Qt.Vertical)
		self.repeat12.setObjectName(_fromUtf8("repeat12"))
		self.repeat12.setMaximum(7)
		self.repeat12.valueChanged.connect(self.Repeat12)
		
		self.horizontalLayout_3.addWidget(self.repeat12)
		self.repeat13 = QtGui.QSlider(self.layoutWidget)
		self.repeat13.setOrientation(QtCore.Qt.Vertical)
		self.repeat13.setObjectName(_fromUtf8("repeat13"))
		self.repeat13.setMaximum(7)
		self.repeat13.valueChanged.connect(self.Repeat13)
		
		self.horizontalLayout_3.addWidget(self.repeat13)
		self.repeat14 = QtGui.QSlider(self.layoutWidget)
		self.repeat14.setOrientation(QtCore.Qt.Vertical)
		self.repeat14.setObjectName(_fromUtf8("repeat14"))
		self.repeat14.setMaximum(7)
		self.repeat14.valueChanged.connect(self.Repeat14)
		
		self.horizontalLayout_3.addWidget(self.repeat14)
		self.repeat15 = QtGui.QSlider(self.layoutWidget)
		self.repeat15.setOrientation(QtCore.Qt.Vertical)
		self.repeat15.setObjectName(_fromUtf8("repeat15"))
		self.repeat15.setMaximum(7)
		self.repeat15.valueChanged.connect(self.Repeat15)
		
		self.horizontalLayout_3.addWidget(self.repeat15)
		self.repeat16 = QtGui.QSlider(self.layoutWidget)
		self.repeat16.setOrientation(QtCore.Qt.Vertical)
		self.repeat16.setObjectName(_fromUtf8("repeat16"))
		self.repeat16.setMaximum(7)
		self.repeat16.valueChanged.connect(self.Repeat16)
		
		self.horizontalLayout_3.addWidget(self.repeat16)
		self.widget = QtGui.QWidget(self.centralwidget)
		self.widget.setGeometry(QtCore.QRect(20, 80, 901, 181))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.note1 = QtGui.QSlider(self.widget)
		self.note1.setOrientation(QtCore.Qt.Vertical)
		self.note1.setObjectName(_fromUtf8("note1"))
		self.note1.setMaximum(1024)
		self.note1.valueChanged.connect(self.Note1)		
		self.horizontalLayout.addWidget(self.note1)
		self.note2 = QtGui.QSlider(self.widget)
		self.note2.setOrientation(QtCore.Qt.Vertical)
		self.note2.setObjectName(_fromUtf8("note2"))
		self.note2.setMaximum(1024)
		self.note2.valueChanged.connect(self.Note2)
		self.horizontalLayout.addWidget(self.note2)
		self.note3 = QtGui.QSlider(self.widget)
		self.note3.setOrientation(QtCore.Qt.Vertical)
		self.note3.setObjectName(_fromUtf8("note3"))
		self.note3.setMaximum(1024)
		self.horizontalLayout.addWidget(self.note3)
		self.note3.valueChanged.connect(self.Note3)
		self.note4 = QtGui.QSlider(self.widget)
		self.note4.setOrientation(QtCore.Qt.Vertical)
		self.note4.setObjectName(_fromUtf8("note4"))
		self.note4.valueChanged.connect(self.Note4)
		self.note4.setMaximum(1024)
		self.horizontalLayout.addWidget(self.note4)
		self.note5 = QtGui.QSlider(self.widget)
		self.note5.setOrientation(QtCore.Qt.Vertical)
		self.note5.setObjectName(_fromUtf8("note5"))
		self.note5.valueChanged.connect(self.Note5)
		self.note5.setMaximum(1024)
		self.horizontalLayout.addWidget(self.note5)
		self.note6 = QtGui.QSlider(self.widget)
		self.note6.setOrientation(QtCore.Qt.Vertical)
		self.note6.setObjectName(_fromUtf8("note6"))
		self.horizontalLayout.addWidget(self.note6)
		self.note6.valueChanged.connect(self.Note6)
		self.note6.setMaximum(1024)
		self.note7 = QtGui.QSlider(self.widget)
		self.note7.setOrientation(QtCore.Qt.Vertical)
		self.note7.setObjectName(_fromUtf8("note7"))
		self.horizontalLayout.addWidget(self.note7)
		self.note7.valueChanged.connect(self.Note7)
		self.note7.setMaximum(1024)
		self.note8 = QtGui.QSlider(self.widget)
		self.note8.setOrientation(QtCore.Qt.Vertical)
		self.note8.setObjectName(_fromUtf8("note8"))
		self.horizontalLayout.addWidget(self.note8)
		self.note8.valueChanged.connect(self.Note8)
		self.note8.setMaximum(1024)
		self.note9 = QtGui.QSlider(self.widget)
		self.note9.setOrientation(QtCore.Qt.Vertical)
		self.note9.setObjectName(_fromUtf8("note9"))
		self.horizontalLayout.addWidget(self.note9)
		self.note9.valueChanged.connect(self.Note9)
		self.note9.setMaximum(1024)
		self.note10 = QtGui.QSlider(self.widget)
		self.note10.setOrientation(QtCore.Qt.Vertical)
		self.note10.setObjectName(_fromUtf8("note10"))
		self.horizontalLayout.addWidget(self.note10)
		self.note10.valueChanged.connect(self.Note10)
		self.note10.setMaximum(1024)
		self.note11 = QtGui.QSlider(self.widget)
		self.note11.setOrientation(QtCore.Qt.Vertical)
		self.note11.setObjectName(_fromUtf8("note11"))
		self.horizontalLayout.addWidget(self.note11)
		self.note11.valueChanged.connect(self.Note11)
		self.note11.setMaximum(1024)
		self.note12 = QtGui.QSlider(self.widget)
		self.note12.setOrientation(QtCore.Qt.Vertical)
		self.note12.setObjectName(_fromUtf8("note12"))
		self.horizontalLayout.addWidget(self.note12)
		self.note12.valueChanged.connect(self.Note12)
		self.note12.setMaximum(1024)
		self.note13 = QtGui.QSlider(self.widget)
		self.note13.setOrientation(QtCore.Qt.Vertical)
		self.note13.setObjectName(_fromUtf8("note13"))
		self.horizontalLayout.addWidget(self.note13)
		self.note13.valueChanged.connect(self.Note13)
		self.note13.setMaximum(1024)
		self.note14 = QtGui.QSlider(self.widget)
		self.note14.setOrientation(QtCore.Qt.Vertical)
		self.note14.setObjectName(_fromUtf8("note14"))
		self.horizontalLayout.addWidget(self.note14)
		self.note14.valueChanged.connect(self.Note14)
		self.note14.setMaximum(1024)
		self.note15 = QtGui.QSlider(self.widget)
		self.note15.setOrientation(QtCore.Qt.Vertical)
		self.note15.setObjectName(_fromUtf8("note15"))
		self.horizontalLayout.addWidget(self.note15)
		self.note15.valueChanged.connect(self.Note15)
		self.note15.setMaximum(1024)
		self.note16 = QtGui.QSlider(self.widget)
		self.note16.setOrientation(QtCore.Qt.Vertical)
		self.note16.setObjectName(_fromUtf8("note16"))
		self.horizontalLayout.addWidget(self.note16)
		self.note16.valueChanged.connect(self.Note16)
		self.note16.setMaximum(1024)
		self.widget1 = QtGui.QWidget(self.centralwidget)
		self.widget1.setGeometry(QtCore.QRect(20, 270, 901, 40))
		self.widget1.setObjectName(_fromUtf8("widget1"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget1)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		
		self.checkBox = QtGui.QCheckBox(self.widget1)		
		self.checkBox.setObjectName(_fromUtf8("checkBox"))
		self.checkBox.stateChanged.connect(self.rest1)		
		self.horizontalLayout_2.addWidget(self.checkBox)
		self.checkBox_2 = QtGui.QCheckBox(self.widget1)
		self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
		self.checkBox_2.stateChanged.connect(self.rest2)
		self.horizontalLayout_2.addWidget(self.checkBox_2)
		self.checkBox_3 = QtGui.QCheckBox(self.widget1)
		self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
		self.horizontalLayout_2.addWidget(self.checkBox_3)
		self.checkBox_3.stateChanged.connect(self.rest3)
		
		self.checkBox_4 = QtGui.QCheckBox(self.widget1)
		self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
		self.checkBox_4.stateChanged.connect(self.rest4)		
		self.horizontalLayout_2.addWidget(self.checkBox_4)
		self.checkBox_5 = QtGui.QCheckBox(self.widget1)
		self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
		self.horizontalLayout_2.addWidget(self.checkBox_5)
		self.checkBox_5.stateChanged.connect(self.rest5)
		self.checkBox_6 = QtGui.QCheckBox(self.widget1)
		self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
		self.horizontalLayout_2.addWidget(self.checkBox_6)
		self.checkBox_6.stateChanged.connect(self.rest6)
		self.checkBox_7 = QtGui.QCheckBox(self.widget1)
		self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
		self.horizontalLayout_2.addWidget(self.checkBox_7)
		self.checkBox_7.stateChanged.connect(self.rest7)
		
		self.checkBox_8 = QtGui.QCheckBox(self.widget1)
		self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
		self.horizontalLayout_2.addWidget(self.checkBox_8)
		self.checkBox_8.stateChanged.connect(self.rest8)
		self.checkBox_9 = QtGui.QCheckBox(self.widget1)
		self.checkBox_9.setObjectName(_fromUtf8("checkBox_9"))
		self.checkBox_9.stateChanged.connect(self.rest9)
		self.checkBox_10 = QtGui.QCheckBox(self.widget1)
		self.checkBox_10.setObjectName(_fromUtf8("checkBox_10"))
		self.horizontalLayout_2.addWidget(self.checkBox_10)
		self.checkBox_10.stateChanged.connect(self.rest10)
		self.checkBox_11 = QtGui.QCheckBox(self.widget1)
		self.checkBox_11.setObjectName(_fromUtf8("checkBox_11"))
		self.checkBox_11.stateChanged.connect(self.rest11)
		self.horizontalLayout_2.addWidget(self.checkBox_11)
		self.checkBox_12 = QtGui.QCheckBox(self.widget1)
		self.checkBox_12.setObjectName(_fromUtf8("checkBox_12"))
		self.horizontalLayout_2.addWidget(self.checkBox_12)
		self.checkBox_12.stateChanged.connect(self.rest12)
		self.checkBox_13 = QtGui.QCheckBox(self.widget1)
		self.checkBox_13.setObjectName(_fromUtf8("checkBox_13"))
		self.horizontalLayout_2.addWidget(self.checkBox_13)
		self.checkBox_13.stateChanged.connect(self.rest13)
		self.checkBox_14 = QtGui.QCheckBox(self.widget1)
		self.checkBox_14.setObjectName(_fromUtf8("checkBox_14"))
		self.horizontalLayout_2.addWidget(self.checkBox_14)
		self.checkBox_14.stateChanged.connect(self.rest14)
		self.checkBox_15 = QtGui.QCheckBox(self.widget1)
		self.checkBox_15.setObjectName(_fromUtf8("checkBox_15"))
		self.horizontalLayout_2.addWidget(self.checkBox_15)
		self.checkBox_15.stateChanged.connect(self.rest15)
		
		self.checkBox_16 = QtGui.QCheckBox(self.widget1)
		self.checkBox_16.setObjectName(_fromUtf8("checkBox_16"))
		self.horizontalLayout_2.addWidget(self.checkBox_16)
		self.checkBox_2.stateChanged.connect(self.rest16)
		self.horizontalLayout_2.addWidget(self.checkBox_9)
		
		self.widget2 = QtGui.QWidget(self.centralwidget)
		self.widget2.setGeometry(QtCore.QRect(20, 290, 901, 45))
		self.widget2.setObjectName(_fromUtf8("widget2"))
		self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget2)
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.sbPPQ1 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ1.setObjectName(_fromUtf8("sbPPQ1"))
		self.horizontalLayout_4.addWidget(self.sbPPQ1)
		self.sbPPQ1.valueChanged.connect(self.ppq1)
		self.sbPPQ2 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ2.setObjectName(_fromUtf8("sbPPQ2"))
		self.horizontalLayout_4.addWidget(self.sbPPQ2)
		self.sbPPQ2.valueChanged.connect(self.ppq2)
		self.sbPPQ3 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ3.setObjectName(_fromUtf8("sbPPQ3"))
		self.horizontalLayout_4.addWidget(self.sbPPQ3)
		self.sbPPQ3.valueChanged.connect(self.ppq3)
		self.sbPPQ4 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ4.setObjectName(_fromUtf8("sbPPQ4"))
		self.horizontalLayout_4.addWidget(self.sbPPQ4)
		self.sbPPQ4.valueChanged.connect(self.ppq4)
		self.sbPPQ5 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ5.setObjectName(_fromUtf8("sbPPQ5"))
		self.horizontalLayout_4.addWidget(self.sbPPQ5)
		self.sbPPQ5.valueChanged.connect(self.ppq5)
		self.sbPPQ6 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ6.setObjectName(_fromUtf8("sbPPQ6"))
		self.horizontalLayout_4.addWidget(self.sbPPQ6)
		self.sbPPQ6.valueChanged.connect(self.ppq6)
		self.sbPPQ7 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ7.setObjectName(_fromUtf8("sbPPQ7"))
		self.horizontalLayout_4.addWidget(self.sbPPQ7)
		self.sbPPQ7.valueChanged.connect(self.ppq7)
		self.sbPPQ8 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ8.setObjectName(_fromUtf8("sbPPQ8"))
		self.horizontalLayout_4.addWidget(self.sbPPQ8)
		self.sbPPQ8.valueChanged.connect(self.ppq8)
		self.sbPPQ9 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ9.setObjectName(_fromUtf8("sbPPQ9"))
		self.horizontalLayout_4.addWidget(self.sbPPQ9)
		self.sbPPQ9.valueChanged.connect(self.ppq9)
		self.sbPPQ10 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ10.setObjectName(_fromUtf8("sbPPQ10"))
		self.horizontalLayout_4.addWidget(self.sbPPQ10)
		self.sbPPQ10.valueChanged.connect(self.ppq10)
		self.sbPPQ11 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ11.setObjectName(_fromUtf8("sbPPQ11"))
		self.horizontalLayout_4.addWidget(self.sbPPQ11)
		self.sbPPQ11.valueChanged.connect(self.ppq11)
		self.sbPPQ12 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ12.setObjectName(_fromUtf8("sbPPQ12"))
		self.horizontalLayout_4.addWidget(self.sbPPQ12)
		self.sbPPQ12.valueChanged.connect(self.ppq12)
		self.sbPPQ13 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ13.setObjectName(_fromUtf8("sbPPQ13"))
		self.horizontalLayout_4.addWidget(self.sbPPQ13)
		self.sbPPQ13.valueChanged.connect(self.ppq13)
		self.sbPPQ14 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ14.setObjectName(_fromUtf8("sbPPQ14"))
		self.horizontalLayout_4.addWidget(self.sbPPQ14)
		self.sbPPQ14.valueChanged.connect(self.ppq14)
		self.sbPPQ15 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ15.setObjectName(_fromUtf8("sbPPQ15"))
		self.horizontalLayout_4.addWidget(self.sbPPQ15)
		self.sbPPQ15.valueChanged.connect(self.ppq15)
		self.sbPPQ16 = QtGui.QSpinBox(self.widget2)
		self.sbPPQ16.setObjectName(_fromUtf8("sbPPQ16"))
		self.horizontalLayout_4.addWidget(self.sbPPQ16)
		self.sbPPQ16.valueChanged.connect(self.ppq16)
		
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 949, 45))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		MainWindow.setMenuBar(self.menubar)
		
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		self.menuScene = QtGui.QMenu(self.menubar)
		self.menuScene.setObjectName(_fromUtf8("menuScene"))
		self.menuEdit = QtGui.QMenu(self.menubar)
		self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
		self.menuPattern = QtGui.QMenu(self.menubar)
		self.menuPattern.setObjectName(_fromUtf8("menuPattern"))
		
		self.actionLoad_scene = QtGui.QAction(MainWindow)
		self.actionLoad_scene.setObjectName(_fromUtf8("actionLoad_scene"))
		self.actionSave_scene = QtGui.QAction(MainWindow)
		self.actionLoad_scene.triggered.connect(self.Load)
		self.actionSave_scene.setObjectName(_fromUtf8("actionSave_scene"))
		self.actionSave_scene.triggered.connect(self.Save)
		self.actionExit = QtGui.QAction(MainWindow)
		
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionCopy = QtGui.QAction(MainWindow)
		self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
		self.actionCopy.triggered.connect(self.Copy)
		self.actionPaste = QtGui.QAction(MainWindow)
		self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
		self.actionPaste.triggered.connect(self.Paste)
		self.actionNextStep = QtGui.QAction(MainWindow)
		self.actionNextStep.setObjectName(_fromUtf8("actionNextStep"))
		self.actionNextStep.triggered.connect(self.NextStep)
		self.actionPrevStep = QtGui.QAction(MainWindow)
		self.actionPrevStep.setObjectName(_fromUtf8("actionPrevStep"))
		self.actionPrevStep.triggered.connect(self.PrevStep)
		self.actionOptions = QtGui.QAction(MainWindow)
		self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
		self.actionOptions.triggered.connect(self.Options)
		self.actionRandom_scene = QtGui.QAction(MainWindow)
		self.actionRandom_scene.setObjectName(_fromUtf8("actionRandom_scene"))
		self.actionRandom_scene.triggered.connect(self.Randomize)
		self.actionTranspose = QtGui.QAction(MainWindow)
		self.actionTranspose.setObjectName(_fromUtf8("actionTranspose"))
		self.actionTranspose.triggered.connect(self.TransposeDlg)
		
		self.actionRandomPPQ = QtGui.QAction(MainWindow)
		self.actionRandomPPQ.setObjectName(_fromUtf8("actionRandomPPQ"))
		self.actionRandomPPQ.triggered.connect(self.RandomPPQ)
		
		self.actionRandomRepeats= QtGui.QAction(MainWindow)
		self.actionRandomRepeats.setObjectName(_fromUtf8("actionRandomRepeats"))
		self.actionRandomRepeats.triggered.connect(self.RandomRepeats)
		
		self.actionRandomRests = QtGui.QAction(MainWindow)
		self.actionRandomRests.setObjectName(_fromUtf8("actionRandomRests"))
		self.actionRandomRests.triggered.connect(self.RandomRests)
		
		self.actionStop = QtGui.QAction(MainWindow)
		self.actionStop.setObjectName(_fromUtf8("actionSavePattern"))
		self.actionStop.triggered.connect(self.Stop)
		self.actionPlay = QtGui.QAction(MainWindow)
		self.actionPlay.setObjectName(_fromUtf8("actionSavePattern"))
		self.actionPlay.triggered.connect(self.Play)
		
		
		self.actionSavePattern = QtGui.QAction(MainWindow)
		self.actionSavePattern.setObjectName(_fromUtf8("actionSavePattern"))
		self.actionSavePattern.triggered.connect(self.SavePatterns)
		self.actionLoadPattern = QtGui.QAction(MainWindow)
		self.actionLoadPattern.setObjectName(_fromUtf8("actionLoadPattern"))
		self.actionLoadPattern.triggered.connect(self.LoadPatterns)
		
		self.actionAddPattern = QtGui.QAction(MainWindow)
		self.actionAddPattern.setObjectName(_fromUtf8("actionAddPattern"))
		self.actionAddPattern.triggered.connect(self.AddPattern)
		self.actionDelPattern = QtGui.QAction(MainWindow)
		self.actionDelPattern.setObjectName(_fromUtf8("actionDelPattern"))
		self.actionDelPattern.triggered.connect(self.DelPattern)
		

		
	
		self.actionNextPattern = QtGui.QAction(MainWindow)
		self.actionNextPattern.setObjectName(_fromUtf8("actionNextPattern"))
		self.actionNextPattern.triggered.connect(self.NextPattern)
		
		self.actionPrevPattern = QtGui.QAction(MainWindow)
		self.actionPrevPattern.setObjectName(_fromUtf8("actionPrevPattern"))
		self.actionPrevPattern.triggered.connect(self.PrevPattern)
		
		self.actionJumpPattern = QtGui.QAction(MainWindow)
		self.actionJumpPattern.setObjectName(_fromUtf8("actionJumpPattern"))
		self.actionJumpPattern.triggered.connect(self.JumpPattern)
		
		
		
		
		self.menuFile.addAction(self.actionLoad_scene)
		self.menuFile.addAction(self.actionSave_scene)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionExit)
	
		
		self.menuEdit.addAction(self.actionCopy)
		self.menuEdit.addAction(self.actionPaste)
		self.menuEdit.addSeparator()
		self.menuEdit.addAction(self.actionOptions)
		
		
		self.menuScene.addAction(self.actionRandom_scene)
		self.menuScene.addAction(self.actionRandomPPQ)
		self.menuScene.addAction(self.actionRandomRests)
		self.menuScene.addAction(self.actionRandomRepeats)
		self.menuScene.addSeparator()		
		self.menuScene.addAction(self.actionPrevStep)
		self.menuScene.addAction(self.actionNextStep)
		self.menuScene.addAction(self.actionTranspose)
		
		self.menuPattern.addAction(self.actionLoadPattern)
		self.menuPattern.addAction(self.actionSavePattern)
		self.menuPattern.addSeparator()
		self.menuPattern.addAction(self.actionAddPattern)
		self.menuPattern.addAction(self.actionDelPattern)		
		self.menuPattern.addAction(self.actionNextPattern)
		self.menuPattern.addAction(self.actionPrevPattern)
		self.menuPattern.addAction(self.actionJumpPattern)
		
		
		

		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuEdit.menuAction())
		self.menubar.addAction(self.menuScene.menuAction())
		self.menubar.addAction(self.menuPattern.menuAction())
		
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def UpdateUi(self):
		
		seq = self.GetSequencer()
		
		self.note1.setValue(seq.GetNote(0))
		self.note2.setValue(seq.GetNote(1))
		self.note3.setValue(seq.GetNote(2))
		self.note4.setValue(seq.GetNote(3))
		self.note5.setValue(seq.GetNote(4))
		self.note6.setValue(seq.GetNote(5))
		self.note7.setValue(seq.GetNote(6))
		self.note8.setValue(seq.GetNote(7))
		self.note9.setValue(seq.GetNote(8))
		self.note10.setValue(seq.GetNote(9))
		self.note11.setValue(seq.GetNote(10))
		self.note12.setValue(seq.GetNote(11))
		self.note13.setValue(seq.GetNote(12))
		self.note14.setValue(seq.GetNote(13))
		self.note15.setValue(seq.GetNote(14))
		self.note16.setValue(seq.GetNote(15))
		
		self.sbPPQ1.setValue(seq.GetPPQ(0))
		self.sbPPQ2.setValue(seq.GetPPQ(1))
		self.sbPPQ3.setValue(seq.GetPPQ(2))
		self.sbPPQ4.setValue(seq.GetPPQ(3))
		self.sbPPQ5.setValue(seq.GetPPQ(4))
		self.sbPPQ6.setValue(seq.GetPPQ(5))
		self.sbPPQ7.setValue(seq.GetPPQ(6))
		self.sbPPQ8.setValue(seq.GetPPQ(7))
		self.sbPPQ9.setValue(seq.GetPPQ(8))
		self.sbPPQ10.setValue(seq.GetPPQ(9))
		self.sbPPQ11.setValue(seq.GetPPQ(10))
		self.sbPPQ12.setValue(seq.GetPPQ(11))
		self.sbPPQ13.setValue(seq.GetPPQ(12))
		self.sbPPQ14.setValue(seq.GetPPQ(13))
		self.sbPPQ15.setValue(seq.GetPPQ(14))
		self.sbPPQ16.setValue(seq.GetPPQ(15))
		
		self.repeat1.setValue(seq.GetRepeat(0))
		self.repeat2.setValue(seq.GetRepeat(1))
		self.repeat3.setValue(seq.GetRepeat(2))
		self.repeat4.setValue(seq.GetRepeat(3))
		self.repeat5.setValue(seq.GetRepeat(4))
		self.repeat6.setValue(seq.GetRepeat(5))
		self.repeat7.setValue(seq.GetRepeat(6))
		self.repeat8.setValue(seq.GetRepeat(7))
		self.repeat9.setValue(seq.GetRepeat(8))
		self.repeat10.setValue(seq.GetRepeat(9))
		self.repeat11.setValue(seq.GetRepeat(10))
		self.repeat12.setValue(seq.GetRepeat(11))
		self.repeat13.setValue(seq.GetRepeat(12))
		self.repeat14.setValue(seq.GetRepeat(13))
		self.repeat15.setValue(seq.GetRepeat(14))
		self.repeat16.setValue(seq.GetRepeat(15))
		
		self.checkBox.setChecked(seq.GetRest(0))
		self.checkBox_2.setChecked(seq.GetRest(1))
		self.checkBox_3.setChecked(seq.GetRest(2))
		self.checkBox_4.setChecked(seq.GetRest(3))
		self.checkBox_5.setChecked(seq.GetRest(4))
		self.checkBox_6.setChecked(seq.GetRest(5))
		self.checkBox_7.setChecked(seq.GetRest(6))
		self.checkBox_8.setChecked(seq.GetRest(7))
		self.checkBox_9.setChecked(seq.GetRest(8))
		self.checkBox_10.setChecked(seq.GetRest(9))
		self.checkBox_11.setChecked(seq.GetRest(10))
		self.checkBox_12.setChecked(seq.GetRest(11))
		self.checkBox_13.setChecked(seq.GetRest(12))
		self.checkBox_14.setChecked(seq.GetRest(13))
		self.checkBox_15.setChecked(seq.GetRest(14))
		self.checkBox_16.setChecked(seq.GetRest(15))
		
		
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.checkBox.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_2.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_4.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_3.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_8.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_6.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_5.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_7.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_16.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_11.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_9.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_15.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_10.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_12.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_13.setText(_translate("MainWindow", "Rest", None))
		self.checkBox_14.setText(_translate("MainWindow", "Rest", None))
		
		self.menuFile.setTitle(_translate("MainWindow", "File", None))
		self.menuScene.setTitle(_translate("MainWindow", "Sequencer", None))
		self.menuEdit.setTitle(_translate("MainWindw","Edit",None))
		self.menuPattern.setTitle(_translate("MainWindow","Pattern",None))
		
		self.actionLoad_scene.setText(_translate("MainWindow", "Load Seq", None))
		self.actionSave_scene.setText(_translate("MainWindow", "Save Seq", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionCopy.setText(_translate("MainWindow", "Copy", None))
		self.actionPaste.setText(_translate("MainWindow", "Paste", None))
		self.actionPrevStep.setText(_translate("MainWindow", "Prev Step", None))
		self.actionNextStep.setText(_translate("MainWindow", "Next Step", None))		
		self.actionOptions.setText(_translate("MainWindow", "Options", None))
		self.actionRandom_scene.setText(_translate("MainWindow", "Random Scene", None))
		self.actionTranspose.setText(_translate("MainWindow", "Transpose", None))
		self.actionRandomPPQ.setText(_translate("MainWindow", "Random PPQ", None))
		self.actionRandomRepeats.setText(_translate("MainWindow", "Random Repeats", None))
		self.actionRandomRests.setText(_translate("MainWindow", "Random Rests", None))
				
		self.actionAddPattern.setText(_translate("MainWindow","Add Pattern",None))
		self.actionNextPattern.setText(_translate("MainWindow","Next Pattern",None))
		self.actionPrevPattern.setText(_translate("MainWindow","Prev Pattern",None))
		self.actionJumpPattern.setText(_translate("MainWindow","Jump to Pattern",None))
		self.actionSavePattern.setText(_translate("MainWindow","Save Patterns",None))
		self.actionLoadPattern.setText(_translate("MainWindow","Load Patterns",None))
	
if __name__ == '__main__':
	
	app = QApplication(sys.argv)  # A new instance of QApplication
	window = QMainWindow()
	app.setStyleSheet("""
		.QMainWindow {
			    border:20px solid black;
			    border-radius: 10px;
			    background-color: rgb(80,80,125);
			 }
		.QDial { border:20px solid black;
			    border-radius: 10px;
			    background-color: rgb(120,120,120);
			 }
		.QPushButton {
			    background-color: rgb(150,150,200);
			 }
		""")
	ui = Ui_MainWindow()
	ui.setupUi(window)
	window.show()
sys.exit(app.exec_())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                