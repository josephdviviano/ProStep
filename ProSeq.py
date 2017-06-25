# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProSeq.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from mido.sockets import PortServer,connect
import pickle
import math
import sys

from midi import *
from mopho import *
from patterns import *
from mido import Message,MidiFile,MidiTrack
import proseq16x8
import seq16x8
import seq16


# Transpose, Shift
# Setup MIDI channels easier
# Turn off MIDI setup in MDI child

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

# thread for handling MIDI i/o		
class Worker(QtCore.QThread):
	
	def __init__(self,mainwindow,parent=None):
		QtCore.QThread.__init__(self,parent)
		self.exiting = False
		self.mainwindow = mainwindow		
		self.ppq = -1
		self.cur_ppq = -1
		self.input_buffer = [0]*256
		self.cur_step = 0
		self.note = 0
		self.repeats = 0
		self.cur_note = 0
		self.rest = 0
		self.midi_channel =0
		self.kb_channel    = 0
		self.midi_input = None
		self.midi_output = None
		self.num_steps = 16
		self.key_ppq = [0]*127
		self.key_last = [0]*127
		
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
					
					for window in self.mainwindow.mdiArea.subWindowList():
						self.mainwindow.windows[window.widget()].UpdateMIDI()
					sync = MIDI_GetSyncPorts()
					if(not sync is None): sync.send(msg)
					self.emit(QtCore.SIGNAL("UpdateUi()"))
					
				elif(key[0] >= 0x90 and key[0] <= 0x9F):
					
					activeSubWindow = self.mainwindow.mdiArea.activeSubWindow()
					if activeSubWindow:
						self.mainwindow.windows[activeSubWindow.widget()].UpdateMIDIInput(key)
					
					self.emit(QtCore.SIGNAL("UpdateUi()"))
					
				#elif(key[0] >= 0x80 and key[0] <= 0x8F):
				#	if(key[0] == 0x80 + self.kb_channel):	
				#		ppq = self.ppq - self.key_ppq[key[1]]						
				#		seq = self.mainwindow.GetSequencer()
				#		seq.SetPPQ(self.key_last[key[1]],ppq)
						
						
				self.midi_output.send(msg)


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
		MIDI_Close()
		
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
		
		MIDI_SetInOut(key,clk,out)
		if(len(syncs) > 0):
			MIDI_SetSyncPorts(syncs)
		
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
		self.windows = {}
		
	def CreateSeq16(self):
		window = QtGui.QMainWindow()	
		ui = seq16.Ui_MainWindow()
		ui.setupUi(window,True)
		self.mdiArea.addSubWindow(window)
		self.windows[window] = ui
		window.resize(940,600)
		window.show()
		
		
	def CreateSeq16x8(self):
		window = QtGui.QMainWindow()	
		ui = seq16x8.Ui_MainWindow()
		ui.setupUi(window,True)
		self.mdiArea.addSubWindow(window)
		self.windows[window] = ui
		window.show()
		
		
	def CreateProSeq16x8(self):

		window = QtGui.QMainWindow()	
		ui = proseq16x8.Ui_MainWindow()
		ui.setupUi(window,True)
		self.mdiArea.addSubWindow(window)
		self.windows[window] = ui
		window.show()
		
		
	def MIDIOptions(self):
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
		
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(1280, 857)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.mdiArea = QtGui.QMdiArea(self.centralwidget)
		self.mdiArea.setGeometry(QtCore.QRect(0, 0, 1280, 821))
		self.mdiArea.setObjectName(_fromUtf8("mdiArea"))
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 920, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		self.menuSequencer = QtGui.QMenu(self.menubar)
		self.menuSequencer.setObjectName(_fromUtf8("menuSequencer"))
		
		self.thread = Worker(self)		
		MainWindow.connect(self.thread, QtCore.SIGNAL("finished()"), self.UpdateUi)
		MainWindow.connect(self.thread, QtCore.SIGNAL("terminated()"), self.UpdateUi)
		MainWindow.connect(self.thread, QtCore.SIGNAL("UpdateUi()"), self.UpdateUi)
		self.mainwindow = MainWindow
		
		self.thread.start()
		
		self.menuMIDI = QtGui.QMenu(self.menubar)
		self.menuMIDI.setObjectName(_fromUtf8("menuMIDI"))
		
		self.actionOptions = QtGui.QAction(MainWindow)		
		self.actionOptions.setObjectName(_fromUtf8("actionOptions"))		
		self.actionOptions.triggered.connect(self.MIDIOptions)
		
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionExit = QtGui.QAction(MainWindow)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		
		self.actionSeq16 = QtGui.QAction(MainWindow)
		self.actionSeq16.setObjectName(_fromUtf8("actionSeq16"))
		self.actionSeq16.triggered.connect(self.CreateSeq16)
		
		self.actionSeq16x8 = QtGui.QAction(MainWindow)
		self.actionSeq16x8.setObjectName(_fromUtf8("actionSeq16x8"))		
		self.actionSeq16x8.triggered.connect(self.CreateSeq16x8)

		self.actionProSeq16x8 = QtGui.QAction(MainWindow)
		self.actionProSeq16x8.setObjectName(_fromUtf8("actionProSeq16x8"))
		self.actionProSeq16x8.triggered.connect(self.CreateProSeq16x8)
		
		self.actionSeqMatrix = QtGui.QAction(MainWindow)
		self.actionSeqMatrix.setObjectName(_fromUtf8("actionSeqMatrix"))
		self.actionMophoLab = QtGui.QAction(MainWindow)
		self.actionMophoLab.setObjectName(_fromUtf8("actionMophoLab"))
		self.actionMidiLoop16 = QtGui.QAction(MainWindow)
		self.actionMidiLoop16.setObjectName(_fromUtf8("actionMidiLoop16"))
		
		
		self.actionSeqMatrix_2 = QtGui.QAction(MainWindow)
		self.actionSeqMatrix_2.setObjectName(_fromUtf8("actionSeqMatrix_2"))
		self.actionSeq42_6 = QtGui.QAction(MainWindow)
		self.actionSeq42_6.setObjectName(_fromUtf8("actionSeq42_6"))
		self.menuFile.addAction(self.actionExit)
		self.menuSequencer.addAction(self.actionSeq16)
		self.menuSequencer.addAction(self.actionSeq16x8)
		self.menuSequencer.addAction(self.actionProSeq16x8)
		
		self.menuSequencer.addAction(self.actionSeq42_6)
		self.menuSequencer.addAction(self.actionSeqMatrix_2)
		self.menuSequencer.addAction(self.actionSeqMatrix)
		self.menuSequencer.addAction(self.actionMophoLab)
		self.menuSequencer.addAction(self.actionMidiLoop16)
		self.menuSequencer.addSeparator()
		self.menuMIDI.addAction(self.actionOptions)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuSequencer.menuAction())
		self.menubar.addAction(self.menuMIDI.menuAction())
		
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.menuFile.setTitle(_translate("MainWindow", "File", None))
		self.menuSequencer.setTitle(_translate("MainWindow", "Create", None))
		self.menuMIDI.setTitle(_translate("MainWindow", "MIDI", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionSeq16.setText(_translate("MainWindow", "Seq16", None))
		self.actionSeq16x8.setText(_translate("MainWindow", "Seq16x8", None))
		self.actionProSeq16x8.setText(_translate("MainWindow", "ProSeq16x8", None))
		self.actionSeqMatrix.setText(_translate("MainWindow", "StepMatrix64", None))
		self.actionMophoLab.setText(_translate("MainWindow", "MophoLab", None))
		self.actionMidiLoop16.setText(_translate("MainWindow", "MidiLooper16", None))
		self.actionOptions.setText(_translate("MainWindow", "Options", None))
		self.actionSeqMatrix_2.setText(_translate("MainWindow", "SeqMatrix", None))
		self.actionSeq42_6.setText(_translate("MainWindow", "Seq42+6", None))

	def UpdateUi(self):
		activeSubWindow = self.mdiArea.activeSubWindow()
		if activeSubWindow:
			self.windows[activeSubWindow.widget()].UpdateUi()
					
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
	