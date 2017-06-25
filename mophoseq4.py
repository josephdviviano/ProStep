# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mophoseq4.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mido.sockets import PortServer,connect
import math
import sys
from midi import *
from mopho import *
from patterns import *

PPQ_WHOLE=96
PLAY_LEN=4*PPQ_WHOLE
TX_DELAY=0.01

MIDI_CHANNEL=int(raw_input("Output Channel>> "))
MIDIKB_CHANNEL=int(raw_input("Input Channel>> "))


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

notes = {}
for i in range(0,125,2):
	n = (i/2) % 12
	s = name_notes[n]
	notes[i] = s + str(i / 24)
	notes[i+1] = s + str((i+1)/24) + 'o'
notes[126]="RST"
notes[127]="REST"

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Worker(QThread):
	
	def __init__(self,mainwindow,parent=None):
		QThread.__init__(self,parent)
		self.exiting = False
		self.mainwindow = mainwindow
		self.scene_len = PLAY_LEN
		self.ppq = 0
		self.input_buffer = [0]*16
		self.cur_step = 0
		
	def __del__(self):
		self.exiting = True
		self.wait()
		
	def run(self):
		print 'running'
		while not self.exiting:
			for msg in midi_input:
				key = msg.bytes()
				if(key[0] == 248):
					self.ppq = self.ppq+1
					if(self.ppq >= 24):
						self.ppq = 0
						self.emit(SIGNAL("UpdateUi()"))
				
				elif(key[0] >= 0x90 and key[0] <= 0x9F):
					
					if(key[0] == 0x90+self.mainwindow.midi_channel):
						value = int((key[1]/127.0)*1024.0)
						self.input_buffer[self.cur_step] = value
						self.mainwindow.scenes[self.mainwindow.cur_scene][self.cur_step] = value
						self.cur_step = self.cur_step + 1
						self.cur_step = self.cur_step % 16
						self.emit(SIGNAL("UpdateUi()"))
				
				"""
				if(key[0] == 248):
					self.ppq = self.ppq+1
					if(self.ppq >= self.scene_len):
						self.mainwindow.cur_scene = self.mainwindow.cur_scene+1
						self.mainwindow.cur_scene = self.mainwindow.cur_scene % self.mainwindow.total_scenes
						self.ppq = 0
						self.emit(SIGNAL("UpdateUi()"))
				"""
						
				midi_output.send(msg)

class Ui_Config(QWidget):

		def __init__(self,parent):
			super(Ui_Config,self).__init__()
			self.parent = parent
			self.initUI()
			
		def initUI(self):
			self.txt1 = QtLabel()
			self.txt1.setText("Seq1 Dest")
			self.txt1.move(20,20)
			
			self.cb1 = QtComboBox()
			self.cb1.move(50,20)
			self.cb1.addItem("Off")
			self.cb1.addItem("Osc1 Freq")
			self.cb1.addItem("Osc2 Freq")
			self.cb1.addItem("Osc all Freq")
			self.cb1.addItem("Osc mix")
			self.cb1.addItem("Noise Level")
			self.cb1.addItem("Osc1 PW")
			self.cb1.addItem("Osc2 PW")
			self.cb1.addItem("All PW")
			self.cb1.addItem("Cutoff")
			self.cb1.addItem("Resonance")
			self.cb1.addItem("Audio Mod")
			self.cb1.addItem("VCA Amt")
			self.cb1.addItem("Stereo Pan")
			self.cb1.addItem("LFO1 Freq")
			self.cb1.addItem("LFO2 Freq")
			self.cb1.addItem("LFO3 Freq")
			self.cb1.addItem("LFO4 Freq")
			self.cb1.addItem("All LFO Freq")
			self.cb1.addItem("LFO1 Amt")
			self.cb1.addItem("LFO2 Amt")
			self.cb1.addItem("LFO3 Amt")
			self.cb1.addItem("LFO4 Amt")
			self.cb1.addItem("All LFO Amt")
			self.cb1.addItem("Env1 Amt")
			self.cb1.addItem("Env2 Amt")
			self.cb1.addItem("Env3 Amt")
			self.cb1.addItem("All Env Amt")
			self.cb1.addItem("Env1 Attack")
			self.cb1.addItem("Env2 Attack")
			self.cb1.addItem("Env3 Attack")
			self.cb1.addItem("Env All Attack")
			self.cb1.addItem("Env1 Decay")
			self.cb1.addItem("Env2 Decay")
			self.cb1.addItem("Env3 Decay")
			self.cb1.addItem("Env All Decay")
			self.cb1.addItem("Env1 Release")
			self.cb1.addItem("Env2 Release")
			self.cb1.addItem("Env3 Release")
			self.cb1.addItem("All Env Release")
			self.cb1.addItem("Mod1 Amt")
			self.cb1.addItem("Mod2 Amt")
			self.cb1.addItem("Mod3 Amt")
			self.cb1.addItem("Mod4 Amt")
			self.cb1.addItem("Audio In")
			self.cb1.addItem("SubOsc1")
			self.cb1.addItem("SubOsc2")
			self.cb1.addItem("Seq Skew")
			
			
			self.txt2 = QLabel()
			self.txt2.setText("Measures per Scene")
			self.txt2.move(20,100)
			
