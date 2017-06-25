# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'env3.ui'
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

class Ui_ENV3Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(400, 300)
		self.label_3 = QtGui.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(240, 10, 46, 13))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.env3ModDest = QtGui.QComboBox(Dialog)
		self.env3ModDest.setGeometry(QtCore.QRect(240, 30, 121, 22))
		self.env3ModDest.setObjectName(_fromUtf8("env3ModDest"))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.addItem(_fromUtf8(""))
		self.env3ModDest.setItemText(48, _fromUtf8(""))
		self.env3ModDest.currentIndexChanged.connect(self.EnvModDest)

		self.env3Repeat = QtGui.QCheckBox(Dialog)
		self.env3Repeat.setGeometry(QtCore.QRect(240, 70, 70, 17))
		self.env3Repeat.setObjectName(_fromUtf8("env3Repeat"))
		self.env3Repeat.toggled.connect(self.EnvRepeat)

		self.label_7 = QtGui.QLabel(Dialog)
		self.label_7.setGeometry(QtCore.QRect(70, 270, 21, 16))
		self.label_7.setObjectName(_fromUtf8("label_7"))
		self.label_9 = QtGui.QLabel(Dialog)
		self.label_9.setGeometry(QtCore.QRect(140, 270, 16, 16))
		self.label_9.setObjectName(_fromUtf8("label_9"))
		self.label_8 = QtGui.QLabel(Dialog)
		self.label_8.setGeometry(QtCore.QRect(100, 270, 16, 16))
		self.label_8.setObjectName(_fromUtf8("label_8"))
		self.label_5 = QtGui.QLabel(Dialog)
		self.label_5.setGeometry(QtCore.QRect(20, 270, 46, 13))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.label_11 = QtGui.QLabel(Dialog)
		self.label_11.setGeometry(QtCore.QRect(200, 270, 41, 20))
		self.label_11.setObjectName(_fromUtf8("label_11"))
		self.label_10 = QtGui.QLabel(Dialog)
		self.label_10.setGeometry(QtCore.QRect(170, 270, 16, 16))
		self.label_10.setObjectName(_fromUtf8("label_10"))
		self.widget = QtGui.QWidget(Dialog)
		self.widget.setGeometry(QtCore.QRect(30, 30, 191, 231))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

		self.env3EnvAmt = QtGui.QSlider(self.widget)
		self.env3EnvAmt.setMaximum(1024)
		self.env3EnvAmt.setOrientation(QtCore.Qt.Vertical)
		self.env3EnvAmt.setObjectName(_fromUtf8("env3EnvAmt"))
		self.env3EnvAmt.valueChanged.connect(self.EnvAmt)

		self.horizontalLayout.addWidget(self.env3EnvAmt)
		self.env3Delay = QtGui.QSlider(self.widget)
		self.env3Delay.setMaximum(1024)
		self.env3Delay.setOrientation(QtCore.Qt.Vertical)
		self.env3Delay.setObjectName(_fromUtf8("env3Delay"))
		self.env3Delay.valueChanged.connect(self.EnvDelay)

		self.horizontalLayout.addWidget(self.env3Delay)
		self.env3Attack = QtGui.QSlider(self.widget)
		self.env3Attack.setMaximum(1024)
		self.env3Attack.setOrientation(QtCore.Qt.Vertical)
		self.env3Attack.setObjectName(_fromUtf8("env3Attack"))
		self.env3Attack.valueChanged.connect(self.EnvAttack)
		self.horizontalLayout.addWidget(self.env3Attack)

		self.env3Decay = QtGui.QSlider(self.widget)
		self.env3Decay.setMaximum(1024)
		self.env3Decay.setOrientation(QtCore.Qt.Vertical)
		self.env3Decay.setObjectName(_fromUtf8("env3Decay"))
		self.env3Decay.valueChanged.connect(self.EnvDecay)
		self.horizontalLayout.addWidget(self.env3Decay)

		self.env3Sustain = QtGui.QSlider(self.widget)
		self.env3Sustain.setMaximum(1024)
		self.env3Sustain.setOrientation(QtCore.Qt.Vertical)
		self.env3Sustain.setObjectName(_fromUtf8("env3Sustain"))
		self.horizontalLayout.addWidget(self.env3Sustain)
		self.env3Sustain.valueChanged.connect(self.EnvSustain)

		self.env3Release = QtGui.QSlider(self.widget)
		self.env3Release.setMaximum(1024)
		self.env3Release.setOrientation(QtCore.Qt.Vertical)
		self.env3Release.setObjectName(_fromUtf8("env3Release"))
		self.horizontalLayout.addWidget(self.env3Release)
		self.env3Release.valueChanged.connect(self.EnvRelease)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label_3.setText(_translate("Dialog", "Mod Dest", None))
		self.env3ModDest.setItemText(0, _translate("Dialog", "Off", None))
		self.env3ModDest.setItemText(1, _translate("Dialog", "Osc 1 Freq", None))
		self.env3ModDest.setItemText(2, _translate("Dialog", "Osc 2 Freq", None))
		self.env3ModDest.setItemText(3, _translate("Dialog", "Osc 1+2 Freq", None))
		self.env3ModDest.setItemText(4, _translate("Dialog", "Osc Mix", None))
		self.env3ModDest.setItemText(5, _translate("Dialog", "Noise Level", None))
		self.env3ModDest.setItemText(6, _translate("Dialog", "Osc 1 PW", None))
		self.env3ModDest.setItemText(7, _translate("Dialog", "Osc 2 PW", None))
		self.env3ModDest.setItemText(8, _translate("Dialog", "Osc 1+2 PW", None))
		self.env3ModDest.setItemText(9, _translate("Dialog", "Filter Freq", None))
		self.env3ModDest.setItemText(10, _translate("Dialog", "Resonance", None))
		self.env3ModDest.setItemText(11, _translate("Dialog", "Filter Audio Mod", None))
		self.env3ModDest.setItemText(12, _translate("Dialog", "VCA Level", None))
		self.env3ModDest.setItemText(13, _translate("Dialog", "Pan", None))
		self.env3ModDest.setItemText(14, _translate("Dialog", "LFO 1 Freq", None))
		self.env3ModDest.setItemText(15, _translate("Dialog", "LFO2 Freq", None))
		self.env3ModDest.setItemText(16, _translate("Dialog", "LFO3 Freq", None))
		self.env3ModDest.setItemText(17, _translate("Dialog", "LFO4 Freq", None))
		self.env3ModDest.setItemText(18, _translate("Dialog", "All LFO Freq", None))
		self.env3ModDest.setItemText(19, _translate("Dialog", "LFO1 Amt", None))
		self.env3ModDest.setItemText(20, _translate("Dialog", "LFO2 Amt", None))
		self.env3ModDest.setItemText(21, _translate("Dialog", "LFO3 Amt", None))
		self.env3ModDest.setItemText(22, _translate("Dialog", "LFO4 Amt", None))
		self.env3ModDest.setItemText(23, _translate("Dialog", "All LFO Amt", None))
		self.env3ModDest.setItemText(24, _translate("Dialog", "Filter Env Amt", None))
		self.env3ModDest.setItemText(25, _translate("Dialog", "Amp Env Amt", None))
		self.env3ModDest.setItemText(26, _translate("Dialog", "Env 3 Amt", None))
		self.env3ModDest.setItemText(27, _translate("Dialog", "All Env Amt", None))
		self.env3ModDest.setItemText(28, _translate("Dialog", "Env1 Attak", None))
		self.env3ModDest.setItemText(29, _translate("Dialog", "Env2 Attack", None))
		self.env3ModDest.setItemText(30, _translate("Dialog", "Env3 Attack", None))
		self.env3ModDest.setItemText(31, _translate("Dialog", "All Env Attacks", None))
		self.env3ModDest.setItemText(32, _translate("Dialog", "Env1 Decay", None))
		self.env3ModDest.setItemText(33, _translate("Dialog", "Env2 Decay", None))
		self.env3ModDest.setItemText(34, _translate("Dialog", "Env3 Decay", None))
		self.env3ModDest.setItemText(35, _translate("Dialog", "All Env Decays", None))
		self.env3ModDest.setItemText(36, _translate("Dialog", "Env1 Release", None))
		self.env3ModDest.setItemText(37, _translate("Dialog", "Env2 Release", None))
		self.env3ModDest.setItemText(38, _translate("Dialog", "Env3 Release", None))
		self.env3ModDest.setItemText(39, _translate("Dialog", "All Env Releases", None))
		self.env3ModDest.setItemText(40, _translate("Dialog", "Mod1 Amt", None))
		self.env3ModDest.setItemText(41, _translate("Dialog", "Mod2 Amt", None))
		self.env3ModDest.setItemText(42, _translate("Dialog", "Mod3 Amt", None))
		self.env3ModDest.setItemText(43, _translate("Dialog", "Mod4 Amt", None))
		self.env3ModDest.setItemText(44, _translate("Dialog", "Ext Audio In Level", None))
		self.env3ModDest.setItemText(45, _translate("Dialog", "Sub Osc1", None))
		self.env3ModDest.setItemText(46, _translate("Dialog", "Sub Osc 2", None))
		self.env3ModDest.setItemText(47, _translate("Dialog", "Skew 1/2", None))
		self.env3Repeat.setText(_translate("Dialog", "Repeat", None))
		self.label_7.setText(_translate("Dialog", "DLY", None))
		self.label_9.setText(_translate("Dialog", "D", None))
		self.label_8.setText(_translate("Dialog", "A", None))
		self.label_5.setText(_translate("Dialog", "Env Amt", None))
		self.label_11.setText(_translate("Dialog", "R", None))
		self.label_10.setText(_translate("Dialog", "S", None))

	def EnvModDest(self,value):
		x = self.env3ModDest.currentIndex()
		nrpn = 57
		SendNRPN(nrpn,x,self.midi_channel)
		
	def EnvAmt(self,value):
		x = int(math.ceil(value/1024.0 * 254.0))
		nrpn = 58
		SendNRPN(nrpn,x,self.midi_channel)
		
	def EnvVelAmt(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 59
		SendNRPN(nrpn,x,self.midi_channel)
		
	def EnvDelay(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 60
		SendNRPN(nrpn,x,self.midi_channel)
		
	def EnvAttack(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 61
		SendNRPN(nrpn,x,self.midi_channel)
		
	def EnvDecay(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 62
		SendNRPN(nrpn,x,self.midi_channel)
		
	def EnvSustain(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 63
		SendNRPN(nrpn,x,self.midi_channel)
		
	def EnvRelease(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 64
		SendNRPN(nrpn,x,self.midi_channel)
		
	def EnvRepeat(self,value):
		nrpn = 98
		x = self.env3Repeat.isChecked()
		SendNRPN(nrpn,x,self.midi_channel)
		