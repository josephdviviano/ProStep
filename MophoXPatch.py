# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mophoxpatch.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import pickle
import math
import sys,os
from random import *
import midi
import mopho
import patterns

import mido
from mido import Message,MidiFile,MidiTrack
from mido.sockets import PortServer,connect
from mido.ports import MultiPort
import oscillator


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

		
class Ui_ConfigDialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(426, 207)
		Dialog.setStyleSheet(_fromUtf8("color : rgb(255,255,255);\n"
	"background-color: rgb(93,93,93);"))
		self.buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.buttonBox.setGeometry(QtCore.QRect(70, 140, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
		self.cbInputs = QtGui.QComboBox(Dialog)
		self.cbInputs.setGeometry(QtCore.QRect(102, 51, 73, 30))
		self.cbInputs.setObjectName(_fromUtf8("cbInputs"))
		self.cbClock = QtGui.QComboBox(Dialog)
		self.cbClock.setGeometry(QtCore.QRect(285, 51, 73, 30))
		self.cbClock.setObjectName(_fromUtf8("cbClock"))
		self.cbOutput1 = QtGui.QComboBox(Dialog)
		self.cbOutput1.setGeometry(QtCore.QRect(60, 82, 73, 30))
		self.cbOutput1.setObjectName(_fromUtf8("cbOutput1"))
		self.cbOutput2 = QtGui.QComboBox(Dialog)
		self.cbOutput2.setGeometry(QtCore.QRect(139, 82, 73, 30))
		self.cbOutput2.setObjectName(_fromUtf8("cbOutput2"))
		self.cbOutput3 = QtGui.QComboBox(Dialog)
		self.cbOutput3.setGeometry(QtCore.QRect(218, 82, 73, 30))
		self.cbOutput3.setObjectName(_fromUtf8("cbOutput3"))
		self.cbOutput4 = QtGui.QComboBox(Dialog)
		self.cbOutput4.setGeometry(QtCore.QRect(297, 82, 73, 30))
		self.cbOutput4.setObjectName(_fromUtf8("cbOutput4"))
		self.cbSync4 = QtGui.QComboBox(Dialog)
		self.cbSync4.setGeometry(QtCore.QRect(298, 112, 73, 30))
		self.cbSync4.setObjectName(_fromUtf8("cbSync4"))
		self.cbSync2 = QtGui.QComboBox(Dialog)
		self.cbSync2.setGeometry(QtCore.QRect(140, 112, 73, 30))
		self.cbSync2.setObjectName(_fromUtf8("cbSync2"))
		self.cbSync1 = QtGui.QComboBox(Dialog)
		self.cbSync1.setGeometry(QtCore.QRect(61, 112, 73, 30))
		self.cbSync1.setObjectName(_fromUtf8("cbSync1"))
		self.cbSync3 = QtGui.QComboBox(Dialog)
		self.cbSync3.setGeometry(QtCore.QRect(219, 112, 73, 30))
		self.cbSync3.setObjectName(_fromUtf8("cbSync3"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(11, 51, 26, 30))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(194, 51, 25, 30))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QtGui.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(11, 81, 39, 30))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(Dialog)
		self.label_4.setGeometry(QtCore.QRect(11, 111, 44, 30))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.label_5 = QtGui.QLabel(Dialog)
		self.label_5.setGeometry(QtCore.QRect(11, 21, 65, 30))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.sbChannel = QtGui.QSpinBox(Dialog)
		self.sbChannel.setGeometry(QtCore.QRect(82, 21, 33, 20))
		self.sbChannel.setMinimum(1)
		self.sbChannel.setMaximum(16)
		self.sbChannel.setObjectName(_fromUtf8("sbChannel"))
		self.sbVoices = QtGui.QSpinBox(Dialog)
		self.sbVoices.setGeometry(QtCore.QRect(208, 21, 33, 30))
		self.sbVoices.setMinimum(1)
		self.sbVoices.setMaximum(32)
		self.sbVoices.setObjectName(_fromUtf8("sbVoices"))
		self.label_6 = QtGui.QLabel(Dialog)
		self.label_6.setGeometry(QtCore.QRect(145, 21, 29, 30))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.label_7 = QtGui.QLabel(Dialog)
		self.label_7.setGeometry(QtCore.QRect(270, 21, 53, 30))
		self.label_7.setObjectName(_fromUtf8("label_7"))
		self.sbBanks = QtGui.QSpinBox(Dialog)
		self.sbBanks.setGeometry(QtCore.QRect(333, 21, 33, 30))
		self.sbBanks.setMinimum(1)
		self.sbBanks.setMaximum(64)
		self.sbBanks.setObjectName(_fromUtf8("sbBanks"))


		outp= mido.get_output_names()
		inp = mido.get_input_names()

		for i in inp:
			self.cbInputs.addItem(i)
			self.cbClock.addItem(i)
		
		self.cbOutput1.addItem("None")
		self.cbOutput2.addItem("None")
		self.cbOutput3.addItem("None")
		self.cbOutput4.addItem("None")
		self.cbSync1.addItem("None")
		self.cbSync2.addItem("None")
		self.cbSync3.addItem("None")
		self.cbSync4.addItem("None")
		
		for i in outp:			
			self.cbOutput1.addItem(i)
			self.cbOutput2.addItem(i)
			self.cbOutput3.addItem(i)
			self.cbOutput4.addItem(i)
			self.cbSync1.addItem(i)
			self.cbSync2.addItem(i)
			self.cbSync3.addItem(i)
			self.cbSync4.addItem(i)
			
		self.retranslateUi(Dialog)
		self.dlg = Dialog
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accepted)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.rejected)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label_3.setText(_translate("Dialog", "Outputs", None))
		self.label_4.setText(_translate("Dialog", "Sync Out", None))
		self.label_5.setText(_translate("Dialog", "MIDI Channel", None))
		self.label_6.setText(_translate("Dialog", "Voices", None))
		self.label_7.setText(_translate("Dialog", "Step Banks", None))
		self.label.setText(_translate("Dialog", "Input", None))
		self.label_2.setText(_translate("Dialog", "Clock", None))


	def accepted(self):
		midi.MIDI_Close()
		
		key = mido.open_input(self.cbInputs.currentText())
		if(self.cbInputs.currentText() == self.cbClock.currentText()):
			clk = key
		else:
			clk  = mido.open_input(self.cbClock.currentText())
		
		out1 = None
		out2 = None
		out3 = None
		out4 = None
		if(self.cbOutput1.currentText() != "None"):
			out1 = mido.open_output(self.cbOutput1.currentText())
		if(self.cbOutput2.currentText() != "None"):
			out2 = mido.open_output(self.cbOutput2.currentText())
		if(self.cbOutput3.currentText() != "None"):
			out3 = mido.open_output(self.cbOutput3.currentText())
		if(self.cbOutput4.currentText() != "None"):
			out4 = mido.open_output(self.cbOutput3.currentText())
		
		x = []
		if(not out1 is None): x.append(out1)
		if(not out2 is None): x.append(out2)
		if(not out3 is None): x.append(out3)
		if(not out4 is None): x.append(out4)
		
		if(len(x) == 0): 
			print "You must select a MIDI output"
			quit()
		
		out  = MultiPort(x)		
		
		sync1 = None
		sync2 = None
		sync3 = None
		sync4 = None
		if(self.cbSync1.currentText() != "None"):
			sync1 = mido.open_output(self.cbSync1.currentText())
		if(self.cbSync2.currentText() != "None"):
			sync2 = mido.open_output(self.cbSync2.currentText())
		if(self.cbSync3.currentText() != "None"):
			sync3 = mido.open_output(self.cbSync3.currentText())
		if(self.cbSync4.currentText() != "None"):
			sync4 = mido.open_output(self.cbSync4.currentText())
		
			
		syncs = []
		if(not sync1 is None): syncs.append(sync1)
		if(not sync2 is None): syncs.append(sync2)
		if(not sync3 is None): syncs.append(sync3)
		if(not sync4 is None): syncs.append(sync4)
		
		midi.MIDI_SetInOut(key,clk,out)
		if(len(syncs) > 0):
			midi.MIDI_SetSyncPorts(syncs)
		
		channel = self.sbChannel.value()-1
		banks = self.sbBanks.value()
		self.parent.num_banks = banks
		self.parent.input_channel = channel
		self.parent.midi_channel = channel
		self.parent.midi_output = out
		self.parent.num_voices = self.sbVoices.value()
		self.parent.num_banks = banks
		
		self.dlg.close()
		
	def rejected(self):
		self.dlg.close()
		
