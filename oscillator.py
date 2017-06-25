# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oscillator.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import midi
import mopho
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

def SendNRPN(nrpn,x,mc):
	midi.SendNRPN(nrpn,x,mc)
	
class Ui_OscDialog(object):

	def UpdateData(self,data):
		osc1 = mopho.GET_Osc1(data)
		osc2 = mopho.GET_Osc2(data)
		oscmisc = mopho.GET_OscMisc(data)
		
		self.osc1freq.setValue(osc1[0])
		self.osc1fine.setValue(osc1[1])
		self.osc1shape.setValue(osc1[2])
		if(osc1[2] == 0):
			self.osc1waveNone.setChecked(True)
		elif(osc1[2] == 1):
			self.osc1WaveSaw.setChecked(True)
		elif(osc1[2] == 2):
			self.osc1WaveTri.setChecked(True)
		elif(osc1[2] == 3):
			self.osc1WaveSawTri.setChecked(True)
		elif(osc1[2] == 4):
			self.osc1WaveSquare.setChecked(True)
		
		self.osc1glide.setValue(osc1[3])
		self.osc1KeyB.setChecked(osc1[4])
		self.osc1Sub.setValue(osc1[5])
		
		self.osc2freq.setValue(osc2[0])
		self.osc2fine.setValue(osc2[1])
		self.osc2shape.setValue(osc2[2])
		if(osc2[2] == 0):
			self.osc2WaveNone.setChecked(True)
		elif(osc1[2] == 1):
			self.osc2WaveSaw.setChecked(True)
		elif(osc2[2] == 2):
			self.osc2WaveTri.setChecked(True)
		elif(osc2[2] == 3):
			self.osc2WaveSawTri.setChecked(True)
		elif(osc2[2] == 4):
			self.osc2WaveSquare.setChecked(True)
		
		self.osc2glide.setValue(osc2[3])
		self.osc2KeyB.setChecked(osc2[4])
		self.osc2Sub.setValue(osc2[5])
		
		self.oscSync.setChecked(oscmisc[0])
		self.comboBox.setCurrentIndex(oscmisc[1])
		self.oscSlop.setValue(oscmisc[2])
		self.oscPBR.setValue(oscmisc[3])
		self.comboBox_2.setCurrentIndex(oscmisc[4])
		
	def setupUi(self, Dialog):
		self.midi_output = None
		self.midi_channel = None
		
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(705, 269)
		
		self.osc1freq = QtGui.QDial(Dialog)
		self.osc1freq.setGeometry(QtCore.QRect(20, 30, 50, 64))
		self.osc1freq.setMaximum(1024)
		self.osc1freq.setObjectName(_fromUtf8("osc1freq"))
		self.osc1freq.valueChanged.connect(self.Osc1Freq)
		
		self.osc1fine = QtGui.QDial(Dialog)
		self.osc1fine.setGeometry(QtCore.QRect(80, 30, 50, 64))
		self.osc1fine.setMaximum(1024)
		self.osc1fine.setPageStep(1024)
		self.osc1fine.setObjectName(_fromUtf8("osc1fine"))
		self.osc1fine.valueChanged.connect(self.Osc1Fine)
		
		self.osc1shape = QtGui.QDial(Dialog)
		self.osc1shape.setGeometry(QtCore.QRect(140, 30, 50, 64))
		self.osc1shape.setMaximum(1024)
		self.osc1shape.setObjectName(_fromUtf8("osc1shape"))
		self.osc1shape.valueChanged.connect(self.Osc1Shape)
		
		self.groupBox = QtGui.QGroupBox(Dialog)
		self.groupBox.setGeometry(QtCore.QRect(190, 20, 151, 121))
		self.groupBox.setObjectName(_fromUtf8("groupBox"))
		
		self.osc1waveNone = QtGui.QRadioButton(self.groupBox)
		self.osc1waveNone.setGeometry(QtCore.QRect(10, 20, 82, 17))
		self.osc1waveNone.setObjectName(_fromUtf8("osc1waveNone"))
		self.osc1waveNone.toggled.connect(self.SendOsc1Wave)
		
		self.osc1WaveSaw = QtGui.QRadioButton(self.groupBox)
		self.osc1WaveSaw.setGeometry(QtCore.QRect(10, 40, 82, 17))
		self.osc1WaveSaw.setObjectName(_fromUtf8("osc1WaveSaw"))
		self.osc1WaveSaw.toggled.connect(self.SendOsc1Wave)
		
		self.osc1WaveTri = QtGui.QRadioButton(self.groupBox)
		self.osc1WaveTri.setGeometry(QtCore.QRect(10, 60, 82, 17))
		self.osc1WaveTri.setObjectName(_fromUtf8("osc1WaveTri"))
		self.osc1WaveTri.toggled.connect(self.SendOsc1Wave)
		
		self.osc1WaveSquare = QtGui.QRadioButton(self.groupBox)
		self.osc1WaveSquare.setGeometry(QtCore.QRect(10, 80, 82, 17))
		self.osc1WaveSquare.setObjectName(_fromUtf8("Square"))
		self.osc1WaveSquare.toggled.connect(self.SendOsc1Wave)
		self.osc1WaveSquare.setChecked(True)
		
		self.osc1WaveSawTri = QtGui.QRadioButton(self.groupBox)
		self.osc1WaveSawTri.setGeometry(QtCore.QRect(10, 100, 82, 21))
		self.osc1WaveSawTri.setObjectName(_fromUtf8("Osc1WaveSawTri"))
		self.osc1WaveSawTri.toggled.connect(self.SendOsc1Wave)
		
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(20, 20, 46, 13))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(30, 100, 46, 13))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QtGui.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(90, 100, 46, 13))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(Dialog)
		self.label_4.setGeometry(QtCore.QRect(150, 100, 46, 13))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.osc1glide = QtGui.QDial(Dialog)
		self.osc1glide.setGeometry(QtCore.QRect(20, 140, 50, 64))
		self.osc1glide.setMaximum(1024)
		self.osc1glide.setObjectName(_fromUtf8("osc1glide"))
		self.osc1glide.valueChanged.connect(self.Osc1Glide)
		
		self.label_5 = QtGui.QLabel(Dialog)
		self.label_5.setGeometry(QtCore.QRect(30, 210, 46, 13))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.osc1KeyB = QtGui.QCheckBox(Dialog)
		self.osc1KeyB.setGeometry(QtCore.QRect(90, 20, 70, 17))
		self.osc1KeyB.setObjectName(_fromUtf8("osc1KeyB"))
		self.osc1KeyB.toggled.connect(self.Osc1KeyB)
		
		self.osc1Sub = QtGui.QDial(Dialog)
		self.osc1Sub.setGeometry(QtCore.QRect(80, 140, 50, 64))
		self.osc1Sub.setMaximum(1024)
		self.osc1Sub.setObjectName(_fromUtf8("osc1Sub"))
		self.osc1Sub.valueChanged.connect(self.Osc1Sub)
		
		self.label_6 = QtGui.QLabel(Dialog)
		self.label_6.setGeometry(QtCore.QRect(90, 210, 46, 13))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.label_7 = QtGui.QLabel(Dialog)
		self.label_7.setGeometry(QtCore.QRect(430, 210, 46, 13))
		self.label_7.setObjectName(_fromUtf8("label_7"))
		self.groupBox_2 = QtGui.QGroupBox(Dialog)
		self.groupBox_2.setGeometry(QtCore.QRect(520, 20, 151, 121))
		self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
		
		self.osc2WaveNone = QtGui.QRadioButton(self.groupBox_2)
		self.osc2WaveNone.setGeometry(QtCore.QRect(10, 20, 82, 17))
		self.osc2WaveNone.setObjectName(_fromUtf8("osc2WaveNone"))
		self.osc2WaveNone.toggled.connect(self.SendOsc2Wave)
		
		self.osc2WaveSaw = QtGui.QRadioButton(self.groupBox_2)
		self.osc2WaveSaw.setGeometry(QtCore.QRect(10, 40, 82, 17))
		self.osc2WaveSaw.setObjectName(_fromUtf8("osc2WaveSaw"))
		self.osc2WaveSaw.toggled.connect(self.SendOsc2Wave)
		
		self.osc2WaveTri = QtGui.QRadioButton(self.groupBox_2)
		self.osc2WaveTri.setGeometry(QtCore.QRect(10, 60, 82, 17))
		self.osc2WaveTri.setObjectName(_fromUtf8("osc2WaveTri"))
		self.osc2WaveTri.toggled.connect(self.SendOsc2Wave)
		
		self.osc2WaveSquare = QtGui.QRadioButton(self.groupBox_2)
		self.osc2WaveSquare.setGeometry(QtCore.QRect(10, 80, 82, 17))
		self.osc2WaveSquare.setObjectName(_fromUtf8("osc2WaveSquare"))
		self.osc2WaveSquare.toggled.connect(self.SendOsc2Wave)
		self.osc2WaveSquare.setChecked(True)
		
		self.osc2WaveSawTri = QtGui.QRadioButton(self.groupBox_2)
		self.osc2WaveSawTri.setGeometry(QtCore.QRect(10, 100, 82, 21))
		self.osc2WaveSawTri.setObjectName(_fromUtf8("Osc2WaveSawTri"))
		self.osc2WaveSawTri.toggled.connect(self.SendOsc2Wave)
		
		self.osc2fine = QtGui.QDial(Dialog)
		self.osc2fine.setGeometry(QtCore.QRect(410, 30, 50, 64))
		self.osc2fine.setMaximum(1024)
		self.osc2fine.setPageStep(1024)
		self.osc2fine.setObjectName(_fromUtf8("osc2fine"))
		self.osc2fine.valueChanged.connect(self.Osc2Fine)
		
		
		self.osc2glide = QtGui.QDial(Dialog)
		self.osc2glide.setGeometry(QtCore.QRect(350, 140, 50, 64))
		self.osc2glide.setMaximum(1024)
		self.osc2glide.setObjectName(_fromUtf8("osc2glide"))
		self.osc2glide.valueChanged.connect(self.Osc2Glide)
		
		self.osc2freq = QtGui.QDial(Dialog)
		self.osc2freq.setGeometry(QtCore.QRect(350, 30, 50, 64))
		self.osc2freq.setMaximum(1024)
		self.osc2freq.setObjectName(_fromUtf8("osc2freq"))
		self.osc2freq.valueChanged.connect(self.Osc2Freq)
		
		self.osc2shape = QtGui.QDial(Dialog)
		self.osc2shape.setGeometry(QtCore.QRect(470, 30, 50, 64))
		self.osc2shape.setMaximum(1024)
		self.osc2shape.setObjectName(_fromUtf8("osc2shape"))
		self.osc2shape.valueChanged.connect(self.Osc2Shape)
		
		
		self.label_8 = QtGui.QLabel(Dialog)
		self.label_8.setGeometry(QtCore.QRect(360, 100, 46, 13))
		self.label_8.setObjectName(_fromUtf8("label_8"))
		self.label_9 = QtGui.QLabel(Dialog)
		self.label_9.setGeometry(QtCore.QRect(350, 20, 46, 13))
		self.label_9.setObjectName(_fromUtf8("label_9"))
		self.label_10 = QtGui.QLabel(Dialog)
		self.label_10.setGeometry(QtCore.QRect(420, 100, 46, 13))
		self.label_10.setObjectName(_fromUtf8("label_10"))
		self.label_11 = QtGui.QLabel(Dialog)
		self.label_11.setGeometry(QtCore.QRect(360, 210, 46, 13))
		self.label_11.setObjectName(_fromUtf8("label_11"))
		self.osc2KeyB = QtGui.QCheckBox(Dialog)
		self.osc2KeyB.setGeometry(QtCore.QRect(420, 20, 70, 17))
		self.osc2KeyB.setObjectName(_fromUtf8("osc2KeyB"))
		self.osc2KeyB.toggled.connect(self.Osc2KeyB)
		
		self.osc2Sub = QtGui.QDial(Dialog)
		self.osc2Sub.setGeometry(QtCore.QRect(410, 140, 50, 64))
		self.osc2Sub.setMaximum(1024)
		self.osc2Sub.setObjectName(_fromUtf8("osc2Sub"))
		self.osc2Sub.valueChanged.connect(self.Osc2Sub)
		
		self.label_12 = QtGui.QLabel(Dialog)
		self.label_12.setGeometry(QtCore.QRect(480, 100, 46, 13))
		self.label_12.setObjectName(_fromUtf8("label_12"))
		self.oscSlop = QtGui.QDial(Dialog)
		self.oscSlop.setGeometry(QtCore.QRect(160, 160, 50, 64))
		self.oscSlop.setObjectName(_fromUtf8("oscSlop"))
		self.oscSlop.valueChanged.connect(self.OscSlop)
		
		self.oscSync = QtGui.QCheckBox(Dialog)
		self.oscSync.setGeometry(QtCore.QRect(220, 140, 70, 17))
		self.oscSync.setObjectName(_fromUtf8("oscSync"))
		self.oscSync.toggled.connect(self.OscSync)
		
		self.label_13 = QtGui.QLabel(Dialog)
		self.label_13.setGeometry(QtCore.QRect(170, 230, 46, 13))
		self.label_13.setObjectName(_fromUtf8("label_13"))
		self.comboBox = QtGui.QComboBox(Dialog)
		self.comboBox.setGeometry(QtCore.QRect(590, 220, 81, 22))
		self.comboBox.setObjectName(_fromUtf8("comboBox"))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.addItem(_fromUtf8(""))
		self.comboBox.currentIndexChanged.connect(self.GlideMode)
		
		self.label_14 = QtGui.QLabel(Dialog)
		self.label_14.setGeometry(QtCore.QRect(590, 200, 81, 16))
		self.label_14.setObjectName(_fromUtf8("label_14"))
		self.oscPBR = QtGui.QDial(Dialog)
		self.oscPBR.setGeometry(QtCore.QRect(480, 160, 50, 64))
		self.oscPBR.setMaximum(1024)
		self.oscPBR.setObjectName(_fromUtf8("oscPBR"))
		self.oscPBR.valueChanged.connect(self.PBRange)
		
		self.labelpbr = QtGui.QLabel(Dialog)
		self.labelpbr.setGeometry(QtCore.QRect(490, 230, 46, 13))
		self.labelpbr.setObjectName(_fromUtf8("labelpbr"))
		self.comboBox_2 = QtGui.QComboBox(Dialog)
		self.comboBox_2.setGeometry(QtCore.QRect(590, 170, 69, 22))
		self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
		self.comboBox_2.addItem(_fromUtf8(""))
		self.comboBox_2.addItem(_fromUtf8(""))
		self.comboBox_2.addItem(_fromUtf8(""))
		self.comboBox_2.addItem(_fromUtf8(""))
		self.comboBox_2.addItem(_fromUtf8(""))
		self.comboBox_2.addItem(_fromUtf8(""))
		self.comboBox_2.currentIndexChanged.connect(self.KeyAssign)
		
		self.label_15 = QtGui.QLabel(Dialog)
		self.label_15.setGeometry(QtCore.QRect(590, 150, 71, 16))
		self.label_15.setObjectName(_fromUtf8("label_15"))
		
		self.oscMix = QtGui.QDial(Dialog)
		self.oscMix.setGeometry(QtCore.QRect(220, 160, 51, 61))
		self.oscMix.setMaximum(1024)
		self.oscMix.valueChanged.connect(self.OscMix)		
		self.oscMix.setObjectName(_fromUtf8("oscMix"))
		
		self.label_16 = QtGui.QLabel(Dialog)
		self.label_16.setGeometry(QtCore.QRect(230, 230, 31, 16))
		self.label_16.setObjectName(_fromUtf8("label_16"))
		self.oscNoise = QtGui.QDial(Dialog)
		self.oscNoise.setGeometry(QtCore.QRect(530, 160, 50, 64))
		self.oscNoise.setMaximum(1024)
		self.oscNoise.setObjectName(_fromUtf8("oscNoise"))
		self.oscNoise.valueChanged.connect(self.NoiseLvl)
		
		self.label_17 = QtGui.QLabel(Dialog)
		self.label_17.setGeometry(QtCore.QRect(540, 230, 46, 13))
		self.label_17.setObjectName(_fromUtf8("label_17"))
		self.oscAudioIn = QtGui.QDial(Dialog)
		self.oscAudioIn.setGeometry(QtCore.QRect(280, 160, 50, 64))
		self.oscAudioIn.setMinimum(0)
		self.oscAudioIn.setMaximum(1024)
		self.oscAudioIn.setObjectName(_fromUtf8("oscAudioIn"))
		self.oscAudioIn.valueChanged.connect(self.ExtAudioIn)
		
		self.label_18 = QtGui.QLabel(Dialog)
		self.label_18.setGeometry(QtCore.QRect(280, 230, 51, 16))
		self.label_18.setObjectName(_fromUtf8("label_18"))

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.groupBox.setTitle(_translate("Dialog", "Wave 1", None))
		self.osc1waveNone.setText(_translate("Dialog", "None", None))
		self.osc1WaveSaw.setText(_translate("Dialog", "Saw", None))
		self.osc1WaveTri.setText(_translate("Dialog", "Triangle", None))
		self.osc1WaveSquare.setText(_translate("Dialog", "Square", None))
		self.osc1WaveSawTri.setText(_translate("Dialog", "Saw/Tri", None))
		self.label.setText(_translate("Dialog", "Osc1", None))
		self.label_2.setText(_translate("Dialog", "Freq", None))
		self.label_3.setText(_translate("Dialog", "Fine", None))
		self.label_4.setText(_translate("Dialog", "Pulse", None))
		self.label_5.setText(_translate("Dialog", "Glide", None))
		self.osc1KeyB.setText(_translate("Dialog", "Keyboard ", None))
		self.label_6.setText(_translate("Dialog", "Sub", None))
		self.label_7.setText(_translate("Dialog", "Sub", None))
		self.groupBox_2.setTitle(_translate("Dialog", "Wave 2", None))
		self.osc2WaveNone.setText(_translate("Dialog", "None", None))
		self.osc2WaveSaw.setText(_translate("Dialog", "Saw", None))
		self.osc2WaveTri.setText(_translate("Dialog", "Triangle", None))
		self.osc2WaveSquare.setText(_translate("Dialog", "Square", None))
		self.osc2WaveSawTri.setText(_translate("Dialog", "Saw/Tri", None))
		self.label_8.setText(_translate("Dialog", "Freq", None))
		self.label_9.setText(_translate("Dialog", "Osc2", None))
		self.label_10.setText(_translate("Dialog", "Fine", None))
		self.label_11.setText(_translate("Dialog", "Glide", None))
		self.osc2KeyB.setText(_translate("Dialog", "Keyboard ", None))
		self.label_12.setText(_translate("Dialog", "Pulse", None))
		self.label_13.setText(_translate("Dialog", "OscSlop", None))
		self.comboBox.setItemText(0, _translate("Dialog", "Fixed Rate", None))
		self.comboBox.setItemText(1, _translate("Dialog", "Fixed Rate Auto", None))
		self.comboBox.setItemText(2, _translate("Dialog", "Fixed Time", None))
		self.comboBox.setItemText(3, _translate("Dialog", "Fixed Time Auto", None))
		self.label_14.setText(_translate("Dialog", "Glide Mode", None))
		self.labelpbr.setText(_translate("Dialog", "PBR", None))
		self.comboBox_2.setItemText(0, _translate("Dialog", "Low Note ", None))
		self.comboBox_2.setItemText(1, _translate("Dialog", "Low note with re-trig", None))
		self.comboBox_2.setItemText(2, _translate("Dialog", "High Note", None))
		self.comboBox_2.setItemText(3, _translate("Dialog", "High Note with re-trig", None))
		self.comboBox_2.setItemText(4, _translate("Dialog", "Last Note", None))
		self.comboBox_2.setItemText(5, _translate("Dialog", "Last Note with re-trig", None))
		self.label_15.setText(_translate("Dialog", "Key Assign", None))
		self.label_16.setText(_translate("Dialog", "Mix", None))
		self.label_17.setText(_translate("Dialog", "Noise", None))
		self.label_18.setText(_translate("Dialog", "Ext Audio", None))
		self.oscSync.setText(_translate("Dialog", "Sync", None))

	def Osc1Freq(self,value):
		x = int(math.ceil((value/1024.0)*120.0))
		nrpn = 0
		SendNRPN(nrpn,x,self.midi_channel)
		
	def Osc1Fine(self,value):
		x = int(math.ceil((value/1024.0)*100.0))
		nrpn = 1
		SendNRPN(nrpn,x,self.midi_channel)
	
	def Osc1Glide(self,value):
		x = int(math.ceil((value/1024.0)*127.0))
		nrpn = 3
		SendNRPN(nrpn,x,self.midi_channel)
			
	def Osc1KeyB(self):
		k =self.osc1KeyB.isChecked()
		SendNRPN(4,k,self.midi_channel)
	
	def Osc1Sub(self,value):
		x = int(math.ceil((value/1024.0)*127.0))
		nrpn = 114
		SendNRPN(nrpn,x,self.midi_channel)
	
	def Osc1Shape(self,value):
		nrpn = 2
		x = int(math.ceil((value/1024.0)*99.0))+4
		if(self.osc1WaveSquare.isChecked() == True):
			SendNRPN(nrpn,x,self.midi_channel)
		
	def SendOsc1Wave(self, value):
		nrpn = 2
		wave = 0
		if(self.osc1waveNone.isChecked() == True):
			wave = 0
		elif(self.osc1WaveSaw.isChecked() == True):
			wave = 1
		elif(self.osc1WaveTri.isChecked() == True):
			wave = 2
		elif(self.osc1WaveSawTri.isChecked() == True):
			wave = 3
		else:
			wave = 4
			wave = self.osc1shape.value()
			wave = int((wave/1024.0)*99.0)+4
			
		SendNRPN(nrpn,wave,self.midi_channel)
			
		
	def Osc2Freq(self,value):
		x = int(math.ceil((value/1024.0)*120.0))
		nrpn = 5
		SendNRPN(nrpn,x,self.midi_channel)
		
	def Osc2Fine(self,value):
		x = int(math.ceil((value/1024.0)*100.0))
		nrpn = 6
		SendNRPN(nrpn,x,self.midi_channel)
	
	def Osc2Glide(self,value):
		x = int(math.ceil((value/1024.0)*127.0))
		nrpn = 8
		SendNRPN(nrpn,x,self.midi_channel)
			
	def Osc2KeyB(self):
		k =self.osc2KeyB.isChecked()
		SendNRPN(9,k,self.midi_channel)
		
	def Osc2Sub(self,value):
		x = int(math.ceil((value/1024.0)*127.0))
		nrpn = 115
		SendNRPN(nrpn,x,self.midi_channel)
	
	def Osc2Shape(self,value):
		nrpn = 7
		x = int(math.ceil((value/1024.0)*99.0))+4
		if(self.osc2WaveSquare.isChecked() == True):
			SendNRPN(nrpn,x,self.midi_channel)
				
	def SendOsc2Wave(self, value):
		nrpn = 7
		wave = 4
		if(self.osc2WaveNone.isChecked() == True):
			wave = 0
		elif(self.osc2WaveSaw.isChecked() == True):
			wave = 1
		elif(self.osc2WaveTri.isChecked() == True):
			wave = 2
		elif(self.osc2WaveSawTri.isChecked() == True):
			wave = 3
		else:
			wave = self.osc2shape.value()
			wave = int(math.ceil((wave/1024.0)*99.0))+4
			
		SendNRPN(nrpn,wave,self.midi_channel)
			
	def OscSlop(self,value):
		nrpn = 12
		x = int(math.ceil((value/99.0)*5.0))
		SendNRPN(nrpn,x,self.midi_channel)
		
	def OscSync(self,value):
		sync = self.oscSync.isChecked()
		nrpn = 10
		SendNRPN(nrpn,sync,self.midi_channel)
		
	def GlideMode(self,value):
		nrpn = 11
		SendNRPN(nrpn,value,self.midi_channel)
		
	def PBRange(self,value):
		nrpn = 93
		x = int(math.ceil((value/1024.0)*12.0))
		SendNRPN(nrpn,x,self.midi_channel)
		
	def KeyAssign(self,value):
		nrpn = 96
		SendNRPN(nrpn,value,self.midi_channel)
	
	def OscMix(self,value):
		x = int(math.ceil((value/1024.0)*127.0))
		nrpn = 13
		SendNRPN(nrpn,x,self.midi_channel)
		
	def NoiseLvl(self,value):
		x = int(math.ceil((value/1024.0)*127.0))
		nrpn = 14
		SendNRPN(nrpn,x,self.midi_channel)
		
	def ExtAudioIn(self,value):
		x = int(math.ceil((value/1024.0)*127.0))
		nrpn = 116
		SendNRPN(nrpn,x,self.midi_channel)
		