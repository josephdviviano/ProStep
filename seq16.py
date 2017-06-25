# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'seq16.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui,Qt
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QMainWindow,QApplication
from mido.sockets import PortServer,connect
import pickle
import math
import sys
import mido
import midi
import mopho
import patterns

from mido import Message,MidiFile,MidiTrack
from mido.ports import MultiPort

TEMPO=145.0

PPQ_WHOLE=96
PLAY_LEN=4*PPQ_WHOLE
TX_DELAY=0.01

MIDI_CHANNEL=1
MIDIKB_CHANNEL=1

fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def NoteToMopho(n):
	
	n = n % 12
	o = n / 12
	if(o > 4): o = 4
	
	return o*24+n*2
	
def MophoToNote(n):
	n = n % 24
	o = o / 24
	note = 24+n+o*12

note_names = {}
for i in range(0,127):
	n = i % 12
	s = midi.name_notes[n]
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


class Worker(QThread):
	
	def __init__(self,mainwindow,parent=None):
		QThread.__init__(self,parent)
		self.exiting = False
		self.mainwindow = mainwindow
		self.scene_len = PLAY_LEN
		self.ppq = -1
		self.cur_ppq = -1
		self.input_buffer = [0]*16
		self.cur_step = 0
		self.note = 0
		self.repeats = 0
		self.cur_note = 0
		self.rest = 0
		self.midi_channel = MIDI_CHANNEL
		self.kb_channel    = MIDIKB_CHANNEL
		self.midi_input = None
		self.midi_output = None
		
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
				
				if(key[0] == 248):
					self.ppq = self.ppq+1
					seq = self.mainwindow.GetSequencer()
					seq.UpdateMIDI()
					self.emit(QtCore.SIGNAL("UpdateUi()"))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
							
				elif(key[0] >= 0x90 and key[0] <= 0x9F):
					seq = self.mainwindow.GetSequencer()
					seq.UpdateMIDIInput(key)
					self.emit(QtCore.SIGNAL("UpdateUi()"))
					
				else:		
					self.midi_output.send(msg)