class Ui_MainWindow(object):

	def __init__(self):
		self.patches = []
		self.names   = []
		self.cur_patch = []
		
	def InitPatches(self):
		files = os.listdir('./Patches')
		os.chdir('./Patches')
		
		for p in files:
			d1 = mopho.OpenFile(p)
			if(len(d1) == 298):
				n = 4
			else:
				n = 6
			
			data1 = mopho.UnpackBits(d1[n:-1])
			self.patches.append(data1)
			x = mopho.GET_NAME(data1)
			name = ''
			for i in range(len(x)):
				name = name + chr(x[i])
			self.names.append(name)
			
		for n in self.names:
			self.cbPattern1.addItem(n)
			self.cbPattern2.addItem(n)
	
		self.cur_patch = self.patches[0][:]

	def Options(self):
		dlg = QtGui.QDialog()
		qdlg = Ui_ConfigDialog()		
		qdlg.setupUi(dlg)
		qdlg.parent = self
		dlg.show()
		dlg.exec_()
					
	def SendCurPatch(self):
		pk = mopho.PackBits(self.cur_patch)
		sysx_hdr = [0xF0,0x01,0x25,0x03]+pk+[0xF7]
		midi.midi_output.send(midi.MSG(sysx_hdr))
		
	def Cross(self):
		print 'cross'
		mut = float(self.leMut1.text())
		if(mut < 0): mut = 0
		if(mut > 1.0): mut=1.0
		mopho.MUT_RATE = mut
		gens = self.sbGens1.value()
		if(gens == 0): gens = randint(1,20)
		splices = self.sbSplices1.value()
		
		data1 = self.patches[self.cbPattern1.currentIndex()]
		data2 = self.patches[self.cbPattern2.currentIndex()]
		
		
		if(splices > 0):
			for i in range(splices):
				n1 = randint(1,len(data1)-1)				
				x   = data1[0:n1] + data2[n1:]
				data1 = x
		data = mopho.realtime_DoGeneration(data1,data2,gens)
			
		self.cur_patch = data
		
		pk = mopho.PackBits(data)
		
		sysx_hdr = [0xF0,0x01,0x25,0x03]
		msg = [0xF0,0x01,0x25,0x3]+pk+ [0xF7]
		midi.midi_output.send(midi.MSG(msg))
	
	def CrossSection(self):
		
		print 'cross section'
		mut = float(self.leMut1.text())
		if(mut < 0): mut = 0
		if(mut > 1.0): mut=1.0
		mopho.MUT_RATE = mut
		gens = self.sbGens1.value()
		if(gens == 0): gens = randint(1,20)
		splices = self.sbSplices1.value()
		
		data1 = self.cur_patch[:]
		data2 = self.patches[self.cbPattern2.currentIndex()][:]
		
		if(splices > 0):
			for i in range(splices):
				n1 = randint(1,len(data1)-1)				
				x   = data1[0:n1] + data2[n1:]
				data1 = x
		x = random()
		if(self.rbOsc1.isChecked()):
			osc1 = mopho.OpOSC1(data1,data2,x)
			mopho.SET_OSC1(self.cur_patch,osc1)
		elif(self.rbOsc2.isChecked()):			
			osc2 = mopho.OpOSC2(data1,data2,x)		
			mopho.SET_OSC2(self.cur_patch,osc2)
		elif(self.rbOscMisc.isChecked()):			
			osc2 = mopho.OpOscMisc(data1,data2,x)		
			mopho.SET_OSCMISC(self.cur_patch,osc2)
		elif(self.rbFilter.isChecked()):
			filt = mopho.OpFilter(data1,data2,x)
			mopho.SET_FILTER(self.cur_patch,filt)
		elif(self.rbVCA.isChecked()):
			vca = mopho.OpVCA(data1,data2,x)
			mopho.SET_VCA(self.cur_patch,vca)
		elif(self.rbEnv3.isChecked()):
			env3 = mopho.OpEnv3(data1,data2,x)	
			mopho.SET_ENV3(self.cur_patch,env3)			
		elif(self.rbMod1.isChecked()):
			mod1 = mopho.OpMOD1(data1,data2,x)
			mopho.SET_MOD1(self.cur_patch,mod1)
		elif(self.rbMod2.isChecked()):			
			mod2 = mopho.OpMOD2(data1,data2,x)
			mopho.SET_MOD2(self.cur_patch,mod2)
		elif(self.rbMod3.isChecked()):
			mod3 = mopho.OpMOD3(data1,data2,x)
			mopho.SET_MOD3(self.cur_patch,mod3)
		elif(self.rbMod4.isChecked()):
			mod4 = mopho.OpMOD4(data1,data2,x)	
			mopho.SET_MOD4(self.cur_patch,mod4)
		elif(self.rbLFO1.isChecked()):
			lfo1 = mopho.OpLFO1(data1,data2,x)
			mopho.SET_LFO1(self.cur_patch,lfo1)
		elif(self.rbLFO2.isChecked()):
			lfo2 = mopho.OpLFO2(data1,data2,x)
			mopho.SET_LFO2(self.cur_patch,lfo2)
		elif(self.rbLFO3.isChecked()):
			lfo3 = mopho.OpLFO3(data1,data2,x)
			mopho.SET_LFO3(self.cur_patch,lfo3)
		elif(self.rbLFO4.isChecked()):
			lfo4 = mopho.OpLFO4(data1,data2,x)
			mopho.SET_LFO4(self.cur_patch,lfo4)
		elif(self.rbClock.isChecked()):
			clock  = mopho.OpClock(data1,data2,x)
			mopho.SET_CLOCK(self.cur_patch,clock)
		elif(self.rbArp.isChecked()):
			arp    = mopho.OpArp(data1,data2,x)
			mopho.SET_ARP(self.cur_patch,arp)
		elif(self.rbModulators.isChecked()):
			modulators = mopho.OpMods(data1,data2,x)
			mopho.SET_MODULATORS(self.cur_patch,modulators)
		elif(self.rbMisc.isChecked()):
			misc = mopho.OpMisc(data1,data2,x)		
			mopho.SET_MISC(self.cur_patch,misc)
		elif(self.rbSEQ1.isChecked()):
			seq1 = mopho.OpSEQ1(data1,data2,x)
			mopho.SET_SEQ1(self.cur_patch,seq1)
		elif(self.rbSEQ2.isChecked()):
			seq2 = mopho.OpSEQ2(data1,data2,x)
			mopho.SET_SEQ2(self.cur_patch,seq2)
		elif(self.rbSEQ3.isChecked()):
			seq3 = mopho.OpSEQ3(data1,data2,x)
			mopho.SET_SEQ3(self.cur_patch,seq3)
		elif(self.rbSEQ4.isChecked()):
			seq4 = mopho.OpSEQ4(data1,data2,x)
			mopho.SET_SEQ4(self.cur_patch,seq4)
			
		name = mopho.OpNAME(data1,data2,x)

		
		
		self.SendCurPatch()
	
	def SetupPatterns(self):
		prob1 = float(self.leProb1.text())
		prob2 = float(self.leProb2.text())
		prob3 = float(self.leProb3.text())
		prob4 = float(self.leProb4.text())
		
		if(prob1 < 0): prob1 = 0
		if(prob1 > 1.0): prob1 = 1.0
		if(prob2 < 0): prob2 = 0
		if(prob2 > 1.0): prob2 = 1.0
		if(prob3 < 0): prob3 = 0
		if(prob3 > 1.0): prob3 = 1.0
		if(prob4 < 0): prob4 = 0
		if(prob4 > 1.0): prob4 = 1.0
		
		oct2 = float(self.leOct2.text())
		oct3 = float(self.leOct3.text())
		oct4 = float(self.leOct4.text())
		oct5 = float(self.leOct5.text())
		
		if(oct2 < 0): oct2 = 0
		if(oct2 > 1.0): oct2 = 1.0
		if(oct3 < 0): oct3 = 0
		if(oct3 > 1.0): oct3 = 1.0
		if(oct4 < 0): oct4 = 0
		if(oct4 > 1.0): oct4 = 1.0
		if(oct5 < 0): oct5 = 0
		if(oct5 > 1.0): oct5 = 1.0
		
		patterns.PROB1 = prob1
		patterns.PROB2 = prob2
		patterns.PROB3 = prob3
		patterns.PROB4 = prob4
		
		patterns.PROB_OCT2 = oct2
		patterns.PROB_OCT3 = oct3
		patterns.PROB_OCT4 = oct4
		patterns.PROB_OCT5 = oct5
		
	def GenSeq1(self):
		self.SetupPatterns()
		alg = self.sbAlg1.value()
		if(alg < 0): alg = -1
		if(alg > 6): alg = -1
		patterns.MUSIC_SetScaleChord(patterns.chord_min,patterns.Scales[self.cbScale1.currentText()])
		seq = patterns.GEN_CreatePattern(alg,16)
		mopho.SET_SEQ1(self.cur_patch,seq)
		self.SendCurPatch()
		
	def GenSeq2(self):
		self.SetupPatterns()
		alg = self.sbAlg2.value()
		if(alg < 0): alg = -1
		if(alg > 6): alg = -1
		
		patterns.MUSIC_SetScaleChord(patterns.chord_min,patterns.Scales[self.cbScale2.currentText()])
		seq = patterns.GEN_CreatePattern(alg,16)		
		mopho.SET_SEQ2(self.cur_patch,seq)
		self.SendCurPatch()
		
	def GenSeq3(self):
		self.SetupPatterns()
		alg = self.sbAlg1.value()
		if(alg < 0): alg = -1
		if(alg > 6): alg = -1
		
		patterns.MUSIC_SetScaleChord(patterns.chord_min,patterns.Scales[self.cbScale3.currentText()])
		seq = patterns.GEN_CreatePattern(alg,16)
		mopho.SET_SEQ3(self.cur_patch,seq)
		self.SendCurPatch()
	
	def GenSeq4(self):
		self.SetupPatterns()
		alg = self.sbAlg1.value()
		if(alg < 0): alg = -1
		if(alg > 6): alg = -1
		
		patterns.MUSIC_SetScaleChord(patterns.chord_min,,patterns.Scales[self.cbScale4.currentText()]
		seq = patterns.GEN_CreatePattern(alg,16)
		mopho.SET_SEQ4(self.cur_patch,seq)
		self.SendCurPatch()
	
	def QuickSeqSetup(self):
		midi.MOPHO_Sequencer(self.midi_channel)

	def EditOscillators(self):
		dlg = QtGui.QDialog()
		ui   = oscillator.Ui_OscDialog()
		ui.setupUi(dlg)
		ui.UpdateData(self.cur_patch)
		ui.midi_output = self.midi_output
		ui.midi_channel = self.midi_channel		
		dlg.show()
		dlg.exec_()
		
	def Parent1(self):
		self.cur_patch = self.patches[self.comboBox.currentIndex()]
		
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(425, 602)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.cbPattern1 = QtGui.QComboBox(self.centralwidget)
		self.cbPattern1.setGeometry(QtCore.QRect(80, 40, 231, 22))
		self.cbPattern1.setObjectName(_fromUtf8("cbPattern1"))
		self.cbPattern2 = QtGui.QComboBox(self.centralwidget)
		self.cbPattern2.setGeometry(QtCore.QRect(80, 80, 231, 22))
		self.cbPattern2.setObjectName(_fromUtf8("cbPattern2"))
		self.label = QtGui.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(20, 40, 46, 13))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(20, 80, 46, 13))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QtGui.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(320, 20, 81, 16))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.pbCross = QtGui.QPushButton(self.centralwidget)
		self.pbCross.setGeometry(QtCore.QRect(50, 180, 91, 23))
		self.pbCross.setObjectName(_fromUtf8("pbCross"))
		self.pbCrossSection = QtGui.QPushButton(self.centralwidget)
		self.pbCrossSection.setGeometry(QtCore.QRect(50, 210, 91, 23))
		self.pbCrossSection.setObjectName(_fromUtf8("pbCrossSection"))
		self.pbAdd = QtGui.QPushButton(self.centralwidget)
		self.pbAdd.setGeometry(QtCore.QRect(60, 120, 91, 23))
		self.pbAdd.setObjectName(_fromUtf8("pbAdd"))
		self.pbSave = QtGui.QPushButton(self.centralwidget)
		self.pbSave.setGeometry(QtCore.QRect(180, 120, 91, 23))
		self.pbSave.setObjectName(_fromUtf8("pbSave"))
		
		self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_5.setGeometry(QtCore.QRect(30, 280, 71, 23))
		self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
		self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_6.setGeometry(QtCore.QRect(30, 310, 71, 23))
		self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
		self.pushButton_7 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_7.setGeometry(QtCore.QRect(30, 340, 71, 23))
		self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
		self.pushButton_8 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_8.setGeometry(QtCore.QRect(30, 370, 71, 23))
		self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))		
		self.pushButton_9 = QtGui.QPushButton(self.centralwidget)
		self.pushButton_9.setGeometry(QtCore.QRect(30, 400, 71, 23))
		self.pushButton_9.setObjectName(_fromUtf8("pushButton_8"))
		
		
		self.leMut1 = QtGui.QLineEdit(self.centralwidget)
		self.leMut1.setGeometry(QtCore.QRect(160, 180, 41, 20))
		self.leMut1.setObjectName(_fromUtf8("leMut1"))
		self.leMut1.setText("0.01")
		self.label_4 = QtGui.QLabel(self.centralwidget)
		self.label_4.setGeometry(QtCore.QRect(170, 160, 21, 16))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.sbGens1 = QtGui.QSpinBox(self.centralwidget)
		self.sbGens1.setGeometry(QtCore.QRect(210, 180, 42, 21))
		self.sbGens1.setObjectName(_fromUtf8("sbGens1"))
		self.label_5 = QtGui.QLabel(self.centralwidget)
		self.label_5.setGeometry(QtCore.QRect(210, 160, 46, 13))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.label_6 = QtGui.QLabel(self.centralwidget)
		self.label_6.setGeometry(QtCore.QRect(260, 160, 46, 13))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.sbSplices1 = QtGui.QSpinBox(self.centralwidget)
		self.sbSplices1.setGeometry(QtCore.QRect(260, 180, 42, 22))
		self.sbSplices1.setObjectName(_fromUtf8("sbSplices1"))
		self.leMut2 = QtGui.QLineEdit(self.centralwidget)
		self.leMut2.setGeometry(QtCore.QRect(160, 209, 41, 20))
		self.leMut2.setObjectName(_fromUtf8("leMut2"))
		self.leMut2.setText("0.01")
		self.sbSplices2 = QtGui.QSpinBox(self.centralwidget)
		self.sbSplices2.setGeometry(QtCore.QRect(260, 209, 42, 22))
		self.sbSplices2.setObjectName(_fromUtf8("sbSplices2"))
		self.sbGens2 = QtGui.QSpinBox(self.centralwidget)
		self.sbGens2.setGeometry(QtCore.QRect(210, 210, 42, 21))
		self.sbGens2.setObjectName(_fromUtf8("sbGens2"))
		self.label_18 = QtGui.QLabel(self.centralwidget)
		self.label_18.setGeometry(QtCore.QRect(180, 440, 46, 13))
		self.label_18.setObjectName(_fromUtf8("label_18"))
		self.leProb1 = QtGui.QLineEdit(self.centralwidget)
		self.leProb1.setGeometry(QtCore.QRect(100, 440, 51, 20))
		self.leProb1.setObjectName(_fromUtf8("leProb1"))
		self.leOct3 = QtGui.QLineEdit(self.centralwidget)
		self.leOct3.setGeometry(QtCore.QRect(240, 470, 51, 20))
		self.leOct3.setObjectName(_fromUtf8("leOct3"))
		self.label_15 = QtGui.QLabel(self.centralwidget)
		self.label_15.setGeometry(QtCore.QRect(40, 530, 46, 13))
		self.label_15.setObjectName(_fromUtf8("label_15"))
		self.leProb4 = QtGui.QLineEdit(self.centralwidget)
		self.leProb4.setGeometry(QtCore.QRect(100, 530, 51, 20))
		self.leProb4.setObjectName(_fromUtf8("leProb4"))
		self.leOct2 = QtGui.QLineEdit(self.centralwidget)
		self.leOct2.setGeometry(QtCore.QRect(240, 440, 51, 21))
		self.leOct2.setObjectName(_fromUtf8("leOct2"))
		self.leProb2 = QtGui.QLineEdit(self.centralwidget)
		self.leProb2.setGeometry(QtCore.QRect(100, 470, 51, 20))
		self.leProb2.setObjectName(_fromUtf8("leProb2"))
		self.label_14 = QtGui.QLabel(self.centralwidget)
		self.label_14.setGeometry(QtCore.QRect(40, 500, 46, 13))
		self.label_14.setObjectName(_fromUtf8("label_14"))
		self.label_16 = QtGui.QLabel(self.centralwidget)
		self.label_16.setGeometry(QtCore.QRect(180, 530, 46, 13))
		self.label_16.setObjectName(_fromUtf8("label_16"))
		self.label_17 = QtGui.QLabel(self.centralwidget)
		self.label_17.setGeometry(QtCore.QRect(180, 500, 46, 13))
		self.label_17.setObjectName(_fromUtf8("label_17"))
		self.label_19 = QtGui.QLabel(self.centralwidget)
		self.label_19.setGeometry(QtCore.QRect(180, 470, 46, 13))
		self.label_19.setObjectName(_fromUtf8("label_19"))
		self.leProb3 = QtGui.QLineEdit(self.centralwidget)
		self.leProb3.setGeometry(QtCore.QRect(100, 500, 51, 20))
		self.leProb3.setObjectName(_fromUtf8("leProb3"))
		self.leOct5 = QtGui.QLineEdit(self.centralwidget)
		self.leOct5.setGeometry(QtCore.QRect(240, 530, 51, 20))
		self.leOct5.setObjectName(_fromUtf8("leOct5"))
		self.label_9 = QtGui.QLabel(self.centralwidget)
		self.label_9.setGeometry(QtCore.QRect(40, 440, 46, 13))
		self.label_9.setObjectName(_fromUtf8("label_9"))
		self.label_10 = QtGui.QLabel(self.centralwidget)
		self.label_10.setGeometry(QtCore.QRect(40, 470, 46, 13))
		self.label_10.setObjectName(_fromUtf8("label_10"))
		self.leOct4 = QtGui.QLineEdit(self.centralwidget)
		self.leOct4.setGeometry(QtCore.QRect(240, 500, 51, 20))
		self.leOct4.setObjectName(_fromUtf8("leOct4"))
		self.sbAlg1 = QtGui.QSpinBox(self.centralwidget)
		self.sbAlg1.setGeometry(QtCore.QRect(110, 280, 42, 22))
		self.sbAlg1.setObjectName(_fromUtf8("sbAlg1"))
		
		self.cbScale1 = QtGui.QComboBox(self.centralwidget)
		self.cbScale1.setGeometry(QtCore.QRect(150, 280, 119, 22))
		self.cbScale1.setObjectName(_fromUtf8("cbScale1"))
		
		self.cbScale2 = QtGui.QComboBox(self.centralwidget)
		self.cbScale2.setGeometry(QtCore.QRect(150, 310, 119, 22))
		self.cbScale2.setObjectName(_fromUtf8("cbScale2"))
		
		self.sbAlg2 = QtGui.QSpinBox(self.centralwidget)
		self.sbAlg2.setGeometry(QtCore.QRect(110, 310, 42, 22))
		self.sbAlg2.setObjectName(_fromUtf8("sbAlg2"))
		self.cbScale3 = QtGui.QComboBox(self.centralwidget)
		self.cbScale3.setGeometry(QtCore.QRect(150, 340, 119, 22))
		self.cbScale3.setObjectName(_fromUtf8("cbScale3"))
		self.sbAlg3 = QtGui.QSpinBox(self.centralwidget)
		self.sbAlg3.setGeometry(QtCore.QRect(110, 340, 42, 22))
		self.sbAlg3.setObjectName(_fromUtf8("sbAlg3"))
		
		self.cbScale4 = QtGui.QComboBox(self.centralwidget)
		self.cbScale4.setGeometry(QtCore.QRect(150, 370, 119, 22))
		self.cbScale4.setObjectName(_fromUtf8("cbScale4"))
		self.sbAlg4 = QtGui.QSpinBox(self.centralwidget)
		self.sbAlg4.setGeometry(QtCore.QRect(110, 370, 42, 22))
		self.sbAlg4.setObjectName(_fromUtf8("sbAlg4"))
		
		self.widget = QtGui.QWidget(self.centralwidget)
		self.widget.setGeometry(QtCore.QRect(320, 40, 84, 502))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.widget)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.rbOsc1 = QtGui.QRadioButton(self.widget)
		self.rbOsc1.setChecked(True)
		self.rbOsc1.setObjectName(_fromUtf8("rbOsc1"))
		self.verticalLayout.addWidget(self.rbOsc1)
		self.rbOsc2 = QtGui.QRadioButton(self.widget)
		self.rbOsc2.setObjectName(_fromUtf8("rbOsc2"))
		self.verticalLayout.addWidget(self.rbOsc2)
		self.rbOscMisc = QtGui.QRadioButton(self.widget)
		self.rbOscMisc.setObjectName(_fromUtf8("rbOscMisc"))
		self.verticalLayout.addWidget(self.rbOscMisc)
		self.rbFilter = QtGui.QRadioButton(self.widget)
		self.rbFilter.setObjectName(_fromUtf8("rbFilter"))
		self.verticalLayout.addWidget(self.rbFilter)
		self.rbVCA = QtGui.QRadioButton(self.widget)
		self.rbVCA.setObjectName(_fromUtf8("rbVCA"))
		self.verticalLayout.addWidget(self.rbVCA)
		self.rbEnv3 = QtGui.QRadioButton(self.widget)
		self.rbEnv3.setObjectName(_fromUtf8("rbEnv3"))
		self.verticalLayout.addWidget(self.rbEnv3)
		self.rbMod1 = QtGui.QRadioButton(self.widget)
		self.rbMod1.setObjectName(_fromUtf8("rbMod1"))
		self.verticalLayout.addWidget(self.rbMod1)
		self.rbMod2 = QtGui.QRadioButton(self.widget)
		self.rbMod2.setObjectName(_fromUtf8("rbMod2"))
		self.verticalLayout.addWidget(self.rbMod2)
		self.rbMod3 = QtGui.QRadioButton(self.widget)
		self.rbMod3.setObjectName(_fromUtf8("rbMod3"))
		self.verticalLayout.addWidget(self.rbMod3)
		self.rbMod4 = QtGui.QRadioButton(self.widget)
		self.rbMod4.setObjectName(_fromUtf8("rbMod4"))
		self.verticalLayout.addWidget(self.rbMod4)
		self.rbLFO1 = QtGui.QRadioButton(self.widget)
		self.rbLFO1.setObjectName(_fromUtf8("rbLFO1"))
		self.verticalLayout.addWidget(self.rbLFO1)
		self.rbLFO2 = QtGui.QRadioButton(self.widget)
		self.rbLFO2.setObjectName(_fromUtf8("rbLFO2"))
		self.verticalLayout.addWidget(self.rbLFO2)
		self.rbLFO3 = QtGui.QRadioButton(self.widget)
		self.rbLFO3.setObjectName(_fromUtf8("rbLFO3"))
		self.verticalLayout.addWidget(self.rbLFO3)
		self.rbLFO4 = QtGui.QRadioButton(self.widget)
		self.rbLFO4.setObjectName(_fromUtf8("rbLFO4"))
		self.verticalLayout.addWidget(self.rbLFO4)
		self.rbClock = QtGui.QRadioButton(self.widget)
		self.rbClock.setObjectName(_fromUtf8("rbClock"))
		self.verticalLayout.addWidget(self.rbClock)
		self.rbArp = QtGui.QRadioButton(self.widget)
		self.rbArp.setObjectName(_fromUtf8("rbArp"))
		self.verticalLayout.addWidget(self.rbArp)
		self.rbModulators = QtGui.QRadioButton(self.widget)
		self.rbModulators.setObjectName(_fromUtf8("rbModulators"))
		self.verticalLayout.addWidget(self.rbModulators)
		self.rbMisc = QtGui.QRadioButton(self.widget)
		self.rbMisc.setObjectName(_fromUtf8("rbMisc"))
		self.verticalLayout.addWidget(self.rbMisc)
		self.rbSeq1 = QtGui.QRadioButton(self.widget)
		self.rbSeq1.setObjectName(_fromUtf8("rbSeq1"))
		self.verticalLayout.addWidget(self.rbSeq1)
		self.rbSeq2 = QtGui.QRadioButton(self.widget)
		self.rbSeq2.setObjectName(_fromUtf8("rbSeq2"))
		self.verticalLayout.addWidget(self.rbSeq2)
		self.rbSeq3 = QtGui.QRadioButton(self.widget)
		self.rbSeq3.setObjectName(_fromUtf8("rbSeq3"))
		self.verticalLayout.addWidget(self.rbSeq3)
		self.rbSeq4 = QtGui.QRadioButton(self.widget)
		self.rbSeq4.setObjectName(_fromUtf8("rbSeq4"))
		self.verticalLayout.addWidget(self.rbSeq4)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 425, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		self.menuEditor = QtGui.QMenu(self.menubar)
		self.menuEditor.setObjectName(_fromUtf8("menuEditor"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionSave = QtGui.QAction(MainWindow)
		self.actionSave.setObjectName(_fromUtf8("actionSave"))
		self.actionExit = QtGui.QAction(MainWindow)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionOscillators = QtGui.QAction(MainWindow)
		self.actionOscillators.setObjectName(_fromUtf8("actionOscillators"))
		self.actionFilter = QtGui.QAction(MainWindow)
		self.actionFilter.setObjectName(_fromUtf8("actionFilter"))
		self.actionVCA = QtGui.QAction(MainWindow)
		self.actionVCA.setObjectName(_fromUtf8("actionVCA"))
		self.actionLFO1 = QtGui.QAction(MainWindow)
		self.actionLFO1.setObjectName(_fromUtf8("actionLFO1"))
		self.actionLFO2 = QtGui.QAction(MainWindow)
		self.actionLFO2.setObjectName(_fromUtf8("actionLFO2"))
		self.actionLFO3 = QtGui.QAction(MainWindow)
		self.actionLFO3.setObjectName(_fromUtf8("actionLFO3"))
		self.actionLFO4 = QtGui.QAction(MainWindow)
		self.actionLFO4.setObjectName(_fromUtf8("actionLFO4"))
		self.actionMOD1 = QtGui.QAction(MainWindow)
		self.actionMOD1.setObjectName(_fromUtf8("actionMOD1"))
		self.actionMOD2 = QtGui.QAction(MainWindow)
		self.actionMOD2.setObjectName(_fromUtf8("actionMOD2"))
		self.actionMOD3 = QtGui.QAction(MainWindow)
		self.actionMOD3.setObjectName(_fromUtf8("actionMOD3"))
		self.actionMOD4 = QtGui.QAction(MainWindow)
		self.actionMOD4.setObjectName(_fromUtf8("actionMOD4"))
		self.actionARP = QtGui.QAction(MainWindow)
		self.actionARP.setObjectName(_fromUtf8("actionARP"))

		self.actionOptions = QtGui.QAction(MainWindow)
		self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
		
		
		self.menuFile.addAction(self.actionSave)
		self.menuFile.addAction(self.actionOptions)
		
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionExit)
		self.menuEditor.addAction(self.actionOscillators)
		self.menuEditor.addAction(self.actionFilter)
		self.menuEditor.addAction(self.actionVCA)
		self.menuEditor.addAction(self.actionLFO1)
		self.menuEditor.addAction(self.actionLFO2)
		self.menuEditor.addAction(self.actionLFO3)
		self.menuEditor.addAction(self.actionLFO4)
		self.menuEditor.addAction(self.actionMOD1)
		self.menuEditor.addAction(self.actionMOD2)
		self.menuEditor.addAction(self.actionMOD3)
		self.menuEditor.addAction(self.actionMOD4)
		self.menuEditor.addAction(self.actionARP)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuEditor.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.InitPatches()
		self.pbCross.clicked.connect(self.Cross)
		self.pbCrossSection.clicked.connect(self.CrossSection)
		self.actionOptions.triggered.connect(self.Options)
		
		for key,item in patterns.Scales.items():
			self.cbScale1.addItem(key)
			self.cbScale2.addItem(key)
			self.cbScale3.addItem(key)
			self.cbScale4.addItem(key)
			
		self.pushButton_5.clicked.connect(self.GenSeq1)
		self.pushButton_6.clicked.connect(self.GenSeq2)
		self.pushButton_7.clicked.connect(self.GenSeq3)
		self.pushButton_8.clicked.connect(self.GenSeq4)
		self.pushButton_9.clicked.connect(self.QuickSeqSetup)
		
		
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.label.setText(_translate("MainWindow", "Pattern 1", None))
		self.label_2.setText(_translate("MainWindow", "Pattern 2", None))
		self.label_3.setText(_translate("MainWindow", "Cross Section", None))
		self.pbCross.setText(_translate("MainWindow", "Cross Pattern", None))
		self.pbCrossSection.setText(_translate("MainWindow", "Cross Section", None))
		self.pbAdd.setText(_translate("MainWindow", "Add to Pool", None))
		self.pbSave.setText(_translate("MainWindow", "Save Current", None))
		self.pushButton_5.setText(_translate("MainWindow", "GenSEQ1", None))
		self.pushButton_6.setText(_translate("MainWindow", "GenSEQ2", None))
		self.pushButton_7.setText(_translate("MainWindow", "GenSEQ3", None))
		self.pushButton_8.setText(_translate("MainWindow", "GenSEQ4", None))
		self.pushButton_9.setText(_translate("MainWindow", "Setup", None))
		self.label_4.setText(_translate("MainWindow", "Mu", None))
		self.label_5.setText(_translate("MainWindow", "Gens", None))
		self.label_6.setText(_translate("MainWindow", "Splices", None))
		self.label_18.setText(_translate("MainWindow", "OCT2", None))
		self.leProb1.setText(_translate("MainWindow", "0.0", None))
		self.leOct3.setText(_translate("MainWindow", "0", None))
		self.label_15.setText(_translate("MainWindow", "PROB4", None))
		self.leProb4.setText(_translate("MainWindow", "0.0", None))
		self.leOct2.setText(_translate("MainWindow", "0", None))
		self.leProb2.setText(_translate("MainWindow", "0.0", None))
		self.label_14.setText(_translate("MainWindow", "PROB3", None))
		self.label_16.setText(_translate("MainWindow", "OCT5", None))
		self.label_17.setText(_translate("MainWindow", "OCT4", None))
		self.label_19.setText(_translate("MainWindow", "OCT3", None))
		self.leProb3.setText(_translate("MainWindow", "0.0", None))
		self.leOct5.setText(_translate("MainWindow", "0", None))
		self.label_9.setText(_translate("MainWindow", "PROB1", None))
		self.label_10.setText(_translate("MainWindow", "PROB2", None))
		self.leOct4.setText(_translate("MainWindow", "0", None))
		self.rbOsc1.setText(_translate("MainWindow", "Osc1", None))
		self.rbOsc2.setText(_translate("MainWindow", "Osc2", None))
		self.rbOscMisc.setText(_translate("MainWindow", "OscMISC", None))
		self.rbFilter.setText(_translate("MainWindow", "Filter", None))
		self.rbVCA.setText(_translate("MainWindow", "VCA", None))
		self.rbEnv3.setText(_translate("MainWindow", "Env3", None))
		self.rbMod1.setText(_translate("MainWindow", "Mod1", None))
		self.rbMod2.setText(_translate("MainWindow", "Mod2", None))
		self.rbMod3.setText(_translate("MainWindow", "Mod3", None))
		self.rbMod4.setText(_translate("MainWindow", "Mod4", None))
		self.rbLFO1.setText(_translate("MainWindow", "LFO1", None))
		self.rbLFO2.setText(_translate("MainWindow", "LFO2", None))
		self.rbLFO3.setText(_translate("MainWindow", "LFO3", None))
		self.rbLFO4.setText(_translate("MainWindow", "LFO4", None))
		self.rbClock.setText(_translate("MainWindow", "Clock", None))
		self.rbArp.setText(_translate("MainWindow", "Arp", None))
		self.rbModulators.setText(_translate("MainWindow", "Modulators", None))
		self.rbMisc.setText(_translate("MainWindow", "Misc", None))
		self.rbSeq1.setText(_translate("MainWindow", "Seq1", None))
		self.rbSeq2.setText(_translate("MainWindow", "Seq2", None))
		self.rbSeq3.setText(_translate("MainWindow", "Seq3", None))
		self.rbSeq4.setText(_translate("MainWindow", "Seq4", None))
		self.menuFile.setTitle(_translate("MainWindow", "File", None))
		self.menuEditor.setTitle(_translate("MainWindow", "Editor", None))
		self.actionSave.setText(_translate("MainWindow", "Save", None))
		self.actionOptions.setText(_translate("MainWindow", "Options", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionOscillators.setText(_translate("MainWindow", "OSC", None))
		self.actionFilter.setText(_translate("MainWindow", "Filter", None))
		self.actionVCA.setText(_translate("MainWindow", "VCA", None))
		self.actionLFO1.setText(_translate("MainWindow", "LFO1", None))
		self.actionLFO2.setText(_translate("MainWindow", "LFO2", None))
		self.actionLFO3.setText(_translate("MainWindow", "LFO3", None))
		self.actionLFO4.setText(_translate("MainWindow", "LFO4", None))
		self.actionMOD1.setText(_translate("MainWindow", "MOD1", None))
		self.actionMOD2.setText(_translate("MainWindow", "MOD2", None))
		self.actionMOD3.setText(_translate("MainWindow", "MOD3", None))
		self.actionMOD4.setText(_translate("MainWindow", "MOD4", None))
		self.actionARP.setText(_translate("MainWindow", "ARP", None))

def run(app):
	sys.exit(app.exec_())
	MIDI_Shutdown()
	
	
if __name__ == '__main__':
	
	app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
	app.setStyleSheet("""
		QMenuBar {
			background-color: rgb(93,93,93);
		}

		QMenuBar::item {
			background: rgb(93,93,93);
		}
		""")
	window = QtGui.QMainWindow()
	
	ui = Ui_MainWindow()
	ui.setupUi(window)
	window.show()
	run(app)
	