class Ui_MainWindow(object):

	def __init__(self):
		self.midi_channel = MOPHO_CHANNEL
		self.scenes = [0]*256
		self.cur_scene = 0
		self.total_scenes = 1
		for i in range(256):
			self.scenes[i] = [0]*64
		self.RSTV = 1024
		self.RESTV = int((126.0/127.0)*1024) 
		self.copy_buffer = [0]*64
		
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(949, 704)
		self.centralwidget = QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.layoutWidget = QWidget(self.centralwidget)
		self.layoutWidget.setGeometry(QRect(480, 30, 451, 102))
		self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
		self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		
		self.updateThread = Worker(self)
		MOPHO_Sequencer(MOPHO_CHANNEL)
		MainWindow.connect(self.updateThread, SIGNAL("finished()"), self.UpdateUi)
		MainWindow.connect(self.updateThread, SIGNAL("terminated()"), self.UpdateUi)
		MainWindow.connect(self.updateThread, SIGNAL("UpdateUi()"), self.UpdateUi)
		self.updateThread.start()
		
		self.dials = [0]*65
		
		self.dial_9 = QDial(self.layoutWidget)
		self.dial_9.setMaximum(1024)
		self.dial_9.setObjectName(_fromUtf8("dial_9"))
		self.dial_9.valueChanged.connect(self.Knob9)
		self.dials[9] = self.dial_9
		
		self.horizontalLayout_2.addWidget(self.dial_9)
		self.dial_10 = QDial(self.layoutWidget)
		self.dial_10.setMaximum(1024)
		self.dial_10.setObjectName(_fromUtf8("dial_10"))
		self.dial_10.valueChanged.connect(self.Knob10)
		self.dials[10] = self.dial_10
		
		self.horizontalLayout_2.addWidget(self.dial_10)
		self.dial_11 = QDial(self.layoutWidget)
		self.dial_11.setMaximum(1024)
		self.dial_11.setObjectName(_fromUtf8("dial_11"))
		self.dial_11.valueChanged.connect(self.Knob11)
		self.dials[11] = self.dial_11
		
		self.horizontalLayout_2.addWidget(self.dial_11)
		self.dial_12 = QDial(self.layoutWidget)
		self.dial_12.setMaximum(1024)
		self.dial_12.setObjectName(_fromUtf8("dial_12"))
		self.dial_12.valueChanged.connect(self.Knob12)
		self.dials[12] = self.dial_12
		
		self.horizontalLayout_2.addWidget(self.dial_12)
		self.dial_13 = QDial(self.layoutWidget)
		self.dial_13.setMaximum(1024)
		self.dial_13.setObjectName(_fromUtf8("dial_13"))
		self.horizontalLayout_2.addWidget(self.dial_13)
		self.dial_13.valueChanged.connect(self.Knob13)
		self.dials[13] = self.dial_13
		
		self.dial_14 = QDial(self.layoutWidget)
		self.dial_14.setMaximum(1024)
		self.dial_14.setObjectName(_fromUtf8("dial_14"))
		self.dial_14.valueChanged.connect(self.Knob14)
		self.dials[14] = self.dial_14
		
		self.horizontalLayout_2.addWidget(self.dial_14)
		self.dial_15 = QDial(self.layoutWidget)
		self.dial_15.setMaximum(1024)
		self.dial_15.setObjectName(_fromUtf8("dial_15"))
		self.dial_15.valueChanged.connect(self.Knob15)
		self.dials[15] = self.dial_15
		
		self.horizontalLayout_2.addWidget(self.dial_15)
		self.dial_16 = QDial(self.layoutWidget)
		self.dial_16.setMaximum(1024)
		self.dial_16.setObjectName(_fromUtf8("dial_16"))
		self.dial_16.valueChanged.connect(self.Knob16)
		self.dials[16] = self.dial_16
		
		self.horizontalLayout_2.addWidget(self.dial_16)
		self.layoutWidget_2 = QWidget(self.centralwidget)
		self.layoutWidget_2.setGeometry(QRect(480, 140, 451, 45))
		self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
		
		self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget_2)
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
		
		self.pushButton_17 = QPushButton(self.layoutWidget_2)
		self.pushButton_17.setObjectName(_fromUtf8("pushButton_17"))
		self.pushButton_17.clicked.connect(self.RST9)
		
		self.horizontalLayout_5.addWidget(self.pushButton_17)
		self.pushButton_18 = QPushButton(self.layoutWidget_2)
		self.pushButton_18.setObjectName(_fromUtf8("pushButton_18"))
		self.pushButton_18.clicked.connect(self.RST10)
		
		self.horizontalLayout_5.addWidget(self.pushButton_18)
		self.pushButton_19 = QPushButton(self.layoutWidget_2)
		self.pushButton_19.setObjectName(_fromUtf8("pushButton_19"))
		self.pushButton_19.clicked.connect(self.RST11)
		
		self.horizontalLayout_5.addWidget(self.pushButton_19)
		self.pushButton_20 = QPushButton(self.layoutWidget_2)
		self.pushButton_20.setObjectName(_fromUtf8("pushButton_20"))
		self.pushButton_20.clicked.connect(self.RST12)
		
		self.horizontalLayout_5.addWidget(self.pushButton_20)
		self.pushButton_21 = QPushButton(self.layoutWidget_2)
		self.pushButton_21.setObjectName(_fromUtf8("pushButton_21"))
		self.pushButton_21.clicked.connect(self.RST13)
		
		self.horizontalLayout_5.addWidget(self.pushButton_21)
		
		self.pushButton_22 = QPushButton(self.layoutWidget_2)
		self.pushButton_22.setObjectName(_fromUtf8("pushButton_22"))
		self.pushButton_22.clicked.connect(self.RST14)
		
		self.horizontalLayout_5.addWidget(self.pushButton_22)
		
		self.pushButton_23 = QPushButton(self.layoutWidget_2)
		self.pushButton_23.setObjectName(_fromUtf8("pushButton_23"))
		self.pushButton_23.clicked.connect(self.RST15)
		
		self.horizontalLayout_5.addWidget(self.pushButton_23)
		
		self.pushButton_24 = QPushButton(self.layoutWidget_2)
		self.pushButton_24.setObjectName(_fromUtf8("pushButton_24"))
		self.pushButton_24.clicked.connect(self.RST16)
		
		self.horizontalLayout_5.addWidget(self.pushButton_24)
		
		self.layoutWidget_3 = QWidget(self.centralwidget)
		self.layoutWidget_3.setGeometry(QRect(480, 170, 451, 45))
		self.layoutWidget_3.setObjectName(_fromUtf8("layoutWidget_3"))
		self.horizontalLayout_6 = QHBoxLayout(self.layoutWidget_3)
		self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
		
		self.pushButton_25 = QPushButton(self.layoutWidget_3)
		self.pushButton_25.setObjectName(_fromUtf8("pushButton_25"))
		self.horizontalLayout_6.addWidget(self.pushButton_25)
		self.pushButton_25.clicked.connect(self.RESET9)
		
		self.pushButton_26 = QPushButton(self.layoutWidget_3)
		self.pushButton_26.setObjectName(_fromUtf8("pushButton_26"))
		self.horizontalLayout_6.addWidget(self.pushButton_26)
		self.pushButton_26.clicked.connect(self.RESET10)
		
		self.pushButton_27 = QPushButton(self.layoutWidget_3)
		self.pushButton_27.setObjectName(_fromUtf8("pushButton_27"))
		self.horizontalLayout_6.addWidget(self.pushButton_27)
		self.pushButton_27.clicked.connect(self.RESET11)
		
		self.pushButton_28 = QPushButton(self.layoutWidget_3)
		self.pushButton_28.setObjectName(_fromUtf8("pushButton_28"))
		self.horizontalLayout_6.addWidget(self.pushButton_28)
		self.pushButton_28.clicked.connect(self.RESET12)
		
		self.pushButton_29 = QPushButton(self.layoutWidget_3)
		self.pushButton_29.setObjectName(_fromUtf8("pushButton_29"))
		self.horizontalLayout_6.addWidget(self.pushButton_29)
		self.pushButton_29.clicked.connect(self.RESET13)
		
		self.pushButton_30 = QPushButton(self.layoutWidget_3)
		self.pushButton_30.setObjectName(_fromUtf8("pushButton_30"))
		self.horizontalLayout_6.addWidget(self.pushButton_30)
		self.pushButton_30.clicked.connect(self.RESET14)
		
		self.pushButton_31 = QPushButton(self.layoutWidget_3)
		self.pushButton_31.setObjectName(_fromUtf8("pushButton_31"))
		self.pushButton_31.clicked.connect(self.RESET15)
		
		self.horizontalLayout_6.addWidget(self.pushButton_31)
		self.pushButton_32 = QPushButton(self.layoutWidget_3)
		self.pushButton_32.setObjectName(_fromUtf8("pushButton_32"))
		self.pushButton_32.clicked.connect(self.RESET16)
		
		self.horizontalLayout_6.addWidget(self.pushButton_32)
		self.layoutWidget_4 = QWidget(self.centralwidget)
		self.layoutWidget_4.setGeometry(QRect(30, 200, 451, 102))
		self.layoutWidget_4.setObjectName(_fromUtf8("layoutWidget_4"))
		self.horizontalLayout_7 = QHBoxLayout(self.layoutWidget_4)
		self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
		self.dial_17 = QDial(self.layoutWidget_4)
		self.dial_17.setMaximum(1024)
		self.dial_17.setObjectName(_fromUtf8("dial_17"))
		self.dial_17.valueChanged.connect(self.Knob21)
		self.dials[17] = self.dial_17
		
		self.horizontalLayout_7.addWidget(self.dial_17)
		self.dial_18 = QDial(self.layoutWidget_4)
		self.dial_18.setMaximum(1024)
		self.dial_18.valueChanged.connect(self.Knob22)
		self.dials[18] = self.dial_18
		
		self.dial_18.setObjectName(_fromUtf8("dial_18"))
		self.horizontalLayout_7.addWidget(self.dial_18)
		self.dial_19 = QDial(self.layoutWidget_4)
		self.dial_19.setMaximum(1024)
		self.dial_19.setObjectName(_fromUtf8("dial_19"))
		self.dial_19.valueChanged.connect(self.Knob23)
		self.dials[19] = self.dial_19
		
		self.horizontalLayout_7.addWidget(self.dial_19)
		self.dial_20 = QDial(self.layoutWidget_4)
		self.dial_20.setMaximum(1024)
		self.dial_20.setObjectName(_fromUtf8("dial_20"))
		self.dial_20.valueChanged.connect(self.Knob24)
		self.dials[20] = self.dial_20
		
		self.horizontalLayout_7.addWidget(self.dial_20)
		self.dial_21 = QDial(self.layoutWidget_4)
		self.dial_21.setMaximum(1024)
		self.dial_21.valueChanged.connect(self.Knob25)
		self.dials[21] = self.dial_21		
		self.dial_21.setObjectName(_fromUtf8("dial_21"))
		
		self.horizontalLayout_7.addWidget(self.dial_21)
		self.dial_22 = QDial(self.layoutWidget_4)		
		self.dial_22.setMaximum(1024)
		self.dial_22.setObjectName(_fromUtf8("dial_22"))
		self.horizontalLayout_7.addWidget(self.dial_22)
		self.dial_22.valueChanged.connect(self.Knob26)
		self.dials[22] = self.dial_22
		
		self.dial_23 = QDial(self.layoutWidget_4)
		self.dial_23.setMaximum(1024)
		self.dial_23.setObjectName(_fromUtf8("dial_23"))
		self.dial_23.valueChanged.connect(self.Knob27)
		self.dials[23] = self.dial_23
		
		self.horizontalLayout_7.addWidget(self.dial_23)
		self.dial_24 = QDial(self.layoutWidget_4)
		self.dial_24.setMaximum(1024)
		self.dial_24.setObjectName(_fromUtf8("dial_24"))
		self.dial_24.valueChanged.connect(self.Knob28)
		self.dials[24] = self.dial_24
		
		self.horizontalLayout_7.addWidget(self.dial_24)
		self.layoutWidget_5 = QWidget(self.centralwidget)
		self.layoutWidget_5.setGeometry(QRect(480, 200, 451, 102))
		self.layoutWidget_5.setObjectName(_fromUtf8("layoutWidget_5"))
		self.horizontalLayout_8 = QHBoxLayout(self.layoutWidget_5)
		self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
		
		self.dial_25 = QDial(self.layoutWidget_5)
		self.dial_25.setMaximum(1024)
		self.dial_25.setObjectName(_fromUtf8("dial_25"))
		self.dial_25.valueChanged.connect(self.Knob29)
		self.dials[25] = self.dial_25
		
		self.horizontalLayout_8.addWidget(self.dial_25)
		self.dial_26 = QDial(self.layoutWidget_5)
		self.dial_26.setMaximum(1024)
		self.dial_26.valueChanged.connect(self.Knob210)
		self.dials[26] = self.dial_26
		
		self.dial_26.setObjectName(_fromUtf8("dial_26"))
		self.horizontalLayout_8.addWidget(self.dial_26)
		self.dial_27 = QDial(self.layoutWidget_5)
		self.dial_27.setMaximum(1024)
		self.dial_27.valueChanged.connect(self.Knob211)
		self.dials[27] = self.dial_27
		
		self.dial_27.setObjectName(_fromUtf8("dial_27"))
		self.horizontalLayout_8.addWidget(self.dial_27)
		self.dial_28 = QDial(self.layoutWidget_5)
		self.dial_28.setMaximum(1024)
		self.dial_28.setObjectName(_fromUtf8("dial_28"))
		self.dial_28.valueChanged.connect(self.Knob212)
		self.dials[28] = self.dial_28
		
		self.horizontalLayout_8.addWidget(self.dial_28)
		self.dial_29 = QDial(self.layoutWidget_5)
		self.dial_29.setMaximum(1024)
		self.dial_29.setObjectName(_fromUtf8("dial_29"))
		self.dial_29.valueChanged.connect(self.Knob213)
		self.dials[29] = self.dial_29
		
		self.horizontalLayout_8.addWidget(self.dial_29)
		self.dial_30 = QDial(self.layoutWidget_5)
		self.dial_30.setMaximum(1024)
		self.dial_30.setObjectName(_fromUtf8("dial_30"))
		self.dial_30.valueChanged.connect(self.Knob214)
		self.dials[30] = self.dial_30
		
		self.horizontalLayout_8.addWidget(self.dial_30)
		self.dial_31 = QDial(self.layoutWidget_5)
		self.dial_31.setMaximum(1024)
		self.dial_31.setObjectName(_fromUtf8("dial_31"))
		self.dial_31.valueChanged.connect(self.Knob215)
		self.dials[31] = self.dial_31
		
		self.horizontalLayout_8.addWidget(self.dial_31)
		self.dial_32 = QDial(self.layoutWidget_5)
		self.dial_32.setMaximum(1024)
		self.dial_32.setObjectName(_fromUtf8("dial_32"))
		self.dial_32.valueChanged.connect(self.Knob216)
		self.dials[32] = self.dial_32
		
		self.horizontalLayout_8.addWidget(self.dial_32)
		
		self.layoutWidget_6 = QWidget(self.centralwidget)
		self.layoutWidget_6.setGeometry(QRect(30, 310, 451, 45))
		self.layoutWidget_6.setObjectName(_fromUtf8("layoutWidget_6"))
		self.horizontalLayout_9 = QHBoxLayout(self.layoutWidget_6)
		self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
		self.pushButton_33 = QPushButton(self.layoutWidget_6)
		self.pushButton_33.setObjectName(_fromUtf8("pushButton_33"))
		self.pushButton_33.clicked.connect(self.RST21)
		
		self.horizontalLayout_9.addWidget(self.pushButton_33)
		self.pushButton_34 = QPushButton(self.layoutWidget_6)
		self.pushButton_34.clicked.connect(self.RST22)
		self.pushButton_34.setObjectName(_fromUtf8("pushButton_34"))
		self.horizontalLayout_9.addWidget(self.pushButton_34)
		self.pushButton_35 = QPushButton(self.layoutWidget_6)
		self.pushButton_35.clicked.connect(self.RST23)
		self.pushButton_35.setObjectName(_fromUtf8("pushButton_35"))
		self.horizontalLayout_9.addWidget(self.pushButton_35)
		self.pushButton_36 = QPushButton(self.layoutWidget_6)
		self.pushButton_36.setObjectName(_fromUtf8("pushButton_36"))
		self.pushButton_36.clicked.connect(self.RST24)
		self.horizontalLayout_9.addWidget(self.pushButton_36)
		self.pushButton_37 = QPushButton(self.layoutWidget_6)
		self.pushButton_37.setObjectName(_fromUtf8("pushButton_37"))
		self.pushButton_37.clicked.connect(self.RST25)
		self.horizontalLayout_9.addWidget(self.pushButton_37)
		self.pushButton_38 = QPushButton(self.layoutWidget_6)
		self.pushButton_38.setObjectName(_fromUtf8("pushButton_38"))
		self.pushButton_38.clicked.connect(self.RST26)
		self.horizontalLayout_9.addWidget(self.pushButton_38)
		self.pushButton_39 = QPushButton(self.layoutWidget_6)
		self.pushButton_39.setObjectName(_fromUtf8("pushButton_39"))
		self.pushButton_39.clicked.connect(self.RST27)
		self.horizontalLayout_9.addWidget(self.pushButton_39)
		self.pushButton_40 = QPushButton(self.layoutWidget_6)
		self.pushButton_40.setObjectName(_fromUtf8("pushButton_40"))
		self.pushButton_40.clicked.connect(self.RST28)
		self.horizontalLayout_9.addWidget(self.pushButton_40)
		self.layoutWidget_7 = QWidget(self.centralwidget)
		
		self.layoutWidget_7.setGeometry(QRect(480, 310, 451, 45))
		self.layoutWidget_7.setObjectName(_fromUtf8("layoutWidget_7"))
		self.horizontalLayout_10 = QHBoxLayout(self.layoutWidget_7)
		self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
		self.pushButton_41 = QPushButton(self.layoutWidget_7)
		self.pushButton_41.setObjectName(_fromUtf8("pushButton_41"))
		self.pushButton_41.clicked.connect(self.RST29)
		self.horizontalLayout_10.addWidget(self.pushButton_41)
		self.pushButton_42 = QPushButton(self.layoutWidget_7)
		self.pushButton_42.setObjectName(_fromUtf8("pushButton_42"))
		self.pushButton_42.clicked.connect(self.RST210)
		self.horizontalLayout_10.addWidget(self.pushButton_42)
		self.pushButton_43 = QPushButton(self.layoutWidget_7)
		self.pushButton_43.setObjectName(_fromUtf8("pushButton_43"))
		self.pushButton_43.clicked.connect(self.RST211)
		self.horizontalLayout_10.addWidget(self.pushButton_43)
		self.pushButton_44 = QPushButton(self.layoutWidget_7)
		self.pushButton_44.clicked.connect(self.RST212)
		self.pushButton_44.setObjectName(_fromUtf8("pushButton_44"))
		self.horizontalLayout_10.addWidget(self.pushButton_44)
		self.pushButton_45 = QPushButton(self.layoutWidget_7)
		self.pushButton_45.setObjectName(_fromUtf8("pushButton_45"))
		self.pushButton_45.clicked.connect(self.RST213)
		self.horizontalLayout_10.addWidget(self.pushButton_45)
		self.pushButton_46 = QPushButton(self.layoutWidget_7)
		self.pushButton_46.setObjectName(_fromUtf8("pushButton_46"))
		self.pushButton_46.clicked.connect(self.RST214)
		self.horizontalLayout_10.addWidget(self.pushButton_46)
		self.pushButton_47 = QPushButton(self.layoutWidget_7)
		self.pushButton_47.setObjectName(_fromUtf8("pushButton_47"))
		self.pushButton_47.clicked.connect(self.RST215)
		self.horizontalLayout_10.addWidget(self.pushButton_47)
		self.pushButton_48 = QPushButton(self.layoutWidget_7)
		self.pushButton_48.setObjectName(_fromUtf8("pushButton_48"))
		self.pushButton_48.clicked.connect(self.RST216)
		self.horizontalLayout_10.addWidget(self.pushButton_48)
		
		self.layoutWidget_8 = QWidget(self.centralwidget)
		self.layoutWidget_8.setGeometry(QRect(30, 460, 451, 45))
		self.layoutWidget_8.setObjectName(_fromUtf8("layoutWidget_8"))
		self.horizontalLayout_11 = QHBoxLayout(self.layoutWidget_8)
		self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
		self.pushButton_49 = QPushButton(self.layoutWidget_8)
		self.pushButton_49.setObjectName(_fromUtf8("pushButton_49"))
		self.pushButton_49.clicked.connect(self.RST31)
		self.horizontalLayout_11.addWidget(self.pushButton_49)
		self.pushButton_50 = QPushButton(self.layoutWidget_8)
		self.pushButton_50.setObjectName(_fromUtf8("pushButton_50"))
		self.pushButton_50.clicked.connect(self.RST32)
		self.horizontalLayout_11.addWidget(self.pushButton_50)
		self.pushButton_51 = QPushButton(self.layoutWidget_8)
		self.pushButton_51.setObjectName(_fromUtf8("pushButton_51"))
		self.pushButton_51.clicked.connect(self.RST33)
		self.horizontalLayout_11.addWidget(self.pushButton_51)
		self.pushButton_52 = QPushButton(self.layoutWidget_8)
		self.pushButton_52.setObjectName(_fromUtf8("pushButton_52"))
		self.pushButton_52.clicked.connect(self.RST34)
		self.horizontalLayout_11.addWidget(self.pushButton_52)
		self.pushButton_53 = QPushButton(self.layoutWidget_8)
		self.pushButton_53.setObjectName(_fromUtf8("pushButton_53"))
		self.pushButton_53.clicked.connect(self.RST35)
		self.horizontalLayout_11.addWidget(self.pushButton_53)
		self.pushButton_54 = QPushButton(self.layoutWidget_8)
		self.pushButton_54.setObjectName(_fromUtf8("pushButton_54"))
		self.pushButton_54.clicked.connect(self.RST36)
		self.horizontalLayout_11.addWidget(self.pushButton_54)
		self.pushButton_55 = QPushButton(self.layoutWidget_8)
		self.pushButton_55.setObjectName(_fromUtf8("pushButton_55"))
		self.pushButton_55.clicked.connect(self.RST37)
		self.horizontalLayout_11.addWidget(self.pushButton_55)
		self.pushButton_56 = QPushButton(self.layoutWidget_8)
		self.pushButton_56.setObjectName(_fromUtf8("pushButton_56"))
		self.pushButton_56.clicked.connect(self.RST38)
		self.horizontalLayout_11.addWidget(self.pushButton_56)
		self.layoutWidget_9 = QWidget(self.centralwidget)
		
		self.layoutWidget_9.setGeometry(QRect(480, 350, 451, 102))
		self.layoutWidget_9.setObjectName(_fromUtf8("layoutWidget_9"))
		self.horizontalLayout_12 = QHBoxLayout(self.layoutWidget_9)
		self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
		self.dial_33 = QDial(self.layoutWidget_9)
		self.dial_33.setMaximum(1024)
		self.dial_33.setObjectName(_fromUtf8("dial_33"))
		self.dial_33.valueChanged.connect(self.Knob39)
		self.dials[41] = self.dial_33
		
		self.horizontalLayout_12.addWidget(self.dial_33)
		self.dial_34 = QDial(self.layoutWidget_9)
		self.dial_34.setMaximum(1024)
		self.dial_34.setObjectName(_fromUtf8("dial_34"))
		self.dial_34.valueChanged.connect(self.Knob310)
		self.dials[42] = self.dial_34
		
		self.horizontalLayout_12.addWidget(self.dial_34)
		self.dial_35 = QDial(self.layoutWidget_9)
		self.dial_35.setMaximum(1024)
		self.dial_35.setObjectName(_fromUtf8("dial_35"))
		self.dial_35.valueChanged.connect(self.Knob311)
		self.dials[43] = self.dial_35
		
		self.horizontalLayout_12.addWidget(self.dial_35)
		self.dial_36 = QDial(self.layoutWidget_9)
		self.dial_36.setMaximum(1024)
		self.dial_36.valueChanged.connect(self.Knob312)
		self.dials[44] = self.dial_36
		
		self.dial_36.setObjectName(_fromUtf8("dial_36"))
		self.horizontalLayout_12.addWidget(self.dial_36)
		self.dial_37 = QDial(self.layoutWidget_9)
		self.dial_37.setMaximum(1024)
		self.dial_37.setObjectName(_fromUtf8("dial_37"))
		self.dial_37.valueChanged.connect(self.Knob313)
		self.dials[45] = self.dial_37
		
		self.horizontalLayout_12.addWidget(self.dial_37)
		self.dial_38 = QDial(self.layoutWidget_9)
		self.dial_38.setMaximum(1024)
		self.dial_38.setObjectName(_fromUtf8("dial_38"))
		self.dial_38.valueChanged.connect(self.Knob314)
		self.dials[46] = self.dial_38
		
		self.horizontalLayout_12.addWidget(self.dial_38)
		self.dial_39 = QDial(self.layoutWidget_9)
		self.dial_39.setMaximum(1024)
		self.dial_39.setObjectName(_fromUtf8("dial_39"))
		self.dial_39.valueChanged.connect(self.Knob315)
		self.dials[47] = self.dial_39
		
		self.horizontalLayout_12.addWidget(self.dial_39)
		self.dial_40 = QDial(self.layoutWidget_9)
		self.dial_40.setMaximum(1024)
		self.dial_40.setObjectName(_fromUtf8("dial_40"))
		self.dial_40.valueChanged.connect(self.Knob316)
		self.dials[48] = self.dial_40
		
		self.horizontalLayout_12.addWidget(self.dial_40)
		self.layoutWidget_10 = QWidget(self.centralwidget)
		
		self.layoutWidget_10.setGeometry(QRect(30, 350, 451, 102))
		self.layoutWidget_10.setObjectName(_fromUtf8("layoutWidget_10"))
		self.horizontalLayout_13 = QHBoxLayout(self.layoutWidget_10)
		self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
		self.dial_41 = QDial(self.layoutWidget_10)
		self.dial_41.setMaximum(1024)
		self.dial_41.setObjectName(_fromUtf8("dial_41"))
		self.dial_41.valueChanged.connect(self.Knob31)
		self.dials[33] = self.dial_41
		
		self.horizontalLayout_13.addWidget(self.dial_41)
		self.dial_42 = QDial(self.layoutWidget_10)
		self.dial_42.setMaximum(1024)
		self.dial_42.valueChanged.connect(self.Knob32)
		self.dials[34] = self.dial_42
		
		self.dial_42.setObjectName(_fromUtf8("dial_42"))
		self.horizontalLayout_13.addWidget(self.dial_42)
		self.dial_43 = QDial(self.layoutWidget_10)
		self.dial_43.setMaximum(1024)
		self.dial_43.valueChanged.connect(self.Knob33)
		self.dials[35] = self.dial_43
		
		self.dial_43.setObjectName(_fromUtf8("dial_43"))
		self.horizontalLayout_13.addWidget(self.dial_43)
		self.dial_44 = QDial(self.layoutWidget_10)
		self.dial_44.setMaximum(1024)
		self.dial_44.valueChanged.connect(self.Knob34)
		self.dials[36] = self.dial_44
		
		self.dial_44.setObjectName(_fromUtf8("dial_44"))
		self.horizontalLayout_13.addWidget(self.dial_44)
		self.dial_45 = QDial(self.layoutWidget_10)
		self.dial_45.setMaximum(1024)
		self.dial_45.valueChanged.connect(self.Knob35)
		self.dials[37] = self.dial_45
		
		self.dial_45.setObjectName(_fromUtf8("dial_45"))
		self.horizontalLayout_13.addWidget(self.dial_45)
		self.dial_46 = QDial(self.layoutWidget_10)
		self.dial_46.setMaximum(1024)
		self.dial_46.setObjectName(_fromUtf8("dial_46"))
		self.dial_46.valueChanged.connect(self.Knob36)
		self.dials[38] = self.dial_46
		
		self.horizontalLayout_13.addWidget(self.dial_46)
		self.dial_47 = QDial(self.layoutWidget_10)
		self.dial_47.setMaximum(1024)
		self.dial_47.valueChanged.connect(self.Knob37)
		self.dial_47.setObjectName(_fromUtf8("dial_47"))
		self.dials[39] = self.dial_47
		
		
		self.horizontalLayout_13.addWidget(self.dial_47)
		self.dial_48 = QDial(self.layoutWidget_10)
		self.dial_48.setMaximum(1024)
		self.dial_48.valueChanged.connect(self.Knob38)
		self.dial_48.setObjectName(_fromUtf8("dial_48"))
		self.dials[40] = self.dial_48
		
		self.horizontalLayout_13.addWidget(self.dial_48)
		self.layoutWidget_11 = QWidget(self.centralwidget)
		
		self.layoutWidget_11.setGeometry(QRect(480, 460, 451, 45))
		self.layoutWidget_11.setObjectName(_fromUtf8("layoutWidget_11"))
		self.horizontalLayout_14 = QHBoxLayout(self.layoutWidget_11)
		self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
		self.pushButton_57 = QPushButton(self.layoutWidget_11)
		self.pushButton_57.setObjectName(_fromUtf8("pushButton_57"))
		self.pushButton_57.clicked.connect(self.RST39)
		
		self.horizontalLayout_14.addWidget(self.pushButton_57)
		self.pushButton_58 = QPushButton(self.layoutWidget_11)
		self.pushButton_58.setObjectName(_fromUtf8("pushButton_58"))
		self.pushButton_58.clicked.connect(self.RST310)
		
		self.horizontalLayout_14.addWidget(self.pushButton_58)
		self.pushButton_59 = QPushButton(self.layoutWidget_11)
		self.pushButton_59.setObjectName(_fromUtf8("pushButton_59"))
		self.pushButton_59.clicked.connect(self.RST311)
		
		self.horizontalLayout_14.addWidget(self.pushButton_59)
		self.pushButton_60 = QPushButton(self.layoutWidget_11)
		self.pushButton_60.setObjectName(_fromUtf8("pushButton_60"))
		self.pushButton_60.clicked.connect(self.RST312)
		
		self.horizontalLayout_14.addWidget(self.pushButton_60)
		self.pushButton_61 = QPushButton(self.layoutWidget_11)
		self.pushButton_61.setObjectName(_fromUtf8("pushButton_61"))
		self.pushButton_61.clicked.connect(self.RST313)
		
		self.horizontalLayout_14.addWidget(self.pushButton_61)
		self.pushButton_62 = QPushButton(self.layoutWidget_11)
		self.pushButton_62.setObjectName(_fromUtf8("pushButton_62"))
		self.pushButton_62.clicked.connect(self.RST314)
		
		self.horizontalLayout_14.addWidget(self.pushButton_62)
		self.pushButton_63 = QPushButton(self.layoutWidget_11)
		self.pushButton_63.setObjectName(_fromUtf8("pushButton_63"))
		self.pushButton_63.clicked.connect(self.RST315)
		
		self.horizontalLayout_14.addWidget(self.pushButton_63)
		self.pushButton_64 = QPushButton(self.layoutWidget_11)
		self.pushButton_64.setObjectName(_fromUtf8("pushButton_64"))
		self.pushButton_64.clicked.connect(self.RST316)
		
		self.horizontalLayout_14.addWidget(self.pushButton_64)
		self.layoutWidget_12 = QWidget(self.centralwidget)
		
		self.layoutWidget_12.setGeometry(QRect(30, 600, 451, 45))
		self.layoutWidget_12.setObjectName(_fromUtf8("layoutWidget_12"))
		self.horizontalLayout_15 = QHBoxLayout(self.layoutWidget_12)
		self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
		self.pushButton_65 = QPushButton(self.layoutWidget_12)
		self.pushButton_65.setObjectName(_fromUtf8("pushButton_65"))
		self.pushButton_65.clicked.connect(self.RST41)
		
		self.horizontalLayout_15.addWidget(self.pushButton_65)
		self.pushButton_66 = QPushButton(self.layoutWidget_12)
		self.pushButton_66.setObjectName(_fromUtf8("pushButton_66"))
		self.pushButton_66.clicked.connect(self.RST42)
		
		self.horizontalLayout_15.addWidget(self.pushButton_66)
		self.pushButton_67 = QPushButton(self.layoutWidget_12)
		self.pushButton_67.setObjectName(_fromUtf8("pushButton_67"))
		self.pushButton_67.clicked.connect(self.RST43)
		
		self.horizontalLayout_15.addWidget(self.pushButton_67)
		self.pushButton_68 = QPushButton(self.layoutWidget_12)
		self.pushButton_68.setObjectName(_fromUtf8("pushButton_68"))
		self.pushButton_68.clicked.connect(self.RST44)
		
		self.horizontalLayout_15.addWidget(self.pushButton_68)
		self.pushButton_69 = QPushButton(self.layoutWidget_12)
		self.pushButton_69.setObjectName(_fromUtf8("pushButton_69"))
		self.pushButton_69.clicked.connect(self.RST45)
		
		self.horizontalLayout_15.addWidget(self.pushButton_69)
		self.pushButton_70 = QPushButton(self.layoutWidget_12)
		self.pushButton_70.setObjectName(_fromUtf8("pushButton_70"))
		self.pushButton_70.clicked.connect(self.RST46)
		
		self.horizontalLayout_15.addWidget(self.pushButton_70)
		self.pushButton_71 = QPushButton(self.layoutWidget_12)
		self.pushButton_71.setObjectName(_fromUtf8("pushButton_71"))
		self.pushButton_71.clicked.connect(self.RST47)
		
		self.horizontalLayout_15.addWidget(self.pushButton_71)
		self.pushButton_72 = QPushButton(self.layoutWidget_12)
		self.pushButton_72.setObjectName(_fromUtf8("pushButton_72"))
		self.pushButton_72.clicked.connect(self.RST48)
		
		self.horizontalLayout_15.addWidget(self.pushButton_72)
		self.layoutWidget_13 = QWidget(self.centralwidget)
		
		self.layoutWidget_13.setGeometry(QRect(480, 490, 451, 102))
		self.layoutWidget_13.setObjectName(_fromUtf8("layoutWidget_13"))
		self.horizontalLayout_16 = QHBoxLayout(self.layoutWidget_13)
		self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
		self.dial_49 = QDial(self.layoutWidget_13)
		self.dial_49.setMaximum(1024)
		self.dial_49.setObjectName(_fromUtf8("dial_49"))
		self.dial_49.valueChanged.connect(self.Knob49)
		self.dials[57] = self.dial_49
		
		self.horizontalLayout_16.addWidget(self.dial_49)
		self.dial_50 = QDial(self.layoutWidget_13)
		self.dial_50.setMaximum(1024)
		self.dial_50.valueChanged.connect(self.Knob410)
		self.dials[58] = self.dial_50
		
		self.dial_50.setObjectName(_fromUtf8("dial_50"))
		self.horizontalLayout_16.addWidget(self.dial_50)
		self.dial_51 = QDial(self.layoutWidget_13)
		self.dial_51.setMaximum(1024)
		self.dial_51.valueChanged.connect(self.Knob411)
		self.dials[59] = self.dial_51
		
		self.dial_51.setObjectName(_fromUtf8("dial_51"))
		self.horizontalLayout_16.addWidget(self.dial_51)
		self.dial_52 = QDial(self.layoutWidget_13)
		self.dial_52.setMaximum(1024)
		self.dial_52.valueChanged.connect(self.Knob412)
		self.dials[60] = self.dial_52
		
		self.dial_52.setObjectName(_fromUtf8("dial_52"))
		self.horizontalLayout_16.addWidget(self.dial_52)
		self.dial_53 = QDial(self.layoutWidget_13)
		self.dial_53.setMaximum(1024)
		self.dial_53.setObjectName(_fromUtf8("dial_53"))
		self.dial_53.valueChanged.connect(self.Knob413)
		self.dials[61] = self.dial_53
		
		self.horizontalLayout_16.addWidget(self.dial_53)
		self.dial_54 = QDial(self.layoutWidget_13)
		self.dial_54.setMaximum(1024)
		self.dial_54.setObjectName(_fromUtf8("dial_54"))
		self.dial_54.valueChanged.connect(self.Knob414)
		self.dials[62] = self.dial_54
		
		self.horizontalLayout_16.addWidget(self.dial_54)
		self.dial_55 = QDial(self.layoutWidget_13)
		self.dial_55.setMaximum(1024)
		self.dial_55.setObjectName(_fromUtf8("dial_55"))
		self.dial_55.valueChanged.connect(self.Knob415)
		self.dials[63] = self.dial_55
		
		self.horizontalLayout_16.addWidget(self.dial_55)
		self.dial_56 = QDial(self.layoutWidget_13)
		self.dial_56.setMaximum(1024)
		self.dial_56.setObjectName(_fromUtf8("dial_56"))
		self.dial_56.valueChanged.connect(self.Knob416)
		self.dials[64] = self.dial_56
		
		self.horizontalLayout_16.addWidget(self.dial_56)
		
		self.layoutWidget_14 = QWidget(self.centralwidget)
		self.layoutWidget_14.setGeometry(QRect(30, 490, 451, 102))
		self.layoutWidget_14.setObjectName(_fromUtf8("layoutWidget_14"))
		self.horizontalLayout_17 = QHBoxLayout(self.layoutWidget_14)
		self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
		self.dial_57 = QDial(self.layoutWidget_14)
		self.dial_57.setMaximum(1024)
		self.dial_57.setObjectName(_fromUtf8("dial_57"))
		self.dial_57.valueChanged.connect(self.Knob41)
		self.dials[49] = self.dial_57
		
		self.horizontalLayout_17.addWidget(self.dial_57)
		self.dial_58 = QDial(self.layoutWidget_14)
		self.dial_58.setMaximum(1024)
		self.dial_58.valueChanged.connect(self.Knob42)
		self.dials[50] = self.dial_58
		
		self.dial_58.setObjectName(_fromUtf8("dial_58"))
		self.horizontalLayout_17.addWidget(self.dial_58)
		self.dial_59 = QDial(self.layoutWidget_14)
		self.dial_59.setMaximum(1024)
		self.dial_59.setObjectName(_fromUtf8("dial_59"))
		self.dial_59.valueChanged.connect(self.Knob43)
		self.dials[51] = self.dial_59
		
		self.horizontalLayout_17.addWidget(self.dial_59)
		self.dial_60 = QDial(self.layoutWidget_14)
		self.dial_60.setMaximum(1024)
		self.dial_60.setObjectName(_fromUtf8("dial_60"))
		self.dial_60.valueChanged.connect(self.Knob44)
		self.dials[52] = self.dial_60
		
		self.horizontalLayout_17.addWidget(self.dial_60)
		self.dial_61 = QDial(self.layoutWidget_14)
		self.dial_61.setMaximum(1024)
		self.dial_61.setObjectName(_fromUtf8("dial_61"))
		self.dial_61.valueChanged.connect(self.Knob45)
		self.dials[53] = self.dial_61
		
		self.horizontalLayout_17.addWidget(self.dial_61)
		self.dial_62 = QDial(self.layoutWidget_14)
		self.dial_62.setMaximum(1024)
		self.dial_62.setObjectName(_fromUtf8("dial_62"))
		self.dial_62.valueChanged.connect(self.Knob46)
		self.dials[54] = self.dial_62
		
		self.horizontalLayout_17.addWidget(self.dial_62)
		self.dial_63 = QDial(self.layoutWidget_14)
		self.dial_63.setMaximum(1024)
		self.dial_63.setObjectName(_fromUtf8("dial_63"))
		self.dial_63.valueChanged.connect(self.Knob47)
		self.dials[55] = self.dial_63
		
		self.horizontalLayout_17.addWidget(self.dial_63)
		self.dial_64 = QDial(self.layoutWidget_14)
		self.dial_64.setMaximum(1024)
		self.dial_64.setObjectName(_fromUtf8("dial_64"))
		self.dial_64.valueChanged.connect(self.Knob48)
		self.dials[56] = self.dial_64
		
		self.horizontalLayout_17.addWidget(self.dial_64)
		self.layoutWidget_15 = QWidget(self.centralwidget)
		self.layoutWidget_15.setGeometry(QRect(480, 600, 451, 45))
		self.layoutWidget_15.setObjectName(_fromUtf8("layoutWidget_15"))
		self.horizontalLayout_18 = QHBoxLayout(self.layoutWidget_15)
		self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
		self.pushButton_73 = QPushButton(self.layoutWidget_15)
		self.pushButton_73.setObjectName(_fromUtf8("pushButton_73"))
		self.pushButton_73.clicked.connect(self.RST49)
		
		self.horizontalLayout_18.addWidget(self.pushButton_73)
		self.pushButton_74 = QPushButton(self.layoutWidget_15)
		self.pushButton_74.setObjectName(_fromUtf8("pushButton_74"))
		self.pushButton_74.clicked.connect(self.RST410)
		
		self.horizontalLayout_18.addWidget(self.pushButton_74)
		self.pushButton_75 = QPushButton(self.layoutWidget_15)
		self.pushButton_75.setObjectName(_fromUtf8("pushButton_75"))
		self.pushButton_75.clicked.connect(self.RST411)
		
		self.horizontalLayout_18.addWidget(self.pushButton_75)
		self.pushButton_76 = QPushButton(self.layoutWidget_15)
		self.pushButton_76.setObjectName(_fromUtf8("pushButton_76"))
		self.pushButton_76.clicked.connect(self.RST412)
		
		self.horizontalLayout_18.addWidget(self.pushButton_76)
		self.pushButton_77 = QPushButton(self.layoutWidget_15)
		self.pushButton_77.setObjectName(_fromUtf8("pushButton_77"))
		self.pushButton_77.clicked.connect(self.RST413)
		
		self.horizontalLayout_18.addWidget(self.pushButton_77)
		self.pushButton_78 = QPushButton(self.layoutWidget_15)
		self.pushButton_78.setObjectName(_fromUtf8("pushButton_78"))
		self.pushButton_78.clicked.connect(self.RST414)
		
		self.horizontalLayout_18.addWidget(self.pushButton_78)
		self.pushButton_79 = QPushButton(self.layoutWidget_15)
		self.pushButton_79.setObjectName(_fromUtf8("pushButton_79"))
		self.pushButton_79.clicked.connect(self.RST415)
		
		self.horizontalLayout_18.addWidget(self.pushButton_79)
		self.pushButton_80 = QPushButton(self.layoutWidget_15)
		self.pushButton_80.setObjectName(_fromUtf8("pushButton_80"))
		self.pushButton_80.clicked.connect(self.RST416)
		
		self.horizontalLayout_18.addWidget(self.pushButton_80)
		
		self.spinBox = QSpinBox(self.centralwidget)
		self.spinBox.setGeometry(QRect(890, 640, 42, 22))
		self.spinBox.setObjectName(_fromUtf8("spinBox"))
		self.spinBox.valueChanged.connect(self.ChangeScene)
		
		self.lcd = QLCDNumber(self.centralwidget)
		self.lcd.display("C0")
		self.lcd.setGeometry(QRect(890-45,640,42,22))
		self.lcd.setObjectName(_fromUtf8("lcd"))
		
		self.widget = QWidget(self.centralwidget)
		self.widget.setGeometry(QRect(30, 30, 451, 102))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.horizontalLayout = QHBoxLayout(self.widget)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		
		self.dial = QDial(self.widget)
		self.dial.setMaximum(1024)
		self.dial.setObjectName(_fromUtf8("dial"))
		self.dial.valueChanged.connect(self.Knob1)
		self.dials[1] = self.dial
		
		self.horizontalLayout.addWidget(self.dial)
		self.dial_3 = QDial(self.widget)
		self.dial_3.setMaximum(1024)
		self.dial_3.valueChanged.connect(self.Knob2)
		self.dials[2] = self.dial_3
		
		self.dial_3.setObjectName(_fromUtf8("dial_3"))
		self.horizontalLayout.addWidget(self.dial_3)
		self.dial_5 = QDial(self.widget)
		self.dial_5.setMaximum(1024)
		self.dial_5.valueChanged.connect(self.Knob3)
		self.dials[3] = self.dial_5
		
		self.dial_5.setObjectName(_fromUtf8("dial_5"))
		self.horizontalLayout.addWidget(self.dial_5)
		self.dial_7 = QDial(self.widget)
		self.dial_7.setMaximum(1024)
		self.dial_7.valueChanged.connect(self.Knob4)
		self.dials[4] = self.dial_7
		
		self.dial_7.setObjectName(_fromUtf8("dial_7"))
		self.horizontalLayout.addWidget(self.dial_7)
		self.dial_2 = QDial(self.widget)
		self.dial_2.setMaximum(1024)
		self.dial_2.setObjectName(_fromUtf8("dial_2"))
		self.dial_2.valueChanged.connect(self.Knob5)
		self.dials[5] = self.dial_2
		
		self.horizontalLayout.addWidget(self.dial_2)
		self.dial_4 = QDial(self.widget)
		self.dial_4.setMaximum(1024)
		self.dial_4.setObjectName(_fromUtf8("dial_4"))
		self.dial_4.valueChanged.connect(self.Knob6)
		self.dials[6] = self.dial_4
		
		self.horizontalLayout.addWidget(self.dial_4)
		self.dial_6 = QDial(self.widget)
		self.dial_6.setMaximum(1024)
		self.dial_6.setObjectName(_fromUtf8("dial_6"))
		self.dial_6.valueChanged.connect(self.Knob7)
		self.dials[7] = self.dial_6
		
		self.horizontalLayout.addWidget(self.dial_6)
		self.dial_8 = QDial(self.widget)
		self.dial_8.setMaximum(1024)
		self.dial_8.valueChanged.connect(self.Knob8)
		self.dial_8.setObjectName(_fromUtf8("dial_8"))
		self.dials[8] = self.dial_8
		
		self.horizontalLayout.addWidget(self.dial_8)
		self.widget1 = QWidget(self.centralwidget)
		self.widget1.setGeometry(QRect(30, 140, 451, 45))
		self.widget1.setObjectName(_fromUtf8("widget1"))
		self.horizontalLayout_3 = QHBoxLayout(self.widget1)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		
		self.pushButton = QPushButton(self.widget1)
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.pushButton.clicked.connect(self.RST1)
		
		self.horizontalLayout_3.addWidget(self.pushButton)
		self.pushButton_4 = QPushButton(self.widget1)
		self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
		self.pushButton_4.clicked.connect(self.RST2)
		
		self.horizontalLayout_3.addWidget(self.pushButton_4)
		self.pushButton_6 = QPushButton(self.widget1)
		self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
		self.pushButton_6.clicked.connect(self.RST3)
		
		self.horizontalLayout_3.addWidget(self.pushButton_6)
		self.pushButton_8 = QPushButton(self.widget1)
		self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
		self.pushButton_8.clicked.connect(self.RST4)
		
		self.horizontalLayout_3.addWidget(self.pushButton_8)
		self.pushButton_10 = QPushButton(self.widget1)
		self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
		self.pushButton_10.clicked.connect(self.RST5)
		
		self.horizontalLayout_3.addWidget(self.pushButton_10)
		self.pushButton_12 = QPushButton(self.widget1)
		self.pushButton_12.setObjectName(_fromUtf8("pushButton_12"))
		self.pushButton_12.clicked.connect(self.RST6)
		
		self.horizontalLayout_3.addWidget(self.pushButton_12)
		self.pushButton_14 = QPushButton(self.widget1)
		self.pushButton_14.setObjectName(_fromUtf8("pushButton_14"))
		self.pushButton_14.clicked.connect(self.RST7)
		
		self.horizontalLayout_3.addWidget(self.pushButton_14)
		self.pushButton_16 = QPushButton(self.widget1)
		self.pushButton_16.setObjectName(_fromUtf8("pushButton_16"))
		self.pushButton_16.clicked.connect(self.RST8)
		
		self.horizontalLayout_3.addWidget(self.pushButton_16)
		self.widget2 = QWidget(self.centralwidget)
		self.widget2.setGeometry(QRect(30, 170, 451, 45))
		self.widget2.setObjectName(_fromUtf8("widget2"))
		self.horizontalLayout_4 = QHBoxLayout(self.widget2)
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.pushButton_2 = QPushButton(self.widget2)
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.pushButton_2.clicked.connect(self.RESET1)
		
		self.horizontalLayout_4.addWidget(self.pushButton_2)
		self.pushButton_3 = QPushButton(self.widget2)
		self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
		self.pushButton_3.clicked.connect(self.RESET2)
		
		self.horizontalLayout_4.addWidget(self.pushButton_3)
		self.pushButton_5 = QPushButton(self.widget2)
		self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
		self.pushButton_5.clicked.connect(self.RESET3)
		
		self.horizontalLayout_4.addWidget(self.pushButton_5)
		self.pushButton_7 = QPushButton(self.widget2)
		self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
		self.pushButton_7.clicked.connect(self.RESET4)
		
		self.horizontalLayout_4.addWidget(self.pushButton_7)
		self.pushButton_9 = QPushButton(self.widget2)
		self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
		self.pushButton_9.clicked.connect(self.RESET5)
		
		self.horizontalLayout_4.addWidget(self.pushButton_9)
		self.pushButton_11 = QPushButton(self.widget2)
		self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
		self.pushButton_11.clicked.connect(self.RESET6)
		
		self.horizontalLayout_4.addWidget(self.pushButton_11)
		self.pushButton_13 = QPushButton(self.widget2)
		self.pushButton_13.setObjectName(_fromUtf8("pushButton_13"))
		self.pushButton_13.clicked.connect(self.RESET7)
		
		self.horizontalLayout_4.addWidget(self.pushButton_13)
		self.pushButton_15 = QPushButton(self.widget2)
		self.pushButton_15.setObjectName(_fromUtf8("pushButton_15"))
		self.pushButton_15.clicked.connect(self.RESET8)
		
		self.horizontalLayout_4.addWidget(self.pushButton_15)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QMenuBar(MainWindow)
		self.menubar.setGeometry(QRect(0, 0, 949, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		self.menuScene = QMenu(self.menubar)
		self.menuScene.setObjectName(_fromUtf8("menuScene"))
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionLoad_scene = QAction(MainWindow)
		self.actionLoad_scene.setObjectName(_fromUtf8("actionLoad_scene"))
		self.actionSave_scene = QAction(MainWindow)
		self.actionSave_scene.setObjectName(_fromUtf8("actionSave_scene"))
		self.actionExit = QAction(MainWindow)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionCopy = QAction(MainWindow)
		self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
		self.actionCopy.triggered.connect(self.Copy)
		self.actionPaste = QAction(MainWindow)
		self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
		self.actionPaste.triggered.connect(self.Paste)
		self.actionNextStep = QAction(MainWindow)
		self.actionNextStep.setObjectName(_fromUtf8("actionNextStep"))
		self.actionNextStep.triggered.connect(self.NextStep)
		self.actionPrevStep = QAction(MainWindow)
		self.actionPrevStep.setObjectName(_fromUtf8("actionPrevStep"))
		self.actionPrevStep.triggered.connect(self.PrevStep)
		self.actionOptions = QAction(MainWindow)
		self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
		self.actionRandom_scene = QAction(MainWindow)
		self.actionRandom_scene.setObjectName(_fromUtf8("actionRandom_scene"))
		self.actionRandom_scene.triggered.connect(self.RandomScene)
		self.actionBreedPatch = QAction(MainWindow)
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
		QMetaObject.connectSlotsByName(MainWindow)
		self.ChangeScene(0)
		
	def PrevStep(self):
		self.updateThread.cur_step = self.updateThread.cur_step - 1
		if(self.updateThread.cur_step):
			self.updateThread.cur_step = 15
			
	def NextStep(self):
		self.updateThread.cur_step = self.updateThread.cur_step + 1
		self.updateThread.cur_step = self.updateThread.cur_step % 16
		
	def Copy(self):
		self.copy_buffer = self.scenes[self.cur_scene][:]
		
	def Paste(self):
		self.scenes[self.cur_scene] = self.copy_buffer[:]
		
	def RandomScene(self):
		seq=MOPHO_GenerateSequence()
		
		for i in range(4):
			for j in range(16):
				self.scenes[self.cur_scene][i*16+j] = int((seq[i][j]/127.0)*1024.0)
			
		self.UpdateUi()

	def Load(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
		self.scenes = pickle.load(open(filename,'r'))
		
	def Save(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '.')
		pickle.dump(self.scenes,open(filename,'w'))
		
	def ChangeScene(self,value):
		if(value >= self.total_scenes):
			self.total_scenes = value+1
		self.cur_scene = value
		self.UpdateUi()
		
	def Dial(self,seq,step,note):
		if(seq == 0): sqx = NRPN_SEQ1_STEP1
		elif(seq == 1): sqx = NRPN_SEQ2_STEP1
		elif(seq == 2): sqx = NRPN_SEQ3_STEP1
		else: sqx=NRPN_SEQ4_STEP1
		
		value = int(math.ceil((note/1024.0)*127))
		#value = scaling[value]
		self.lcd.display(str(notes[value]))
		MOPHO_SendSeqStep(sqx,step,value,self.midi_channel)
		self.scenes[self.cur_scene][seq*16+step] = note
	
	def Knob1(self,value):
	    self.Dial(0,0,value)
	def Knob2(self,value):
	    self.Dial(0,1,value)
	def Knob3(self,value):
	    self.Dial(0,2,value)
	def Knob4(self,value):
	    self.Dial(0,3,value)
	def Knob5(self,value):
	    self.Dial(0,4,value)
	def Knob6(self,value):
	    self.Dial(0,5,value)
	def Knob7(self,value):
	    self.Dial(0,6,value)
	def Knob8(self,value):
	    self.Dial(0,7,value)
	def Knob9(self,value):
	    self.Dial(0,8,value)
	def Knob10(self,value):
	    self.Dial(0,9,value)
	def Knob11(self,value):
	    self.Dial(0,10,value)
	def Knob12(self,value):
	    self.Dial(0,11,value)
	def Knob13(self,value):
	    self.Dial(0,12,value)
	def Knob14(self,value):
	    self.Dial(0,13,value)
	def Knob15(self,value):
	    self.Dial(0,14,value)
	def Knob16(self,value):
	    self.Dial(0,15,value)
	    
	
	def Knob21(self,value):
	    self.Dial(1,0,value)
	def Knob22(self,value):
	    self.Dial(1,1,value)
	def Knob23(self,value):
	    self.Dial(1,2,value)
	def Knob24(self,value):
	    self.Dial(1,3,value)
	def Knob25(self,value):
	    self.Dial(1,4,value)
	def Knob26(self,value):
	    self.Dial(1,5,value)
	def Knob27(self,value):
	    self.Dial(1,6,value)
	def Knob28(self,value):
	    self.Dial(1,7,value)
	def Knob29(self,value):
	    self.Dial(1,8,value)
	def Knob210(self,value):
	    self.Dial(1,9,value)
	def Knob211(self,value):
	    self.Dial(1,10,value)
	def Knob212(self,value):
	    self.Dial(1,11,value)
	def Knob213(self,value):
	    self.Dial(1,12,value)
	def Knob214(self,value):
	    self.Dial(1,13,value)
	def Knob215(self,value):
	    self.Dial(1,14,value)
	def Knob216(self,value):
	    self.Dial(1,15,value)
	
	
	def Knob31(self,value):
	    self.Dial(2,0,value)
	def Knob32(self,value):
	    self.Dial(2,1,value)
	def Knob33(self,value):
	    self.Dial(2,2,value)
	def Knob34(self,value):
	    self.Dial(2,3,value)
	def Knob35(self,value):
	    self.Dial(2,4,value)
	def Knob36(self,value):
	    self.Dial(2,5,value)
	def Knob37(self,value):
	    self.Dial(2,6,value)
	def Knob38(self,value):
	    self.Dial(2,7,value)
	def Knob39(self,value):
	    self.Dial(2,8,value)
	def Knob310(self,value):
	    self.Dial(2,9,value)
	def Knob311(self,value):
	    self.Dial(2,10,value)
	def Knob312(self,value):
	    self.Dial(2,11,value)
	def Knob313(self,value):
	    self.Dial(2,12,value)
	def Knob314(self,value):
	    self.Dial(2,13,value)
	def Knob315(self,value):
	    self.Dial(2,14,value)
	def Knob316(self,value):
	    self.Dial(2,15,value)
	
	def Knob41(self,value):
	    self.Dial(3,0,value)
	def Knob42(self,value):
	    self.Dial(3,1,value)
	def Knob43(self,value):
	    self.Dial(3,2,value)
	def Knob44(self,value):
	    self.Dial(3,3,value)
	def Knob45(self,value):
	    self.Dial(3,4,value)
	def Knob46(self,value):
	    self.Dial(3,5,value)
	def Knob47(self,value):
	    self.Dial(3,6,value)
	def Knob48(self,value):
	    self.Dial(3,7,value)
	def Knob49(self,value):
	    self.Dial(3,8,value)
	def Knob410(self,value):
	    self.Dial(3,9,value)
	def Knob411(self,value):
	    self.Dial(3,10,value)
	def Knob412(self,value):
	    self.Dial(3,11,value)
	def Knob413(self,value):
	    self.Dial(3,12,value)
	def Knob414(self,value):
	    self.Dial(3,13,value)
	def Knob415(self,value):
	    self.Dial(3,14,value)
	def Knob416(self,value):
	    self.Dial(3,15,value)
	
	def RESET1(self,value):
	    self.Dial(0,0,self.RSTV)
	def RESET2(self,value):
	    self.Dial(0,1,self.RSTV)
	def RESET3(self,value):
	    self.Dial(0,2,self.RSTV)
	def RESET4(self,value):
	    self.Dial(0,3,self.RESTV)
	def RESET5(self,value):
	    self.Dial(0,4,self.RSTV)
	def RESET6(self,value):
	    self.Dial(0,5,self.RESTV)
	def RESET7(self,value):
	    self.Dial(0,6,self.RSTV)
	def RESET8(self,value):
	    self.Dial(0,7,self.RSTV)
	def RESET9(self,value):
	    self.Dial(0,8,self.RSTV)
	def RESET10(self,value):
	    self.Dial(0,9,self.RSTV)
	def RESET11(self,value):
	    self.Dial(0,10,self.RSTV)
	def RESET12(self,value):
	    self.Dial(0,11,self.RSTV)
	def RESET13(self,value):
	    self.Dial(0,12,self.RSTV)
	def RESET14(self,value):
	    self.Dial(0,13,self.RSTV)
	def RESET15(self,value):
	    self.Dial(0,14,self.RSTV)
	def RESET16(self,value):
	    self.Dial(0,15,self.RSTV)
	    
	    
	def RST1(self,value):		
	    self.Dial(0,0,self.RESTV)
	def RST2(self,value):
	    self.Dial(0,1,self.RESTV)
	def RST3(self,value):
	    self.Dial(0,2,self.RESTV)
	def RST4(self,value):
	    self.Dial(0,3,self.RESTV)
	def RST5(self,value):
	    self.Dial(0,4,self.RESTV)
	def RST6(self,value):
	    self.Dial(0,5,self.RESTV)
	def RST7(self,value):
	    self.Dial(0,6,self.RESTV)
	def RST8(self,value):
	    self.Dial(0,7,self.RESTV)
	def RST9(self,value):
	    self.Dial(0,8,self.RESTV)
	def RST10(self,value):
	    self.Dial(0,9,self.RESTV)
	def RST11(self,value):
	    self.Dial(0,10,self.RESTV)
	def RST12(self,value):
	    self.Dial(0,11,self.RESTV)
	def RST13(self,value):
	    self.Dial(0,12,self.RESTV)
	def RST14(self,value):
	    self.Dial(0,13,self.RESTV)
	def RST15(self,value):
	    self.Dial(0,14,self.RESTV)
	def RST16(self,value):
	    self.Dial(0,15,self.RESTV)
	    

	def RST21(self,value):
	    self.Dial(1,0,self.RSTV)
	def RST22(self,value):
	    self.Dial(1,1,self.RSTV)
	def RST23(self,value):
	    self.Dial(1,2,self.RSTV)
	def RST24(self,value):
	    self.Dial(1,3,self.RSTV)
	def RST25(self,value):
	    self.Dial(1,4,self.RSTV)
	def RST26(self,value):
	    self.Dial(1,5,self.RSTV)
	def RST27(self,value):
	    self.Dial(1,6,self.RSTV)
	def RST28(self,value):
	    self.Dial(1,7,self.RSTV)
	def RST29(self,value):
	    self.Dial(1,8,self.RSTV)
	def RST210(self,value):
	    self.Dial(1,9,self.RSTV)
	def RST211(self,value):
	    self.Dial(1,10,self.RSTV)
	def RST212(self,value):
	    self.Dial(1,11,self.RSTV)
	def RST213(self,value):
	    self.Dial(1,12,self.RSTV)
	def RST214(self,value):
	    self.Dial(1,13,self.RSTV)
	def RST215(self,value):
	    self.Dial(1,14,self.RSTV)
	def RST216(self,value):
	    self.Dial(1,15,self.RSTV)
	    
	def RST31(self,value):
	    self.Dial(2,0,self.RSTV)
	def RST32(self,value):
	    self.Dial(2,1,self.RSTV)
	def RST33(self,value):
	    self.Dial(2,2,self.RSTV)
	def RST34(self,value):
	    self.Dial(2,3,self.RSTV)
	def RST35(self,value):
	    self.Dial(2,4,self.RSTV)
	def RST36(self,value):
	    self.Dial(2,5,self.RSTV)
	def RST37(self,value):
	    self.Dial(2,6,self.RSTV)
	def RST38(self,value):
	    self.Dial(2,7,self.RSTV)
	def RST39(self,value):
	    self.Dial(2,8,self.RSTV)
	def RST310(self,value):
	    self.Dial(2,9,self.RSTV)
	def RST311(self,value):
	    self.Dial(2,10,self.RSTV)
	def RST312(self,value):
	    self.Dial(2,11,self.RSTV)
	def RST313(self,value):
	    self.Dial(2,12,self.RSTV)
	def RST314(self,value):
	    self.Dial(2,13,self.RSTV)
	def RST315(self,value):
	    self.Dial(2,14,self.RSTV)
	def RST316(self,value):
	    self.Dial(2,15,self.RSTV)

	def RST41(self,value):
	    self.Dial(3,0,self.RSTV)
	def RST42(self,value):
	    self.Dial(3,1,self.RSTV)
	def RST43(self,value):
	    self.Dial(3,2,self.RSTV)
	def RST44(self,value):
	    self.Dial(3,3,self.RSTV)
	def RST45(self,value):
	    self.Dial(3,4,self.RSTV)
	def RST46(self,value):
	    self.Dial(3,5,self.RSTV)
	def RST47(self,value):
	    self.Dial(3,6,self.RSTV)
	def RST48(self,value):
	    self.Dial(3,7,self.RSTV)
	def RST49(self,value):
	    self.Dial(3,8,self.RSTV)
	def RST410(self,value):
	    self.Dial(3,9,self.RSTV)
	def RST411(self,value):
	    self.Dial(3,10,self.RSTV)
	def RST412(self,value):
	    self.Dial(3,11,self.RSTV)
	def RST413(self,value):
	    self.Dial(3,12,self.RSTV)
	def RST414(self,value):
	    self.Dial(3,13,self.RSTV)
	def RST415(self,value):
	    self.Dial(3,14,self.RSTV)
	def RST416(self,value):
	    self.Dial(3,15,self.RSTV)

	def BreedPatch(self):
		sysex = realtime_gen()
		midi_output.send(MSG(sysex))
		
	def UpdateUi(self):		
		for i in range(64):			
			self.dials[i+1].setValue(self.scenes[self.cur_scene][i])
		
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.pushButton_17.setText(_translate("MainWindow", "RST", None))
		self.pushButton_18.setText(_translate("MainWindow", "RST", None))
		self.pushButton_19.setText(_translate("MainWindow", "RST", None))
		self.pushButton_20.setText(_translate("MainWindow", "RST", None))
		self.pushButton_21.setText(_translate("MainWindow", "RST", None))
		self.pushButton_22.setText(_translate("MainWindow", "RST", None))
		self.pushButton_23.setText(_translate("MainWindow", "RST", None))
		self.pushButton_24.setText(_translate("MainWindow", "RST", None))
		self.pushButton_25.setText(_translate("MainWindow", "REST", None))
		self.pushButton_26.setText(_translate("MainWindow", "REST", None))
		self.pushButton_27.setText(_translate("MainWindow", "REST", None))
		self.pushButton_28.setText(_translate("MainWindow", "REST", None))
		self.pushButton_29.setText(_translate("MainWindow", "REST", None))
		self.pushButton_30.setText(_translate("MainWindow", "REST", None))
		self.pushButton_31.setText(_translate("MainWindow", "REST", None))
		self.pushButton_32.setText(_translate("MainWindow", "REST", None))
		self.pushButton_33.setText(_translate("MainWindow", "RST", None))
		self.pushButton_34.setText(_translate("MainWindow", "RST", None))
		self.pushButton_35.setText(_translate("MainWindow", "RST", None))
		self.pushButton_36.setText(_translate("MainWindow", "RST", None))
		self.pushButton_37.setText(_translate("MainWindow", "RST", None))
		self.pushButton_38.setText(_translate("MainWindow", "RST", None))
		self.pushButton_39.setText(_translate("MainWindow", "RST", None))
		self.pushButton_40.setText(_translate("MainWindow", "RST", None))
		self.pushButton_41.setText(_translate("MainWindow", "RST", None))
		self.pushButton_42.setText(_translate("MainWindow", "RST", None))
		self.pushButton_43.setText(_translate("MainWindow", "RST", None))
		self.pushButton_44.setText(_translate("MainWindow", "RST", None))
		self.pushButton_45.setText(_translate("MainWindow", "RST", None))
		self.pushButton_46.setText(_translate("MainWindow", "RST", None))
		self.pushButton_47.setText(_translate("MainWindow", "RST", None))
		self.pushButton_48.setText(_translate("MainWindow", "RST", None))
		self.pushButton_49.setText(_translate("MainWindow", "RST", None))
		self.pushButton_50.setText(_translate("MainWindow", "RST", None))
		self.pushButton_51.setText(_translate("MainWindow", "RST", None))
		self.pushButton_52.setText(_translate("MainWindow", "RST", None))
		self.pushButton_53.setText(_translate("MainWindow", "RST", None))
		self.pushButton_54.setText(_translate("MainWindow", "RST", None))
		self.pushButton_55.setText(_translate("MainWindow", "RST", None))
		self.pushButton_56.setText(_translate("MainWindow", "RST", None))
		self.pushButton_57.setText(_translate("MainWindow", "RST", None))
		self.pushButton_58.setText(_translate("MainWindow", "RST", None))
		self.pushButton_59.setText(_translate("MainWindow", "RST", None))
		self.pushButton_60.setText(_translate("MainWindow", "RST", None))
		self.pushButton_61.setText(_translate("MainWindow", "RST", None))
		self.pushButton_62.setText(_translate("MainWindow", "RST", None))
		self.pushButton_63.setText(_translate("MainWindow", "RST", None))
		self.pushButton_64.setText(_translate("MainWindow", "RST", None))
		self.pushButton_65.setText(_translate("MainWindow", "RST", None))
		self.pushButton_66.setText(_translate("MainWindow", "RST", None))
		self.pushButton_67.setText(_translate("MainWindow", "RST", None))
		self.pushButton_68.setText(_translate("MainWindow", "RST", None))
		self.pushButton_69.setText(_translate("MainWindow", "RST", None))
		self.pushButton_70.setText(_translate("MainWindow", "RST", None))
		self.pushButton_71.setText(_translate("MainWindow", "RST", None))
		self.pushButton_72.setText(_translate("MainWindow", "RST", None))
		self.pushButton_73.setText(_translate("MainWindow", "RST", None))
		self.pushButton_74.setText(_translate("MainWindow", "RST", None))
		self.pushButton_75.setText(_translate("MainWindow", "RST", None))
		self.pushButton_76.setText(_translate("MainWindow", "RST", None))
		self.pushButton_77.setText(_translate("MainWindow", "RST", None))
		self.pushButton_78.setText(_translate("MainWindow", "RST", None))
		self.pushButton_79.setText(_translate("MainWindow", "RST", None))
		self.pushButton_80.setText(_translate("MainWindow", "RST", None))
		self.pushButton.setText(_translate("MainWindow", "RST", None))
		self.pushButton_4.setText(_translate("MainWindow", "RST", None))
		self.pushButton_6.setText(_translate("MainWindow", "RST", None))
		self.pushButton_8.setText(_translate("MainWindow", "RST", None))
		self.pushButton_10.setText(_translate("MainWindow", "RST", None))
		self.pushButton_12.setText(_translate("MainWindow", "RST", None))
		self.pushButton_14.setText(_translate("MainWindow", "RST", None))
		self.pushButton_16.setText(_translate("MainWindow", "RST", None))
		self.pushButton_2.setText(_translate("MainWindow", "REST", None))
		self.pushButton_3.setText(_translate("MainWindow", "REST", None))
		self.pushButton_5.setText(_translate("MainWindow", "REST", None))
		self.pushButton_7.setText(_translate("MainWindow", "REST", None))
		self.pushButton_9.setText(_translate("MainWindow", "REST", None))
		self.pushButton_11.setText(_translate("MainWindow", "REST", None))
		self.pushButton_13.setText(_translate("MainWindow", "REST", None))
		self.pushButton_15.setText(_translate("MainWindow", "REST", None))
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