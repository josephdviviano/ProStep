# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter.ui'
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

class Ui_FilterDialog(object):

	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(500, 300)
		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(120, 100, 31, 16))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QtGui.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(180, 100, 46, 13))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(40, 80, 31, 69))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_4 = QtGui.QLabel(Dialog)
		self.label_4.setGeometry(QtCore.QRect(110, 230, 46, 13))
		self.label_4.setObjectName(_fromUtf8("label_4"))

		self.filt4pole = QtGui.QCheckBox(Dialog)
		self.filt4pole.setGeometry(QtCore.QRect(250, 10, 70, 17))
		self.filt4pole.setObjectName(_fromUtf8("filt4pole"))
		self.filt4pole.toggled.connect(self.Filt4Pole)
		
		self.filtEnvAmt = QtGui.QSlider(Dialog)
		self.filtEnvAmt.setGeometry(QtCore.QRect(250, 50, 19, 191))
		self.filtEnvAmt.setMinimum(-1024)
		self.filtEnvAmt.setMaximum(1024)
		self.filtEnvAmt.setOrientation(QtCore.Qt.Vertical)
		self.filtEnvAmt.setObjectName(_fromUtf8("filtEnvAmt"))
		self.filtEnvAmt.valueChanged.connect(self.FiltEnvAmt)
		
		self.label_5 = QtGui.QLabel(Dialog)
		self.label_5.setGeometry(QtCore.QRect(240, 260, 46, 13))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.label_6 = QtGui.QLabel(Dialog)
		self.label_6.setGeometry(QtCore.QRect(40, 230, 46, 16))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.label_7 = QtGui.QLabel(Dialog)
		self.label_7.setGeometry(QtCore.QRect(310, 270, 21, 16))
		self.label_7.setObjectName(_fromUtf8("label_7"))
		self.label_8 = QtGui.QLabel(Dialog)
		self.label_8.setGeometry(QtCore.QRect(350, 270, 16, 16))
		self.label_8.setObjectName(_fromUtf8("label_8"))
		self.label_9 = QtGui.QLabel(Dialog)
		self.label_9.setGeometry(QtCore.QRect(390, 270, 16, 16))
		self.label_9.setObjectName(_fromUtf8("label_9"))
		self.label_10 = QtGui.QLabel(Dialog)
		self.label_10.setGeometry(QtCore.QRect(430, 270, 16, 16))
		self.label_10.setObjectName(_fromUtf8("label_10"))
		self.label_11 = QtGui.QLabel(Dialog)
		self.label_11.setGeometry(QtCore.QRect(470, 270, 21, 20))
		self.label_11.setObjectName(_fromUtf8("label_11"))
		self.widget = QtGui.QWidget(Dialog)
		self.widget.setGeometry(QtCore.QRect(20, 10, 211, 81))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.filtCutoff = QtGui.QDial(self.widget)
		self.filtCutoff.setMaximum(1024)
		self.filtCutoff.setObjectName(_fromUtf8("filtCutoff"))
		self.filtCutoff.valueChanged.connect(self.FiltCutoff)
		
		self.horizontalLayout.addWidget(self.filtCutoff)
		self.filtRes = QtGui.QDial(self.widget)
		self.filtRes.setMaximum(1024)
		self.filtRes.setObjectName(_fromUtf8("filtRes"))
		self.filtRes.valueChanged.connect(self.FiltRes)
		self.horizontalLayout.addWidget(self.filtRes)
		
		self.filtKeyAmt = QtGui.QDial(self.widget)
		self.filtKeyAmt.setMaximum(1024)
		self.filtKeyAmt.setObjectName(_fromUtf8("filtKeyAmt"))
		self.horizontalLayout.addWidget(self.filtKeyAmt)
		self.filtKeyAmt.valueChanged.connect(self.FiltKeyAmt)
		
		self.widget1 = QtGui.QWidget(Dialog)
		self.widget1.setGeometry(QtCore.QRect(20, 140, 141, 71))
		self.widget1.setObjectName(_fromUtf8("widget1"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget1)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.filtVelAmt = QtGui.QDial(self.widget1)
		self.filtVelAmt.setMaximum(1024)
		self.filtVelAmt.setObjectName(_fromUtf8("filtVelAmt"))
		self.horizontalLayout_2.addWidget(self.filtVelAmt)
		self.filtVelAmt.valueChanged.connect(self.FiltVelAmt)
		
		self.filtAudioMix = QtGui.QDial(self.widget1)
		self.filtAudioMix.setMaximum(1024)
		self.filtAudioMix.setObjectName(_fromUtf8("filtAudioMix"))
		self.filtAudioMix.valueChanged.connect(self.FiltAudioMod)
		
		self.horizontalLayout_2.addWidget(self.filtAudioMix)
		self.widget2 = QtGui.QWidget(Dialog)
		self.widget2.setGeometry(QtCore.QRect(290, 39, 201, 221))
		self.widget2.setObjectName(_fromUtf8("widget2"))
		self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget2)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.filtDelay = QtGui.QSlider(self.widget2)
		self.filtDelay.setMaximum(1024)
		self.filtDelay.setOrientation(QtCore.Qt.Vertical)
		self.filtDelay.setObjectName(_fromUtf8("filtDelay"))
		self.filtDelay.valueChanged.connect(self.FiltDelay)
		
		self.horizontalLayout_3.addWidget(self.filtDelay)
		self.filtAttack = QtGui.QSlider(self.widget2)
		self.filtAttack.setMaximum(1024)
		self.filtAttack.setOrientation(QtCore.Qt.Vertical)
		self.filtAttack.setObjectName(_fromUtf8("filtAttack"))
		self.horizontalLayout_3.addWidget(self.filtAttack)
		self.filtAttack.valueChanged.connect(self.FiltAttack)
		
		self.filtDecay = QtGui.QSlider(self.widget2)
		self.filtDecay.setMaximum(1024)
		self.filtDecay.setOrientation(QtCore.Qt.Vertical)
		self.filtDecay.setObjectName(_fromUtf8("filtDecay"))
		self.filtDecay.valueChanged.connect(self.FiltDecay)
		
		self.horizontalLayout_3.addWidget(self.filtDecay)
		self.filtSustain = QtGui.QSlider(self.widget2)
		self.filtSustain.setMaximum(1024)
		self.filtSustain.setOrientation(QtCore.Qt.Vertical)
		self.filtSustain.setObjectName(_fromUtf8("filtSustain"))
		self.filtSustain.valueChanged.connect(self.FiltSustain)
		self.horizontalLayout_3.addWidget(self.filtSustain)
		
		self.filtRelease = QtGui.QSlider(self.widget2)
		self.filtRelease.setMaximum(1024)
		self.filtRelease.setOrientation(QtCore.Qt.Vertical)
		self.filtRelease.setObjectName(_fromUtf8("filtRelease"))
		self.horizontalLayout_3.addWidget(self.filtRelease)
		self.filtRelease.valueChanged.connect(self.FiltRelease)
		
		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label_2.setText(_translate("Dialog", "Res", None))
		self.label_3.setText(_translate("Dialog", "Key Amt", None))
		self.label.setText(_translate("Dialog", "Cutoff", None))
		self.label_4.setText(_translate("Dialog", "Audio Mod", None))
		self.filt4pole.setText(_translate("Dialog", "4 pole", None))
		self.label_5.setText(_translate("Dialog", "Env Amt", None))
		self.label_6.setText(_translate("Dialog", "Vel Amt", None))
		self.label_7.setText(_translate("Dialog", "DLY", None))
		self.label_8.setText(_translate("Dialog", "A", None))
		self.label_9.setText(_translate("Dialog", "D", None))
		self.label_10.setText(_translate("Dialog", "S", None))
		self.label_11.setText(_translate("Dialog", "R", None))

	def FiltDelay(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 22
		SendNRPN(nrpn,x,self.midi_channel)
		
	def FiltAttack(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 23
		SendNRPN(nrpn,x,self.midi_channel)
		
	def FiltDecay(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 24
		SendNRPN(nrpn,x,self.midi_channel)
	
	def FiltSustain(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 25
		SendNRPN(nrpn,x,self.midi_channel)
		
	def FiltRelease(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 26
		SendNRPN(nrpn,x,self.midi_channel)
		
	def Filt4Pole(self):
		x = self.filt4pole.isChecked()
		SendNRPN(19,x,self.midi_channel)
		
	def FiltKeyAmt(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 17
		SendNRPN(nrpn,x,self.midi_channel)
		
	def FiltEnvAmt(self,value):
		x = int(math.ceil((value+1024)/2048.0 * 254.0))
		nrpn = 20
		SendNRPN(nrpn,x,self.midi_channel)
		
	def FiltCutoff(self,value):
		x = int(math.ceil(value/1024.0 * 164.0))
		nrpn = 15
		SendNRPN(nrpn,x,self.midi_channel)
		
	def FiltRes(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 16
		SendNRPN(nrpn,x,self.midi_channel)
		
	def FiltAudioMod(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 18
		SendNRPN(nrpn,x,self.midi_channel)
		
	def FiltVelAmt(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 21
		SendNRPN(nrpn,x,self.midi_channel)
		