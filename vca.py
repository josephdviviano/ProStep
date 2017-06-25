# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vca.ui'
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

class Ui_VCADialog(object):
	def setupUi(self, Dialog):        
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(400, 300)
		
		self.vcaLvl = QtGui.QDial(Dialog)
		self.vcaLvl.setGeometry(QtCore.QRect(10, 20, 50, 64))
		self.vcaLvl.setMaximum(1024)
		self.vcaLvl.setObjectName(_fromUtf8("vcaLvl"))
		self.vcaLvl.valueChanged.connect(self.VcaLvl)
		
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(20, 90, 46, 13))
		self.label.setObjectName(_fromUtf8("label"))
		
		self.vcaEnvAmt = QtGui.QDial(Dialog)
		self.vcaEnvAmt.setGeometry(QtCore.QRect(70, 20, 50, 64))
		self.vcaEnvAmt.setMaximum(1024)
		self.vcaEnvAmt.setObjectName(_fromUtf8("vcaEnvAmt"))
		self.vcaEnvAmt.valueChanged.connect(self.VcaEnvAmt)
		
		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(80, 90, 46, 13))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.vcaVelAmt = QtGui.QDial(Dialog)
		self.vcaVelAmt.setGeometry(QtCore.QRect(10, 110, 50, 64))
		self.vcaVelAmt.setMaximum(1024)
		self.vcaVelAmt.setObjectName(_fromUtf8("vcaVelAmt"))
		self.vcaVelAmt.valueChanged.connect(self.VcaVelAmt)
		
		self.label_3 = QtGui.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(20, 190, 46, 13))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		
		self.vcaVolume = QtGui.QDial(Dialog)
		self.vcaVolume.setGeometry(QtCore.QRect(70, 110, 50, 64))
		self.vcaVolume.setMaximum(1024)
		self.vcaVolume.setObjectName(_fromUtf8("vcaVolume"))
		self.vcaVolume.valueChanged.connect(self.VcaVolume)
		
		self.label_4 = QtGui.QLabel(Dialog)
		self.label_4.setGeometry(QtCore.QRect(80, 190, 46, 13))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.label_5 = QtGui.QLabel(Dialog)
		self.label_5.setGeometry(QtCore.QRect(150, 270, 21, 16))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.label_6 = QtGui.QLabel(Dialog)
		self.label_6.setGeometry(QtCore.QRect(210, 270, 21, 16))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.label_7 = QtGui.QLabel(Dialog)
		self.label_7.setGeometry(QtCore.QRect(250, 270, 21, 20))
		self.label_7.setObjectName(_fromUtf8("label_7"))
		self.label_8 = QtGui.QLabel(Dialog)
		self.label_8.setGeometry(QtCore.QRect(300, 270, 21, 16))
		self.label_8.setObjectName(_fromUtf8("label_8"))
		self.label_9 = QtGui.QLabel(Dialog)
		self.label_9.setGeometry(QtCore.QRect(340, 270, 21, 16))
		self.label_9.setObjectName(_fromUtf8("label_9"))
		self.widget = QtGui.QWidget(Dialog)
		self.widget.setGeometry(QtCore.QRect(130, 9, 251, 251))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		
		self.vcaDelay = QtGui.QSlider(self.widget)
		self.vcaDelay.setMaximum(1024)
		self.vcaDelay.setOrientation(QtCore.Qt.Vertical)
		self.vcaDelay.setObjectName(_fromUtf8("vcaDelay"))
		self.vcaDelay.valueChanged.connect(self.VcaDelay)
		
		self.horizontalLayout.addWidget(self.vcaDelay)
		self.vcaAttack = QtGui.QSlider(self.widget)
		self.vcaAttack.setMaximum(1024)
		self.vcaAttack.setOrientation(QtCore.Qt.Vertical)
		self.vcaAttack.setObjectName(_fromUtf8("vcaAttack"))
		self.vcaAttack.valueChanged.connect(self.VcaAttack)
		
		self.horizontalLayout.addWidget(self.vcaAttack)
		self.vcaDecay = QtGui.QSlider(self.widget)
		self.vcaDecay.setMaximum(1024)
		self.vcaDecay.setOrientation(QtCore.Qt.Vertical)
		self.vcaDecay.setObjectName(_fromUtf8("vcaDecay"))
		self.vcaDecay.valueChanged.connect(self.VcaDecay)
		
		self.horizontalLayout.addWidget(self.vcaDecay)
		self.vcaSustain = QtGui.QSlider(self.widget)
		self.vcaSustain.setMaximum(1024)
		self.vcaSustain.setOrientation(QtCore.Qt.Vertical)
		self.vcaSustain.setObjectName(_fromUtf8("vcaSustain"))
		self.horizontalLayout.addWidget(self.vcaSustain)
		self.vcaSustain.valueChanged.connect(self.VcaSustain)
		
		self.vcaRelease = QtGui.QSlider(self.widget)
		self.vcaRelease.setMaximum(1024)
		self.vcaRelease.setOrientation(QtCore.Qt.Vertical)
		self.vcaRelease.setObjectName(_fromUtf8("vcaRelease"))
		self.horizontalLayout.addWidget(self.vcaRelease)
		self.vcaRelease.valueChanged.connect(self.VcaRelease)
		
		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label.setText(_translate("Dialog", "Level", None))
		self.label_2.setText(_translate("Dialog", "ENVAMT", None))
		self.label_3.setText(_translate("Dialog", "VELAMT", None))
		self.label_4.setText(_translate("Dialog", "Volume", None))
		self.label_5.setText(_translate("Dialog", "DLY", None))
		self.label_6.setText(_translate("Dialog", "A", None))
		self.label_7.setText(_translate("Dialog", "D", None))
		self.label_8.setText(_translate("Dialog", "S", None))
		self.label_9.setText(_translate("Dialog", "R", None))

	def VcaLvl(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 27
		SendNRPN(nrpn,x,self.midi_channel)
		
	def VcaEnvAmt(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 30
		SendNRPN(nrpn,x,self.midi_channel)
		
	def VcaVelAmt(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 31
		SendNRPN(nrpn,x,self.midi_channel)
		
	def VcaDelay(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 32
		SendNRPN(nrpn,x,self.midi_channel)
		
	def VcaAttack(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 33
		SendNRPN(nrpn,x,self.midi_channel)
		
	def VcaDecay(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 34
		SendNRPN(nrpn,x,self.midi_channel)
		
	def VcaSustain(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 35
		SendNRPN(nrpn,x,self.midi_channel)
		
	def VcaRelease(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 36
		SendNRPN(nrpn,x,self.midi_channel)
		
	def VcaVolume(self,value):
		x = int(math.ceil(value/1024.0 * 127.0))
		nrpn = 29
		SendNRPN(nrpn,x,self.midi_channel)
		