class Ui_Config(QtGui.QDialog):

		def __init__(self,parent):
			super(QtGui.QDialog,self).__init__()
			self.parent = parent
			
			outp= mido.get_output_names()
			inp = mido.get_input_names()

			dlg = self
			self.layout = QtGui.QHBoxLayout()
			self.vlayout = QtGui.QVBoxLayout()
			
			self.inputs = QtGui.QComboBox()
			self.clocks = QtGui.QComboBox()
			self.outputs = QtGui.QComboBox()
			
			self.inputs.addItem("None")
			self.clocks.addItem("None")
			self.outputs.addItem("None")
			
			for i in inp:
				self.inputs.addItem(i)
				self.clocks.addItem(i)
			
			for i in outp:
				self.outputs.addItem(i)
			self.inp_chan = QtGui.QComboBox()
			self.outp_chan = QtGui.QComboBox()
			for i in range(15):
				self.inp_chan.addItem(str(i))
				self.outp_chan.addItem(str(i))
			
			self.resize(512,200)
			
			self.buttons = QtGui.QDialogButtonBox( QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
			self.buttons.accepted.connect(self.accepted)
			self.buttons.rejected.connect(self.rejected)
			self.buttons.move
			self.layout.setGeometry(QtCore.QRect(10,10,510,50))
			self.buttons.setGeometry(QtCore.QRect(300,160,120,40))
			self.layout.addWidget(self.inputs)
			self.layout.addWidget(self.clocks)
			self.layout.addWidget(self.outputs)
			self.layout.addWidget(self.inp_chan)
			self.layout.addWidget(self.outp_chan)
			dlg.setLayout(self.layout)
			dlg.setWindowTitle("MIDI Setup")
			dlg.show()
			dlg.exec_()
			
			self.input_channel = 0
			self.output_channel = 0
			
		def accepted(self):
			#MIDI_Close()
			bMidi = False
			
			if(self.inputs.currentText() != 'None'):
				key = mido.open_input(self.inputs.currentText())			
				bMidi = True
				if(self.inputs.currentText() == self.clocks.currentText()):
					clk = key
				elif(self.clocks.currentText() != "None"):
					clk  = mido.open_input(self.clocks.currentText())
					bMidi = True
					
			if(self.outputs.currentText() != "None"):
				out = mido.open_output(self.outputs.currentText())
				bMidi = True
			
			if(bMidi == True):
				midi.MIDI_SetInOut(key,clk,out)
				
			self.parent.input_channel = int(self.inp_chan.currentText())
			self.parent.midi_channel = int(self.outp_chan.currentText())
			
			self.close()
			
		def rejected(self):
			self.close()

class Sequencer:
	
	def __init__(self):
		self.notes = [0]*16
		self.cur_step = 0
		self.ppq = [0]*16
		self.repeats = [0]*16
		self.rests = [0]*16
		self.num_steps = 16
		self.mainwindow = None
		
		self.cur_rest = 0
		self.cur_ppq = 6
		self.cur_repeats = 0
		self.cur_note = 0
		self.cur_note = 0		
		self.ppq_cnt = 0
		self.cur_instep=0
		
		self.midi_input = None
		self.midi_output = None
		self.kb_channel = 0
		self.midi_channel = 0
		
	def UpdateMIDI(self):
		if(self.midi_output is None):
			self.midi_input,self.midi_output = midi.MIDI_GetInOut()
		self.ppq_cnt = self.ppq_cnt+1
		if(self.ppq_cnt >= self.cur_ppq):
			self.ppq_cnt = 0
			self.cur_repeats = self.cur_repeats - 1
			if(self.cur_repeats < 0):
				self.cur_step = self.cur_step + 1
				self.cur_step = self.cur_step % 16						
				if(self.cur_step >= self.num_steps):
					self.cur_step = 0
				if(self.cur_rest == 0):
					self.midi_output.send(midi.MSG([0x80+self.midi_channel,self.cur_note,127]))
				self.cur_rest  = self.rests[self.cur_step]
				self.cur_note = self.notes[self.cur_step]
				self.cur_repeats = self.repeats[self.cur_step]
				self.cur_ppq = self.ppq[self.cur_step]
			else:
				if(self.cur_rest == 0):
					self.midi_output.send(midi.MSG([0x80+self.midi_channel,self.cur_note,127]))
				
				
			if(self.cur_rest != 1):
				self.midi_output.send(midi.MSG([0x90+self.midi_channel,self.cur_note,127]))
				
	def UpdateMIDIInput(self,key):
		#if(key[0] == 0x90 + self.kb_channel):			
		self.notes[self.cur_instep] = key[1]
		self.cur_instep = self.cur_instep + 1
		self.cur_instep = self.cur_instep % 16
		
		
	def Randomize(self):
		seq = patterns.GEN_CreatePattern()
		
		for i in range(16):
			seq[i] = seq[i] + 24
			if(seq[i] < 24): seq[i] = 24
			if(seq[i] > 80): seq[i] = 80
			self.notes[i] = seq[i]
			self.ppq[i] = 6
			self.repeats[i] = 0
			
	def GetNote(self,i):
		return int((self.notes[i]/127.0)*1024)
		
class Ui_MainWindow(object):
	def __init__(self):
		self.sequencer = Sequencer()
		
	def GetSequencer(self):
		return self.sequencer
		
	def UpdateMIDI(self):
		seq = self.GetSequencer()
		seq.UpdateMIDI()
		
	def UpdateMIDIInput(self,msg):
		seq = self.GetSequencer()
		seq.UpdateMIDIInput(msg)
			
	def Save(self):
		filename = QtGui.QFileDialog.getSaveFileName(self.mainwindow, 'Save File', '.')
		mid = MidiFile()
		mid.ticks_per_beat = 24
		track = MidiTrack()
		mid.tracks.append(track)
		
		for i in range(16):
			
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
		mid.save(str(filename))
			
				
	def Load(self):
		filename = QtGui.QFileDialog.getOpenFileName(self.mainwindow, 'Open File', '.')
		
	
	def Options(self):
		
		ui = Ui_Config(self)
		
		try:
			self.thread.midi_input, self.thread.midi_output = midi.MIDI_GetInOut()
			self.thread.kb_channel = self.input_channel 
			self.thread.midi_channel = self.midi_channel
		except:
			pass
		self.sequencer.midi_channel = self.midi_channel
		self.sequencer.kb_channel = self.input_channel
		
	def Copy(self):
		pass
		
	def Paste(self):
		pass
		
	def PrevStep(self):
		self.thread.cur_step = self.thread.cur_step - 1
		if(self.thread.cur_step < 0): self.cur_step = 15
		
	def NextStep(self):
		self.thread.cur_step = self.thread.cur_step + 1
		self.thread.cur_step = self.thread.cur_step % 16
		
	def Randomize(self):
		seq = self.GetSequencer()
		seq.Randomize()
		self.UpdateUi()
		
	def SetSteps(self,value):
		seq = self.GetSequencer()
		seq.num_steps = value
		
	def Note1(self,value):
		value = int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[0] = value
		self.lcdNumber.display(note_names[value])
		
	def Note2(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[1] = value
		self.lcdNumber.display(note_names[value])
		
	def Note3(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[2] = value
		self.lcdNumber.display(note_names[value])
		
	def Note4(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[3] = value
		self.lcdNumber.display(note_names[value])
				
	def Note5(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[4] = value
		self.lcdNumber.display(note_names[value])
		
	def Note6(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[5] = value
		self.lcdNumber.display(note_names[value])
		
	def Note7(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[6] = value
		self.lcdNumber.display(note_names[value])
		
	def Note8(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[7] = value
		self.lcdNumber.display(note_names[value])
		
	def Note9(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[8] = value
		self.lcdNumber.display(note_names[value])
		
	def Note10(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[9] = value
		self.lcdNumber.display(note_names[value])
		
	def Note11(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[10] = value
		self.lcdNumber.display(note_names[value])
		
	def Note12(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[11] = value
		self.lcdNumber.display(note_names[value])
		
	def Note13(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[12] = value
		self.lcdNumber.display(note_names[value])
		
	def Note14(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[13] = value
		self.lcdNumber.display(note_names[value])
		
	def Note15(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[14] = value
		self.lcdNumber.display(note_names[value])
		
	def Note16(self,value):
		value=int(math.ceil((value/1024.0)*127))
		seq = self.GetSequencer()
		seq.notes[15] = value
		self.lcdNumber.display(note_names[value])
		
	
	def ppq1(self,value):
		seq = self.GetSequencer()
		seq.ppq[0] = value
	def ppq2(self,value):
		seq = self.GetSequencer()
		seq.ppq[1] = value
	def ppq3(self,value):
		seq = self.GetSequencer()
		seq.ppq[2] = value
	def ppq4(self,value):
		seq = self.GetSequencer()
		seq.ppq[3] = value
	def ppq5(self,value):
		seq = self.GetSequencer()
		seq.ppq[4] = value
	def ppq6(self,value):
		seq = self.GetSequencer()
		seq.ppq[5] = value
	def ppq7(self,value):
		seq = self.GetSequencer()
		seq.ppq[6] = value
	def ppq8(self,value):
		seq = self.GetSequencer()
		seq.ppq[7] = value
	def ppq9(self,value):
		seq = self.GetSequencer()
		seq.ppq[8] = value
	def ppq10(self,value):
		seq = self.GetSequencer()
		seq.ppq[9] = value
	def ppq11(self,value):
		seq = self.GetSequencer()
		seq.ppq[10] = value
	def ppq12(self,value):
		seq = self.GetSequencer()
		seq.ppq[11] = value
	def ppq13(self,value):
		seq = self.GetSequencer()
		seq.ppq[12] = value
	def ppq14(self,value):
		seq = self.GetSequencer()
		seq.ppq[13] = value
	def ppq15(self,value):
		seq = self.GetSequencer()
		seq.ppq[14] = value
	def ppq16(self,value):
		seq = self.GetSequencer()
		seq.ppq[15] = value
	
	def rest1(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[0] = value
	def rest2(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[1] = value
	def rest3(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[2] = value
	def rest4(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[3] = value
	def rest5(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[4] = value
	def rest6(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[5] = value
	def rest7(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[6] = value
	def rest8(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[7] = value
	def rest9(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[8] = value
	def rest10(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[9] = value
	def rest11(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[10] = value
	def rest12(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[11] = value
	def rest13(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[12] = value
	def rest14(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[13] = value
	def rest15(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[14] = value
	def rest16(self,state):
		value = 0
		if(state == QtCore.Qt.Checked): value = 1
		seq = self.GetSequencer()
		seq.rests[15] = value
	
	def Repeat1(self,value):
		seq = self.GetSequencer()
		seq.repeats[0] = value
	def Repeat2(self,value):
		seq = self.GetSequencer()
		seq.repeats[1] = value
	def Repeat3(self,value):
		seq = self.GetSequencer()
		seq.repeats[2] = value
	def Repeat4(self,value):
		seq = self.GetSequencer()
		seq.repeats[3] = value
	def Repeat5(self,value):
		seq = self.GetSequencer()
		seq.repeats[4] = value
	def Repeat6(self,value):
		seq = self.GetSequencer()
		seq.repeats[5] = value
	def Repeat7(self,value):
		seq = self.GetSequencer()
		seq.repeats[6] = value
	def Repeat8(self,value):
		seq = self.GetSequencer()
		seq.repeats[7] = value
	def Repeat9(self,value):
		seq = self.GetSequencer()
		seq.repeats[8] = value
	def Repeat10(self,value):
		seq = self.GetSequencer()
		seq.repeats[9] = value
	def Repeat11(self,value):
		seq = self.GetSequencer()
		seq.repeats[10] = value
	def Repeat12(self,value):
		seq = self.GetSequencer()
		seq.repeats[11] = value
	def Repeat13(self,value):
		seq = self.GetSequencer()
		seq.repeats[12] = value
	def Repeat14(self,value):
		seq = self.GetSequencer()
		seq.repeats[13] = value
	def Repeat15(self,value):
		seq = self.GetSequencer()
		seq.repeats[14] = value
	def Repeat16(self,value):
		seq = self.GetSequencer()
		seq.repeats[15] = value
	
	def setupUi(self, MainWindow,bMDIChild=False):
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
		
		if(bMDIChild == False):
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
		self.checkBox_4 = QtGui.QCheckBox(self.widget1)
		self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
		self.checkBox_4.stateChanged.connect(self.rest3)		
		self.horizontalLayout_2.addWidget(self.checkBox_4)
		self.checkBox_3 = QtGui.QCheckBox(self.widget1)
		self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
		self.horizontalLayout_2.addWidget(self.checkBox_3)
		self.checkBox_3.stateChanged.connect(self.rest4)
		self.checkBox_8 = QtGui.QCheckBox(self.widget1)
		self.checkBox_8.setObjectName(_fromUtf8("checkBox_8"))
		self.horizontalLayout_2.addWidget(self.checkBox_8)
		self.checkBox_8.stateChanged.connect(self.rest5)
		self.checkBox_6 = QtGui.QCheckBox(self.widget1)
		self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
		self.horizontalLayout_2.addWidget(self.checkBox_6)
		self.checkBox_6.stateChanged.connect(self.rest6)
		self.checkBox_5 = QtGui.QCheckBox(self.widget1)
		self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
		self.horizontalLayout_2.addWidget(self.checkBox_5)
		self.checkBox_5.stateChanged.connect(self.rest7)
		self.checkBox_7 = QtGui.QCheckBox(self.widget1)
		self.checkBox_7.setObjectName(_fromUtf8("checkBox_7"))
		self.horizontalLayout_2.addWidget(self.checkBox_7)
		self.checkBox_7.stateChanged.connect(self.rest8)
		self.checkBox_16 = QtGui.QCheckBox(self.widget1)
		self.checkBox_16.setObjectName(_fromUtf8("checkBox_16"))
		self.horizontalLayout_2.addWidget(self.checkBox_16)
		self.checkBox_2.stateChanged.connect(self.rest9)
		self.checkBox_11 = QtGui.QCheckBox(self.widget1)
		self.checkBox_11.setObjectName(_fromUtf8("checkBox_11"))
		self.checkBox_11.stateChanged.connect(self.rest10)
		self.horizontalLayout_2.addWidget(self.checkBox_11)
		self.checkBox_9 = QtGui.QCheckBox(self.widget1)
		self.checkBox_9.setObjectName(_fromUtf8("checkBox_9"))
		self.checkBox_9.stateChanged.connect(self.rest11)
		self.horizontalLayout_2.addWidget(self.checkBox_9)
		self.checkBox_15 = QtGui.QCheckBox(self.widget1)
		self.checkBox_15.setObjectName(_fromUtf8("checkBox_15"))
		self.horizontalLayout_2.addWidget(self.checkBox_15)
		self.checkBox_15.stateChanged.connect(self.rest12)
		self.checkBox_10 = QtGui.QCheckBox(self.widget1)
		self.checkBox_10.setObjectName(_fromUtf8("checkBox_10"))
		self.horizontalLayout_2.addWidget(self.checkBox_10)
		self.checkBox_10.stateChanged.connect(self.rest13)
		self.checkBox_12 = QtGui.QCheckBox(self.widget1)
		self.checkBox_12.setObjectName(_fromUtf8("checkBox_12"))
		self.horizontalLayout_2.addWidget(self.checkBox_12)
		self.checkBox_12.stateChanged.connect(self.rest14)
		self.checkBox_13 = QtGui.QCheckBox(self.widget1)
		self.checkBox_13.setObjectName(_fromUtf8("checkBox_13"))
		self.horizontalLayout_2.addWidget(self.checkBox_13)
		self.checkBox_13.stateChanged.connect(self.rest15)
		
		self.checkBox_14 = QtGui.QCheckBox(self.widget1)
		self.checkBox_14.setObjectName(_fromUtf8("checkBox_14"))
		self.horizontalLayout_2.addWidget(self.checkBox_14)
		self.checkBox_14.stateChanged.connect(self.rest16)
		
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
		self.actionBreedPatch = QtGui.QAction(MainWindow)
		self.actionBreedPatch.setObjectName(_fromUtf8("actionBreedPatch"))
		self.actionBreedPatch.triggered.connect(self.BreedPatch)
		
		self.menuFile.addAction(self.actionLoad_scene)
		self.menuFile.addAction(self.actionSave_scene)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionExit)
		self.menuScene.addAction(self.actionCopy)
		self.menuScene.addAction(self.actionPaste)
		self.menuScene.addAction(self.actionRandom_scene)
		self.menuScene.addAction(self.actionBreedPatch)
		self.menuScene.addAction(self.actionPrevStep)
		self.menuScene.addAction(self.actionNextStep)
		self.menuScene.addAction(self.actionOptions)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuScene.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		self.Randomize()
	
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
		
		self.sbPPQ1.setValue(seq.ppq[0])
		self.sbPPQ2.setValue(seq.ppq[1])
		self.sbPPQ3.setValue(seq.ppq[2])
		self.sbPPQ4.setValue(seq.ppq[3])
		self.sbPPQ5.setValue(seq.ppq[4])
		self.sbPPQ6.setValue(seq.ppq[5])
		self.sbPPQ7.setValue(seq.ppq[6])
		self.sbPPQ8.setValue(seq.ppq[7])
		self.sbPPQ9.setValue(seq.ppq[8])
		self.sbPPQ10.setValue(seq.ppq[9])
		self.sbPPQ11.setValue(seq.ppq[10])
		self.sbPPQ12.setValue(seq.ppq[11])
		self.sbPPQ13.setValue(seq.ppq[12])
		self.sbPPQ14.setValue(seq.ppq[13])
		self.sbPPQ15.setValue(seq.ppq[14])
		self.sbPPQ16.setValue(seq.ppq[15])
		
	def BreedPatch(self):
		sysex = realtime_gen()
		midi_output.send(MSG(sysex))
		
	def retranslateUi(self, MainWindow,bMDIChild=False):
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
		self.menuScene.setTitle(_translate("MainWindow", "Scene", None))
		self.actionLoad_scene.setText(_translate("MainWindow", "Load scene", None))
		self.actionSave_scene.setText(_translate("MainWindow", "Save scene", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionCopy.setText(_translate("MainWindow", "Copy", None))
		self.actionPaste.setText(_translate("MainWindow", "Paste", None))
		self.actionPrevStep.setText(_translate("MainWindow", "Prev Step", None))
		self.actionNextStep.setText(_translate("MainWindow", "Next Step", None))		
		self.actionOptions.setText(_translate("MainWindow", "Options", None))
		self.actionRandom_scene.setText(_translate("MainWindow", "Random Scene", None))
		self.actionBreedPatch.setText(_translate("MainWindow", "Breed Patch", None))

if __name__ == '__main__':
	
	app = QApplication(sys.argv)  # A new instance of QApplication
	window = QMainWindow()
	app.setStyleSheet("""
		.QMainWindow {
			    border:20px solid black;
			    border-radius: 10px;
			    background-color: rgb(50,50,55);
			 }
		.QDial { border:20px solid black;
			    border-radius: 10px;
			    background-color: rgb(100,100,100);
			 }
		.QPushButton {
			    background-color: rgb(200,200,200);
			 }
		""")
	ui = Ui_MainWindow()
	ui.setupUi(window)
	window.show()
	sys.exit(app.exec_())