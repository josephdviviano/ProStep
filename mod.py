# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mod.ui'
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

class Ui_ModDialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(362, 175)
		self.modDest = QtGui.QComboBox(Dialog)
		self.modDest.setGeometry(QtCore.QRect(100, 100, 121, 22))
		self.modDest.setObjectName(_fromUtf8("modDest"))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.addItem(_fromUtf8(""))
		self.modDest.setItemText(48, _fromUtf8(""))
		self.modDest.currentIndexChanged.connect(self.ModDest)

		self.label_3 = QtGui.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(100, 80, 46, 13))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.modAmt = QtGui.QDial(Dialog)
		self.modAmt.setGeometry(QtCore.QRect(20, 40, 50, 64))
		self.modAmt.setMaximum(1024)
		self.modAmt.setObjectName(_fromUtf8("modAmt"))
		self.modAmt.valueChanged.connect(self.ModAmt)

		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(40, 110, 41, 20))
		self.label.setObjectName(_fromUtf8("label"))
		self.modSrc = QtGui.QComboBox(Dialog)
		self.modSrc.setGeometry(QtCore.QRect(100, 50, 121, 22))
		self.modSrc.setObjectName(_fromUtf8("modSrc"))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.addItem(_fromUtf8(""))
		self.modSrc.currentIndexChanged.connect(self.ModSrc)

		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(100, 30, 46, 13))
		self.label_2.setObjectName(_fromUtf8("label_2"))

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.modDest.setItemText(0, _translate("Dialog", "Off", None))
		self.modDest.setItemText(1, _translate("Dialog", "Osc 1 Freq", None))
		self.modDest.setItemText(2, _translate("Dialog", "Osc 2 Freq", None))
		self.modDest.setItemText(3, _translate("Dialog", "Osc 1+2 Freq", None))
		self.modDest.setItemText(4, _translate("Dialog", "Osc Mix", None))
		self.modDest.setItemText(5, _translate("Dialog", "Noise Level", None))
		self.modDest.setItemText(6, _translate("Dialog", "Osc 1 PW", None))
		self.modDest.setItemText(7, _translate("Dialog", "Osc 2 PW", None))
		self.modDest.setItemText(8, _translate("Dialog", "Osc 1+2 PW", None))
		self.modDest.setItemText(9, _translate("Dialog", "Filter Freq", None))
		self.modDest.setItemText(10, _translate("Dialog", "Resonance", None))
		self.modDest.setItemText(11, _translate("Dialog", "Filter Audio Mod", None))
		self.modDest.setItemText(12, _translate("Dialog", "VCA Level", None))
		self.modDest.setItemText(13, _translate("Dialog", "Pan", None))
		self.modDest.setItemText(14, _translate("Dialog", "LFO 1 Freq", None))
		self.modDest.setItemText(15, _translate("Dialog", "LFO2 Freq", None))
		self.modDest.setItemText(16, _translate("Dialog", "LFO3 Freq", None))
		self.modDest.setItemText(17, _translate("Dialog", "LFO4 Freq", None))
		self.modDest.setItemText(18, _translate("Dialog", "All LFO Freq", None))
		self.modDest.setItemText(19, _translate("Dialog", "LFO1 Amt", None))
		self.modDest.setItemText(20, _translate("Dialog", "LFO2 Amt", None))
		self.modDest.setItemText(21, _translate("Dialog", "LFO3 Amt", None))
		self.modDest.setItemText(22, _translate("Dialog", "LFO4 Amt", None))
		self.modDest.setItemText(23, _translate("Dialog", "All LFO Amt", None))
		self.modDest.setItemText(24, _translate("Dialog", "Filter Env Amt", None))
		self.modDest.setItemText(25, _translate("Dialog", "Amp Env Amt", None))
		self.modDest.setItemText(26, _translate("Dialog", "Env 3 Amt", None))
		self.modDest.setItemText(27, _translate("Dialog", "All Env Amt", None))
		self.modDest.setItemText(28, _translate("Dialog", "Env1 Attak", None))
		self.modDest.setItemText(29, _translate("Dialog", "Env2 Attack", None))
		self.modDest.setItemText(30, _translate("Dialog", "Env3 Attack", None))
		self.modDest.setItemText(31, _translate("Dialog", "All Env Attacks", None))
		self.modDest.setItemText(32, _translate("Dialog", "Env1 Decay", None))
		self.modDest.setItemText(33, _translate("Dialog", "Env2 Decay", None))
		self.modDest.setItemText(34, _translate("Dialog", "Env3 Decay", None))
		self.modDest.setItemText(35, _translate("Dialog", "All Env Decays", None))
		self.modDest.setItemText(36, _translate("Dialog", "Env1 Release", None))
		self.modDest.setItemText(37, _translate("Dialog", "Env2 Release", None))
		self.modDest.setItemText(38, _translate("Dialog", "Env3 Release", None))
		self.modDest.setItemText(39, _translate("Dialog", "All Env Releases", None))
		self.modDest.setItemText(40, _translate("Dialog", "Mod1 Amt", None))
		self.modDest.setItemText(41, _translate("Dialog", "Mod2 Amt", None))
		self.modDest.setItemText(42, _translate("Dialog", "Mod3 Amt", None))
		self.modDest.setItemText(43, _translate("Dialog", "Mod4 Amt", None))
		self.modDest.setItemText(44, _translate("Dialog", "Ext Audio In Level", None))
		self.modDest.setItemText(45, _translate("Dialog", "Sub Osc1", None))
		self.modDest.setItemText(46, _translate("Dialog", "Sub Osc 2", None))
		self.modDest.setItemText(47, _translate("Dialog", "Skew 1/2", None))
		self.label_3.setText(_translate("Dialog", "Mod Dest", None))
		self.label.setText(_translate("Dialog", "Amt", None))
		self.modSrc.setItemText(0, _translate("Dialog", "Off", None))
		self.modSrc.setItemText(1, _translate("Dialog", "Sequence Track 1", None))
		self.modSrc.setItemText(2, _translate("Dialog", "Sequence Track 2", None))
		self.modSrc.setItemText(3, _translate("Dialog", "Sequence Track 3", None))
		self.modSrc.setItemText(4, _translate("Dialog", "Sequence Track 4", None))
		self.modSrc.setItemText(5, _translate("Dialog", "LFO 1", None))
		self.modSrc.setItemText(6, _translate("Dialog", "LFO 2", None))
		self.modSrc.setItemText(7, _translate("Dialog", "LFO 3", None))
		self.modSrc.setItemText(8, _translate("Dialog", "LFO 4", None))
		self.modSrc.setItemText(9, _translate("Dialog", "Filter Envelope", None))
		self.modSrc.setItemText(10, _translate("Dialog", "Amp Envelope", None))
		self.modSrc.setItemText(11, _translate("Dialog", "Envelope 3", None))
		self.modSrc.setItemText(12, _translate("Dialog", "Pitch Bend", None))
		self.modSrc.setItemText(13, _translate("Dialog", "Mod Wheel", None))
		self.modSrc.setItemText(14, _translate("Dialog", "Pressure", None))
		self.modSrc.setItemText(15, _translate("Dialog", "Breath", None))
		self.modSrc.setItemText(16, _translate("Dialog", "Foot", None))
		self.modSrc.setItemText(17, _translate("Dialog", "Expression", None))
		self.modSrc.setItemText(18, _translate("Dialog", "Velocity", None))
		self.modSrc.setItemText(19, _translate("Dialog", "Note Number", None))
		self.modSrc.setItemText(20, _translate("Dialog", "Noise", None))
		self.modSrc.setItemText(21, _translate("Dialog", "Audio In Envelope Follower", None))
		self.modSrc.setItemText(22, _translate("Dialog", "Audio in Peak", None))
		self.label_2.setText(_translate("Dialog", "Mod Src", None))

	def ModAmt(self,value):
		x = int(math.ceil(value/1024.0 * 254.0))
		if(self.mod_num == 1):
			nrpn = 66
		elif(self.mod_num == 2):
			nrpn = 69
		elif(self.mod_num == 3):
			nrpn = 72
		else:
			nrpn = 75
			
		SendNRPN(nrpn,x,self.midi_channel)
		
	def ModSrc(self,value):
		x = self.modSrc.currentIndex()
		if(self.mod_num == 1):
			nrpn = 65
		elif(self.mod_num == 2):
			nrpn = 68
		elif(self.mod_num == 3):
			nrpn = 71
		else:
			nrpn = 74
		SendNRPN(nrpn,x,self.midi_channel)
		
	def ModDest(self,value):
		x = self.modDest.currentIndex()
		if(self.mod_num == 1):
			nrpn = 67
		elif(self.mod_num == 2):
			nrpn = 70
		elif(self.mod_num == 3):
			nrpn = 73
		else:
			nrpn = 76
		SendNRPN(nrpn,x,self.midi_channel)
		