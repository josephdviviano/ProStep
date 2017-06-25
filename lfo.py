# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lfo.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from midi import *
from mopho import *
import math
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

class Ui_LFODialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(335, 260)
		
		self.lfoFreq = QtGui.QDial(Dialog)
		self.lfoFreq.setGeometry(QtCore.QRect(10, 20, 50, 64))
		self.lfoFreq.setMaximum(1024)
		self.lfoFreq.setObjectName(_fromUtf8("lfoFreq"))
		self.lfoFreq.valueChanged.connect(self.LfoFreq)
		
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(30, 80, 46, 13))
		self.label.setObjectName(_fromUtf8("label"))
		self.groupBox = QtGui.QGroupBox(Dialog)
		self.groupBox.setGeometry(QtCore.QRect(80, 20, 111, 211))
		self.groupBox.setObjectName(_fromUtf8("groupBox"))
		
		self.lfo32 = QtGui.QRadioButton(self.groupBox)
		self.lfo32.setGeometry(QtCore.QRect(10, 20, 82, 17))
		self.lfo32.setObjectName(_fromUtf8("lfo32"))
		self.lfo32.toggled.connect(self.LfoStep)
		
		self.lfo16 = QtGui.QRadioButton(self.groupBox)
		self.lfo16.setGeometry(QtCore.QRect(10, 40, 82, 17))
		self.lfo16.setObjectName(_fromUtf8("lfo16"))
		self.lfo16.toggled.connect(self.LfoStep)
		
		self.lfo8 = QtGui.QRadioButton(self.groupBox)
		self.lfo8.setGeometry(QtCore.QRect(10, 60, 82, 17))
		self.lfo8.setObjectName(_fromUtf8("lfo8"))
		self.lfo8.toggled.connect(self.LfoStep)
		
		self.lfo6 = QtGui.QRadioButton(self.groupBox)
		self.lfo6.setGeometry(QtCore.QRect(10, 80, 82, 17))
		self.lfo6.setObjectName(_fromUtf8("lfo6"))
		self.lfo6.toggled.connect(self.LfoStep)
		
		self.lfo4 = QtGui.QRadioButton(self.groupBox)
		self.lfo4.setGeometry(QtCore.QRect(10, 100, 82, 17))
		self.lfo4.setObjectName(_fromUtf8("lfo4"))
		self.lfo4.toggled.connect(self.LfoStep)
		
		self.lfo3 = QtGui.QRadioButton(self.groupBox)
		self.lfo3.setGeometry(QtCore.QRect(10, 120, 82, 17))
		self.lfo3.setObjectName(_fromUtf8("lfo3"))
		self.lfo3.toggled.connect(self.LfoStep)
		
		self.lfo2 = QtGui.QRadioButton(self.groupBox)
		self.lfo2.setGeometry(QtCore.QRect(10, 140, 82, 17))
		self.lfo2.setObjectName(_fromUtf8("lfo2"))
		self.lfo2.toggled.connect(self.LfoStep)
		
		self.lfo1 = QtGui.QRadioButton(self.groupBox)
		self.lfo1.setGeometry(QtCore.QRect(10, 160, 82, 17))
		self.lfo1.setObjectName(_fromUtf8("lfo1"))
		self.lfo1.toggled.connect(self.LfoStep)
		
		self.lfo0 = QtGui.QRadioButton(self.groupBox)
		self.lfo0.setGeometry(QtCore.QRect(10, 180, 82, 17))
		self.lfo0.setChecked(True)
		self.lfo0.setObjectName(_fromUtf8("lfo0"))
		self.lfo0.toggled.connect(self.LfoStep)
		
		self.lfoAmt = QtGui.QDial(Dialog)
		self.lfoAmt.setGeometry(QtCore.QRect(10, 100, 50, 64))
		self.lfoAmt.setMaximum(1024)
		self.lfoAmt.setObjectName(_fromUtf8("lfoAmt"))
		self.lfoAmt.valueChanged.connect(self.LfoAmt)
		
		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(30, 170, 21, 16))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.lfoModDest = QtGui.QComboBox(Dialog)
		self.lfoModDest.setGeometry(QtCore.QRect(200, 30, 121, 22))
		self.lfoModDest.setObjectName(_fromUtf8("lfoModDest"))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.addItem(_fromUtf8(""))
		self.lfoModDest.setItemText(48, _fromUtf8(""))
		self.lfoModDest.currentIndexChanged.connect(self.LfoModDest)
		self.label_3 = QtGui.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(200, 10, 46, 13))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.lfoKeySync = QtGui.QCheckBox(Dialog)
		self.lfoKeySync.setGeometry(QtCore.QRect(260, 10, 70, 17))
		self.lfoKeySync.setObjectName(_fromUtf8("lfoKeySync"))
		self.lfoKeySync.toggled.connect(self.LfoKeySync)
		
		self.groupBox_2 = QtGui.QGroupBox(Dialog)
		self.groupBox_2.setGeometry(QtCore.QRect(190, 60, 121, 131))
		self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
		
		self.lfoTri = QtGui.QRadioButton(self.groupBox_2)
		self.lfoTri.setGeometry(QtCore.QRect(10, 20, 82, 17))
		self.lfoTri.setChecked(True)
		self.lfoTri.setObjectName(_fromUtf8("lfoTri"))
		self.lfoTri.toggled.connect(self.LfoWave)
		
		self.lfoRevSaw = QtGui.QRadioButton(self.groupBox_2)
		self.lfoRevSaw.setGeometry(QtCore.QRect(10, 40, 82, 17))
		self.lfoRevSaw.setObjectName(_fromUtf8("lfoRevSaw"))
		self.lfoRevSaw.toggled.connect(self.LfoWave)
		
		self.lfoSaw = QtGui.QRadioButton(self.groupBox_2)
		self.lfoSaw.setGeometry(QtCore.QRect(10, 60, 82, 17))
		self.lfoSaw.setObjectName(_fromUtf8("lfoSaw"))
		self.lfoSaw.toggled.connect(self.LfoWave)
		
		self.lfoPulse = QtGui.QRadioButton(self.groupBox_2)
		self.lfoPulse.setGeometry(QtCore.QRect(10, 80, 82, 17))
		self.lfoPulse.setObjectName(_fromUtf8("lfoPulse"))
		self.lfoPulse.toggled.connect(self.LfoWave)
		
		self.lfoRandom = QtGui.QRadioButton(self.groupBox_2)
		self.lfoRandom.setGeometry(QtCore.QRect(10, 100, 82, 17))
		self.lfoRandom.setObjectName(_fromUtf8("lfoRandom"))
		self.lfoRandom.toggled.connect(self.LfoWave)
			
		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label.setText(_translate("Dialog", "Freq", None))
		self.groupBox.setTitle(_translate("Dialog", "Frequency Selection", None))
		self.lfo32.setText(_translate("Dialog", "32 Step", None))
		self.lfo16.setText(_translate("Dialog", "16 step", None))
		self.lfo8.setText(_translate("Dialog", "8 Step", None))
		self.lfo6.setText(_translate("Dialog", "6 Step", None))
		self.lfo4.setText(_translate("Dialog", "4 Step", None))
		self.lfo3.setText(_translate("Dialog", "3 Step", None))
		self.lfo2.setText(_translate("Dialog", "2 Step", None))
		self.lfo1.setText(_translate("Dialog", "1.5 Step", None))
		self.lfo0.setText(_translate("Dialog", "Freq", None))
		self.label_2.setText(_translate("Dialog", "Amt", None))
		self.lfoModDest.setItemText(0, _translate("Dialog", "Off", None))
		self.lfoModDest.setItemText(1, _translate("Dialog", "Osc 1 Freq", None))
		self.lfoModDest.setItemText(2, _translate("Dialog", "Osc 2 Freq", None))
		self.lfoModDest.setItemText(3, _translate("Dialog", "Osc 1+2 Freq", None))
		self.lfoModDest.setItemText(4, _translate("Dialog", "Osc Mix", None))
		self.lfoModDest.setItemText(5, _translate("Dialog", "Noise Level", None))
		self.lfoModDest.setItemText(6, _translate("Dialog", "Osc 1 PW", None))
		self.lfoModDest.setItemText(7, _translate("Dialog", "Osc 2 PW", None))
		self.lfoModDest.setItemText(8, _translate("Dialog", "Osc 1+2 PW", None))
		self.lfoModDest.setItemText(9, _translate("Dialog", "Filter Freq", None))
		self.lfoModDest.setItemText(10, _translate("Dialog", "Resonance", None))
		self.lfoModDest.setItemText(11, _translate("Dialog", "Filter Audio Mod", None))
		self.lfoModDest.setItemText(12, _translate("Dialog", "VCA Level", None))
		self.lfoModDest.setItemText(13, _translate("Dialog", "Pan", None))
		self.lfoModDest.setItemText(14, _translate("Dialog", "LFO 1 Freq", None))
		self.lfoModDest.setItemText(15, _translate("Dialog", "LFO2 Freq", None))
		self.lfoModDest.setItemText(16, _translate("Dialog", "LFO3 Freq", None))
		self.lfoModDest.setItemText(17, _translate("Dialog", "LFO4 Freq", None))
		self.lfoModDest.setItemText(18, _translate("Dialog", "All LFO Freq", None))
		self.lfoModDest.setItemText(19, _translate("Dialog", "LFO1 Amt", None))
		self.lfoModDest.setItemText(20, _translate("Dialog", "LFO2 Amt", None))
		self.lfoModDest.setItemText(21, _translate("Dialog", "LFO3 Amt", None))
		self.lfoModDest.setItemText(22, _translate("Dialog", "LFO4 Amt", None))
		self.lfoModDest.setItemText(23, _translate("Dialog", "All LFO Amt", None))
		self.lfoModDest.setItemText(24, _translate("Dialog", "Filter Env Amt", None))
		self.lfoModDest.setItemText(25, _translate("Dialog", "Amp Env Amt", None))
		self.lfoModDest.setItemText(26, _translate("Dialog", "Env 3 Amt", None))
		self.lfoModDest.setItemText(27, _translate("Dialog", "All Env Amt", None))
		self.lfoModDest.setItemText(28, _translate("Dialog", "Env1 Attak", None))
		self.lfoModDest.setItemText(29, _translate("Dialog", "Env2 Attack", None))
		self.lfoModDest.setItemText(30, _translate("Dialog", "Env3 Attack", None))
		self.lfoModDest.setItemText(31, _translate("Dialog", "All Env Attacks", None))
		self.lfoModDest.setItemText(32, _translate("Dialog", "Env1 Decay", None))
		self.lfoModDest.setItemText(33, _translate("Dialog", "Env2 Decay", None))
		self.lfoModDest.setItemText(34, _translate("Dialog", "Env3 Decay", None))
		self.lfoModDest.setItemText(35, _translate("Dialog", "All Env Decays", None))
		self.lfoModDest.setItemText(36, _translate("Dialog", "Env1 Release", None))
		self.lfoModDest.setItemText(37, _translate("Dialog", "Env2 Release", None))
		self.lfoModDest.setItemText(38, _translate("Dialog", "Env3 Release", None))
		self.lfoModDest.setItemText(39, _translate("Dialog", "All Env Releases", None))
		self.lfoModDest.setItemText(40, _translate("Dialog", "Mod1 Amt", None))
		self.lfoModDest.setItemText(41, _translate("Dialog", "Mod2 Amt", None))
		self.lfoModDest.setItemText(42, _translate("Dialog", "Mod3 Amt", None))
		self.lfoModDest.setItemText(43, _translate("Dialog", "Mod4 Amt", None))
		self.lfoModDest.setItemText(44, _translate("Dialog", "Ext Audio In Level", None))
		self.lfoModDest.setItemText(45, _translate("Dialog", "Sub Osc1", None))
		self.lfoModDest.setItemText(46, _translate("Dialog", "Sub Osc 2", None))
		self.lfoModDest.setItemText(47, _translate("Dialog", "Skew 1/2", None))
		self.label_3.setText(_translate("Dialog", "Mod Dest", None))
		self.lfoKeySync.setText(_translate("Dialog", "Key Sync", None))
		self.groupBox_2.setTitle(_translate("Dialog", "LFO Waveform", None))
		self.lfoTri.setText(_translate("Dialog", "Triangle", None))
		self.lfoRevSaw.setText(_translate("Dialog", "Reverse Saw", None))
		self.lfoSaw.setText(_translate("Dialog", "Sawtooth", None))
		self.lfoPulse.setText(_translate("Dialog", "Pulse(Square)", None))
		self.lfoRandom.setText(_translate("Dialog", "Random", None))

	def LfoFreq(self,value):
		x = int(math.ceil(value/1024.0 * 164.0))
		if(self.lfo_num == 1):
			nrpn = 37
		elif(self.lfo_num == 2):
			nrpn = 42
		elif(self.lfo_num == 3):
			nrpn = 47
		else:
			nrpn = 52
			
		SendNRPN(nrpn,x,self.midi_channel)
	
	def LfoStep(self,value):
		
		if(self.lfo32.isChecked()):
			x = 151
		elif(self.lfo16.isChecked()):
			x = 152		
		elif(self.lfo8.isChecked()):
			x = 153
		elif(self.lfo6.isChecked()):
			x = 154		
		elif(self.lfo4.isChecked()):
			x = 155
		elif(self.lfo3.isChecked()):
			x = 156
		elif(self.lfo2.isChecked()):
			x = 157
		elif(self.lfo1.isChecked()):
			x = 158
		
		if(self.lfo_num == 1):
			nrpn = 37
		elif(self.lfo_num == 2):
			nrpn = 42
		elif(self.lfo_num == 3):
			nrpn = 47
		else:
			nrpn = 52
			
		SendNRPN(nrpn,x,self.midi_channel)
	

	def SetWave(self,value):
		if(self.lfo_num == 1):
			nrpn = 38
		elif(self.lfo_num == 2):
			nrpn = 43
		elif(self.lfo_num == 3):
			nrpn = 48
		else:
			nrpn = 53
			
		SendNRPN(nrpn,value,self.midi_channel)
		
	def LfoWave(self):
		if(self.lfoTri.isChecked()):
			self.SetWave(0)		
		elif(self.lfoRevSaw.isChecked()):
			self.SetWave(1)	
		elif(self.lfoSaw.isChecked()):
			self.SetWave(2)
		elif(self.lfoPulse.isChecked()):
			self.SetWave(3)
		elif(self.lfoRandom.isChecked()):
			self.SetWave(4)
	
	def LfoAmt(self,value):
	
		x = int(math.ceil(value/1024.0 * 164.0))
		if(self.lfo_num == 1):
			nrpn = 39
		elif(self.lfo_num == 2):
			nrpn = 44
		elif(self.lfo_num == 3):
			nrpn = 49
		else:
			nrpn = 54
			
		SendNRPN(nrpn,x,self.midi_channel)
	
	def LfoModDest(self,value):
		x = self.lfoModDest.currentIndex()
		if(self.lfo_num == 1):
			nrpn = 40
		elif(self.lfo_num == 2):
			nrpn = 45
		elif(self.lfo_num == 3):
			nrpn = 50
		else:
			nrpn = 55
		SendNRPN(nrpn,x,self.midi_channel)
		
	def LfoKeySync(self,value):
		sync = self.lfoKeySync.isChecked()
		if(self.lfo_num == 1):
			nrpn = 41
		elif(self.lfo_num == 2):
			nrpn = 46
		elif(self.lfo_num == 3):
			nrpn = 51
		else:
			nrpn = 56
		SendNRPN(nrpn,value,self.midi_channel)
		