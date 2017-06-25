
from PyQt4 import QtCore, QtGui
from mido.sockets import PortServer,connect
import pickle
import math
import sys

from midi import *
from mopho import *
from patterns import *
from mido import Message,MidiFile,MidiTrack

# multiple sequencers running
# pattern chain - sequencer #, num_measures

TEMPO=145.0

PPQ_WHOLE=96
PLAY_LEN=4*PPQ_WHOLE
TX_DELAY=0.01

MIDI_CHANNEL=1
MIDIKB_CHANNEL=1

fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

MUSIC_SetScaleChord(scale_phrygian_dom,chord_min)

# maximum voice sequencers
MAX_SEQS=16
MAX_TRACKERS=16

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

note_names = []
for i in range(0,127):
	n = i % 12
	s = name_notes[n]
	x = s + str(i / 12)
	note_names.append(x)
	

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

# Voice is a monophonic sequence
class Voice:
	
	def __init__(self, steps=16):
		self.seq_length = steps
		self.notes = [0]*self.seq_length
		self.velocity = [0]*self.seq_length
		self.cur_step = 0
		self.ppq = [0]*self.seq_length
		self.repeats = [0]*self.seq_length
		self.rests = [0]*self.seq_length
		self.num_steps = steps
		self.cur_ppq = 6
		self.cur_repeats = 0
		self.rest = 0
		self.note = 0
		self.Randomize()
		self.cur_bank = 0
		self.last_note=0
		self.midi_channel = 0	
		self.midi_input = None
		self.midi_output=None
		self.reset = True
		self.cur_instep = 0
		
	def SetNote(self,step,note):		
		self.notes[step+self.cur_bank*16] = note

	def SetNoteStep(self,step,note):		
		self.notes[step] = note
		
		
	def SetPPQ(self,step,ppq):
		self.ppq[step+self.cur_bank*16] = ppq
	
	def SetRest(self,step,value):
		self.rests[step+self.cur_bank*16] = value
	
	def SetRepeat(self,step,value):
		self.repeats[step+self.cur_bank*16] = value
	
	def SetCurStep(self,val):
		self.cur_step = val
		
	def IncCurStep(self):
		self.cur_step = self.cur_step + 1
		self.cur_step = self.cur_step % self.seq_length
		
	
	
	
	def Panic(self):
		if(not self.midi_output is None):
			self.midi_output.send(MSG([0x80+self.midi_channel,self.note,127]))
		
	def Save(self,mid):
		track = MidiTrack()
		mid.tracks.append(track)
		
		for i in range(self.num_steps):
			
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
				
	def Load(self):
		pass		



	def Transpose(self,value):
		
		for i in range(self.num_steps):
			self.notes[i] = self.notes[i] + value
			if(self.notes[i] < 0): self.notes[i] = 0
			if(self.notes[i] > 127): self.notes[i] = 127
			
	
			
	def Randomize(self):
		seq = []
		for i in range(self.num_steps/16):
			seq = seq + GEN_CreatePattern(GEN_TYPE_RANDOM)
		
		seq = SEQ_UpDown(seq)
				
		for i in range(self.num_steps):			
			seq[i] = seq[i] + 36
			if(seq[i] < 24): seq[i] = 24
			if(seq[i] > 80): seq[i] = 80
			self.notes[i] = seq[i]
			self.ppq[i] = 6
			self.repeats[i] = 0
			self.rests[i] = 0
			
	def RandomizePPQ(self):
		for i in range(self.num_steps):
			self.ppq[i] = choice([1,3,6,12,24])
		
	def RandomizeRests(self):
		for i in range(self.num_steps):
			self.rests[i] = randint(0,1)
			
	def RandomizeRepeats(self):
		for i in range(self.num_steps):
			self.repeats[i] = randint(0,7)
	
	def Pickle(self,filename):
		pickle.dump( self, open(filename,'wb') )
		
	def Unpickle(self,filename):
		self = pickle.load( open(filename,'rb'))

	def Copy(self, c):
		self.notes = c.notes[:]
		self.ppq = c.ppq[:]
		self.repeats = c.repeats[:]
		self.rests = c.rests[:]		
		self.seq_length = c.seq_length
		self.cur_step = c.cur_step
		self.num_steps = c.num_steps
		self.cur_ppq = c.cur_ppq
		self.cur_repeats = c.cur_repeats
		self.rest = c.rest
		self.note = c.note
		self.midi_channel = c.midi_channel
		
	def GetNote(self,step):
		return self.notes[step+self.cur_bank*16]
		
	def GetPPQ(self,step):
		return self.ppq[step+self.cur_bank*16]		
		
	def GetRepeat(self,step):
		return self.repeats[step+self.cur_bank*16]		
	
	def GetRest(self,step):
		return self.rests[step+self.cur_bank*16]
	
	def SetPort(self,port):
		self.midi_output = port
		
	def SetChannel(self,ch):
		self.midi_channel = ch
		
	def ShiftLeft(self,n=1):
		o = self.notes[:]
		
		for i in range(n):
			x = o.pop(0)
			o.append(x)
			
		self.notes = o[:]
		
	def ShiftRight(self,n=1):
		o = self.notes[:]
		for i in range(n):
			x = o.pop()
			o.insert(0,x)
			
		self.notes = o[:]
	
	def ShiftRandom(self,n=1):
		for i in range(n):
			if(random() < 0.5): self.ShiftLeft(1)
			else: self.ShiftRight(1)
			
	def ShiftPPQLeft(self,n=1):
		o = self.ppq[:]
		t = [6,12,24,48]
		
		for i in range(n):
			x = o.pop(0)
			o.append(choice(t))
			
		self.ppq = o[:]
		
	def ShiftPPQRight(self,n=1):
		o = self.ppq[:]
		t = [6,12,24,48]
		
		for i in range(n):
			x = o.pop()
			o.insert(0,choice(t))
			
		self.ppq = o[:]
	
	def ShiftPPQRandom(self,n=1):
		for i in range(n):
			if(random() < 0.5): self.ShiftPPQLeft(1)
			else: self.ShiftPPQRight(1)
			
	def Transpose(self,oct):
		
		for i in range(self.num_steps):
			self.notes[i] = self.notes[i] + oct
		
	def HalfNotes(self):				
		for i in range(0,self.num_steps):
			self.ppq[i] = 48
	
	def QuarterNotes(self):				
		for i in range(0,self.num_steps):
			self.ppq[i] = 24
		
	def EigthNotes(self):				
		for i in range(0,self.num_steps):
			self.ppq[i] = 12
			
	def SixteenthNotes(self):				
		for i in range(0,self.num_steps):
			self.ppq[i] = 6
	
	def SetSteps(self,steps):
		
		if(steps > self.num_steps):
			self.Resize(steps)
			
		self.num_steps = steps
		
	def ClosePort(self):
		if(not self.midi_output is None):
			self.midi_output.close()
			self.midi_output = None
			
	def Variation(self,voice):
		notes = voice.notes[:]
		out    = []
		while len(notes) > 0:
			i = randint(0,len(notes)-1)
			out.append(notes[i])
			del notes [i]
		self.notes = out[:]
			
	def Reset(self):
		v = self
		v.cur_step = 0
		v.rest  = v.rests[v.cur_step]
		v.note = v.notes[v.cur_step]
		v.cur_repeats = v.repeats[v.cur_step]
		v.cur_ppq = v.ppq[v.cur_step]
		
	def Roll(self,num):
		for i in range(num):
			x1 = randint(0,self.num_steps-1)
			x2 = randint(0,self.num_steps-1)
			t   = self.notes[x1]
			self.notes[x1] = self.notes[x2]
			self.notes[x2] = t
			
	def SetBank(self,bank):
		self.cur_bank = bank

	
	def Resize(self,steps):				
		self.SetNumSteps(steps)
		self.Randomize()
		
		
	def SetNumSteps(self,num):		
		self.num_steps = num
		self.seq_length = num
		self.notes = [0]*num
		self.ppq   = [0]*num
		self.repeats = [0]*num
		self.rests = [0]*num
		
	def Init(self,banks,channel):
		self.Resize(banks*16)
		self.midi_channel = channel
		
	def UpdateMIDIInput(self,key):
		self.notes[self.cur_instep] = key[1]
		self.cur_instep = self.cur_instep + 1
		self.cur_instep = self.cur_instep % self.num_steps
		
class Voices:
	
	
	def __init__(self, num_banks=1, num=MAX_SEQS, max = MAX_SEQS):
		
		self.voices      = [0]*max
		self.cur_voice = 0
		self.num_voices = num
		self.bActivated = True
		
		for i in range(max):
			self.voices[i] = Voice(num_banks*16)
			
	def Init(self,voices,banks,channel):
		self.midi_channel = channel
		self.num_voices = voices
		self.num_banks = banks
		
		for i in range(voices):
			self.voices[i].Init(banks,channel)
			
		
	def GetVoice(self):
		return self.voices[self.cur_voice]

		
	def SetChannel(self,ch):
		self.midi_channel = ch
		for i in range(self.num_voices):
			self.voices[i].SetChannel(ch)
			
	def SetVoice(self,v):
		if(v < 0): v = 0
		if(v >= self.num_voices): v = self.num_voices
		
		self.cur_voice = v
		voice = self.GetVoice()
		
	def CloseMidiPort(self):
		voice = self.GetVoice()
		voice.ClosePort()
		
	def Copy(self,c):
		c.Copy(self.voices[self.cur_voice])
		return c
				
	def GetNote(self,step):
		voice = self.GetVoice()
		return voice.GetNote(step)
		
	def GetPPQ(self,step):
		voice = self.GetVoice()
		return voice.GetPPQ(step)
	
	def GetRest(self,step):
		voice = self.GetVoice()
		return voice.GetRest(step)
	
	def GetRepeat(self,step):
		voice = self.GetVoice()
		return voice.GetRepeat(step)
	
	def Paste(self,c):
		voice = self.GetVoice()
		voice.Copy(c)
				
	def Reset(self):
		for i in range(self.num_voices):
			voice = self.voices[i]
			voice.Reset()
	
	
	def Randomize(self):
		voice = self.GetVoice()
		voice.Randomize()
		
	def RandomizePPQ(self):
		voice = self.GetVoice()
		voice.RandomizePPQ()
		
	def RandomizeRests(self):
		voice = self.GetVoice()
		voice.RandomizeRests()
		
		
	def RandomizeRepeats(self):
		voice = self.GetVoice()
		voice.RandomizeRepeats()
	
	def Resize(self,size):
		
		for i in range(self.num_voices):
			voice = self.voices[i]		
			voice.Resize(size)
	
	def SetNumSteps(self,steps):
		voice = self.GetVoice()
		voice.SetSteps(steps)
	
	def SetBank(self,bank):
		self.cur_bank = bank
		voice = self.GetVoice()
		voice.SetBank(bank)
	
	def SetNumSteps(self,num):
		voice = self.GetVoice()
		voice.SetSteps(num)
	
	def SetNumVoices(self,num):
		self.num_voices = num
		
		
	def SetNumBanks(self,num):
		for i in range(self.num_voices):
			voice = self.voices[i]
			voice.SetSteps(num*16)
	
	
	def SetMidiChannel(self,ch):
		voice = self.GetVoice()
		voice.SetChannel(ch)
	
	def SetMidiPort(self,port):
		voice = self.GetVoice()
		voice.SetOutput(port)
		
	def SetNote(self,step,note):
		voice = self.GetVoice()
		voice.SetNote(step,note)
		
	def SetPPQ(self,step,value):
		voice = self.GetVoice()
		voice.SetPPQ(step,value)
		
		
	def SetRest(self,step,value):
		voice = self.GetVoice()
		voice.SetRest(step,value)
	
	def SetRepeat(self,step,value):
		voice = self.GetVoice()
		voice.SetRepeat(step,value)
	
	
	def ShiftLeft(self,n=1):
		voice = self.GetVoice()
		voice.ShiftLeft(n)

	def ShiftRight(self,n=1):
		voice = self.GetVoice()
		voice.ShiftRight(n)
	
	def ShiftRandom(self,n=1):
		voice = self.GetVoice()
		voice.ShiftRandom(n)
	
	def StopNotes(self):
		for i in range(self.num_voices):
			self.voices[i].StopNotes()
	
	def Transpose(self,value):
		voice = self.GetVoice()
		voice.Transpose(value)
		
			
	def Variation(self,seq):
		self.num_voices = seq.num_voices	
		for i in range(seq.num_voices):
			self.voices[i].Variation(seq.voices[i])
	
	
	
	def HalfNotes(self):
		for i in range(self.num_voices):
			self.voices[i].HalfNotes()
	
	def QuarterNotes(self):
		for i in range(self.num_voices):
			self.voices[i].QuarterNotes()
				
	def EightNotes(self):
		for i in range(self.num_voices):
			self.voices[i].EigthNotes()
	
	def SixteenthNotes(self):
		for i in range(self.num_voices):
			self.voices[i].SixteenthNotes()
	
	
# sequencer holds all sequence data
class Sequencer:

	def __init__(self):
		
		
		self.seqs = []
		self.copy_seq = None
		
		for i in range(8):
			self.seqs.append(Voices())
			
		self.num_sequencers = 8
		self.num_banks = 1		
		self.mainwindow = None			
		self.cur_var   = 0
		
		self.midi_channel = 0
		self.midi_port = None
		
		self.bStopped = False
		self.next_var  = 0
		
		self.midi_output = None
		
		self.transpose_step = 0
		self.transpose_repeat = 0
		
		self.start_ppq = 0
		self.motion = None
		self.bActivated = False
	
	
	def SaveMidi(self, filename):		
		#mid = MidiFile()
		#mid.ticks_per_beat = 24
		#for i in range(self.num_sequencers):
		#	for j in range(self.sequencers[i].num_voices):
		#		self.sequencers[i].voices[j].SaveMidi(mid)
		#mid.save(str(filename))
		pass
		
	def LoadPickle(self,filename):
		#self = pickle.load(open(filename,'rb'))
		pass
		
	def SavePickle(self, filename):
		#pickle.dump(self, open(filename,'wb'))
		pass
			
			
	def ChangeVar(self,var):
		self.next_var = var
		
		
	def ChangeVoice(self,voice):
		cvoice = self.GetCurrentVoice()		
		cvoice.SetVoice(voice)
		
	def Copy(self):
		self.copy_seq = Voice()
		voice = self.GetCurrentVoice()		
		self.copy_seq = voice.Copy()
		
	def DoMatrix(self):
		seq = self.GetCurrentSeq()
		v = seq.GetVoice()
		
		if(self.parent.chkMatrix.isChecked()):
			n = 0
			if(self.parent.rbMatrix1.isChecked()):
				n = 0
			elif(self.parent.rbMatrix2.isChecked()):
				n = 1
			elif(self.parent.rbMatrix3.isChecked()):
				n = 2
			elif(self.parent.rbMatrix4.isChecked()):
				n = 3
			elif(self.parent.rbMatrix5.isChecked()):
				n = 4
			elif(self.parent.rbMatrix6.isChecked()):
				n = 5
			elif(self.parent.rbMatrix7.isChecked()):
				n = 6
			elif(self.parent.rbMatrix8.isChecked()):
				n = 7
			
			
			v.Roll(n+1)
		
		if(self.parent.chkShiftCore.isChecked()):
			n = 1
			if(self.parent.rbShift1.isChecked()):
				n1 = 1
			elif(self.parent.rbShift2.isChecked()):
				n1 = 2
			elif(self.parent.rbShiftR.isChecked()):
				n1 = -1
			if(self.parent.rbShift3.isChecked()):
				n1 = 3
			elif(self.parent.rbShift5.isChecked()):
				n1 = 5
			
			n2 = 0
			if(self.parent.rbShift8.isChecked()):
				n2 = 8
			elif(self.parent.rbShift13.isChecked()):
				n2 = 13
			elif(self.parent.rbShift21.isChecked()):
				n2 = 21
			elif(self.parent.rbShift34.isChecked()):
				n2 = 34
			elif(self.parent.rbShift55.isChecked()):
				n2 = 55
									
			if(n1 == -1):
				n1 = randint(0,99)
			
			n1 = n1 + n2
			if(self.parent.rbLeft.isChecked()):				
				v.ShiftLeft(n)
			elif(self.parent.rbRight.isChecked()):
				v.ShiftRight(n)
			elif(self.parent.rbRandom.isChecked()):
				v.ShiftRandom(n)
				
		if(self.parent.chkTranspose.isChecked()):
			self.transpose_repeat = self.transpose_repeat - 1
			if(self.transpose_repeat <= 0):
				self.transpose_step = self.transpose_step + 1
				self.transpose_step = self.transpose_step % 8
				trans = False
				if(self.parent.chkTranspose1.isChecked() and self.transpose_step == 0):
					trans = True
					t = self.parent.sbTransOct1.value()
					self.transpose_repeat = self.parent.sbTransRep1.value()
				elif(self.parent.chkTranspose2.isChecked() and self.transpose_step == 1):
					t = self.parent.sbTransOct2.value()
					trans = True
					self.transpose_repeat = self.parent.sbTransRep2.value()
				elif(self.parent.chkTranspose3.isChecked() and self.transpose_step == 2):
					trans = True
					t = self.parent.sbTransOct3.value()
					self.transpose_repeat = self.parent.sbTransRep3.value()
				elif(self.parent.chkTranspose4.isChecked() and self.transpose_step == 3):
					t = self.parent.sbTransOct4.value()
					self.transpose_repeat = self.parent.sbTransRep4.value()
					trans = True
				elif(self.parent.chkTranspose5.isChecked() and self.transpose_step == 4):
					trans = True
					t = self.parent.sbTransOct5.value()
					self.transpose_repeat = self.parent.sbTransRep5.value()
				elif(self.parent.chkTranspose6.isChecked() and self.transpose_step == 5):
					t = self.parent.sbTransOct6.value()
					self.transpose_repeat = self.parent.sbTransRep6.value()
					trans = True
				elif(self.parent.chkTranspose7.isChecked() and self.transpose_step == 6):
					trans = True
					t = self.parent.sbTransOct7.value()
					self.transpose_repeat = self.parent.sbTransRep7.value()
				elif(self.parent.chkTranspose8.isChecked() and self.transpose_step == 7):
					t = self.parent.sbTransOct8.value()
					self.transpose_repeat = self.parent.sbTransRep8.value()
					trans = True
				
				if(trans == True):
					v.Transpose(t)
		
		
	def GenerateVariations(self):
		seqA = self.seqs[0]
		for i in range(1,8):
			self.seqs[i].Variation(seqA)
		
	def GetCurrentSeq(self):
		return self.seqs[self.cur_var]
		
	def GetCurrentVoice(self):
		return self.seqs[self.cur_var]
		
	def GetNote(self,step):
		voice = self.GetCurrentVoice()		
		return voice.GetNote(step)
		
	def GetPPQ(self,step):
		voice = self.GetCurrentVoice()		
		return voice.GetPPQ(step)
		
		
	def GetRepeat(self,step):
		voice = self.GetCurrentVoice()		
		return voice.GetRepeat(step)
		
		
	def GetRest(self,step):
		voice = self.GetCurrentVoice()		
		return voice.GetRest(step)
		
	def Init(self, voices, banks, channel):
		self.midi_channel = channel
		self.num_banks = banks
		self.num_voices = voices
		
		for i in range(8):
			self.seqs[i] = Voices(banks,voices)
			
		
	def Panic(self):
		midi_input, midi_output = MIDI_GetInOut()
		for i in range(127):
			midi_output.send(MSG([0x80+self.midi_channel,i,127]))
		
	def Paste(self):
		voice = self.GetCurrentVoice()		
		voice.Paste(self.copy_seq)
		
	def Randomize(self):
		voice = self.GetCurrentVoice()		
		voice.Randomize()			
	
	def RandomizePPQ(self):
		voice = self.GetCurrentVoice()		
		voice.RandomizePPQ()
		
		
	def RandomizeRests(self):
		voice = self.GetCurrentVoice()		
		voice.RandomizeRests()
		
	def RandomizeRepeats(self):
		voice = self.GetCurrentVoice()		
		voice.RandomizeRepeats()
			
	def Resize(self,num_voices):
		self.num_banks = num_voices
		for s in self.seqs:
			s.Resize(self.num_banks)
	
	def SetNote(self,step,value):
		voice = self.GetCurrentVoice()		
		voice.SetNote(step,value)
		
	def SetPPQ(self,step,value):
		voice = self.GetCurrentVoice()		
		voice.SetPPQ(step,value)
	
	
	def SetRest(self,step,value):
		voice = self.GetCurrentVoice()		
		voice.SetPPQ(step,value)
		
	def SetRepeat(self,step,value):
		voice = self.GetCurrentVoice()		
		voice.SetRepeat(step,value)
	
	def ShiftLeft(self):
		seq = self.GetCurrentSeq()
		seq.ShiftLeft()
		
	def ShiftLeft(self):
		seq = self.GetCurrentSeq()
		seq.ShiftRight()
	
	def SetNumSeqs(self,n):
		self.num_sequencers = n
		for i in range(8):			
			self.seqs[i].SetNumVoices(n)
		
	def SetNumRows(self,num):
		self.num_rows = num
		for i in range(8):			
			self.seqs[i].SetNumBanks(num)
		
	def SetMidiChannel(self,ch):
		self.midi_channel = ch
		for i in range(8):
			self.seqs[i].SetMidiChannel(ch)
	
	def SetMidiPort(self,port):
		for i in range(8):
			self.seqs[i].SetMidiOutput(port)
		
		
	def StopNotes(self):
		seq = self.GetCurrentSeq()
		seq.StopNotes()
		
	def SetBank(self,bank):
		self.cur_bank = bank
		seq = self.GetCurrentSeq()
		seq.SetBank(bank)
		
	def SetNumSteps(self,num):
		seq = self.GetCurrentSeq()
		seq.SetNumSteps(num)
		
	def SetNoteStep(self,step,note):
		seq = self.GetCurrentSeq()
		
		voice = seq.GetVoice()		
		voice.SetNoteStep(step,note)


	def Transpose(self,value):
		voice = self.GetCurrentVoice()		
		voice.Transpose(value)
	
	def Update(self,ppq):
		
		if(self.midi_output is None):
			self.midi_input,self.midi_output = MIDI_GetInOut()

		i = 0
		seq = self.GetCurrentSeq()
		
		for v in seq.voices:
			if(v.cur_ppq == 0): v.cur_ppq = 6
			
				
			if(v.reset==True):
				v.reset = False
				self.midi_output.send(MSG([0x80+self.midi_channel,v.last_note,127]))						
				self.midi_output.send(MSG([0x90+self.midi_channel,v.note,127]))
				v.last_note = v.note
				
			if(ppq % v.cur_ppq == 0):	
				
														
				v.cur_repeats = v.cur_repeats - 1
				
				

				
				if(v.cur_repeats < 0):
					v.cur_step = v.cur_step + 1				
					self.midi_output.send(MSG([0x80+self.midi_channel,v.last_note,127]))						
					self.midi_output.send(MSG([0x80+self.midi_channel,v.note,127]))						
									
					if(v.cur_step >= v.num_steps): 
						self.DoMatrix()										
						self.cur_var = self.next_var						
						v.Reset()
						
					else:
						v.cur_step = v.cur_step % v.num_steps																	
						v.rest  = v.rests[v.cur_step]
						
						v.note = v.notes[v.cur_step]
						v.cur_repeats = v.repeats[v.cur_step]
						v.cur_ppq = v.ppq[v.cur_step]					
				if(v.rest != 1):
					self.last_note = v.note
					self.midi_output.send(MSG([0x90+self.midi_channel,v.note,127]))
				
		
			i = i + 1
			if(i >= seq.num_voices): break
			
		
	
	def HalfNotes(self):
		seq = self.GetCurrentSeq()
		voice = seq.GetVoice()
		voice.HalfNotes()
				
	def QuarterNotes(self):
		seq = self.GetCurrentSeq()
		voice = seq.GetVoice()
		voice.QuarterNotes()
	
	def EigthNotes(self):
		seq = self.GetCurrentSeq()
		voice = seq.GetVoice()
		voice.EigthNotes()
	
	def SixteenthNotes(self):
		seq = self.GetCurrentSeq()
		voice = seq.GetVoice()
		voice.SixteenthNotes()
	
		
	
	def CloseMidiPort(self):
		pass
		
	def ChangeBanks(self,banks):
		self.num_banks= banks
		seq = self.GetCurrentSeq()
		for i in range(seq.num_voices):
			seq.voices[i].SetNumSteps(banks*16)
			
	def ChangeVoices(self,voices):
		self.num_voices = voices
		seq = self.GetCurrentSeq()
		seq.num_voices = voices
		for i in range(voices):
			seq.voices[i] = Voice()
			seq.voices[i].Init(self.num_banks,self.midi_channel)
		
			
	def Activate(self):
		self.bActivated = True
	
	
	def UpdateMIDIInput(self,key):
		seq = self.GetCurrentSeq()
		v    = seq.GetVoice()		
		v.UpdateMIDIInput(key)
		
class MotionData:
	
	def __init__(self,parent):
		
		self.measures = 0
		self.CC = [0]*16
		self.Motions = {}
		
		self.cur_tick = 0
		self.ticks     = 0
		self.bRecording = False
		self.parent = parent
		self.Init(16)
		self.last_capture = 0
		self.last_sample = 0.0
		
	def Init(self,steps):
		self.ticks = steps*24
		for i in range(16):
			self.Motions[i] = [0]*self.ticks
			
	def Update(self,ppq,midi_channel):
		self.ppq = ppq
		midi_input, midi_output = MIDI_GetInOut()
		msg = [0xB0+midi_channel,0,0]
		self.cur_tick = self.cur_tick + 1
		self.cur_tick = self.cur_tick % self.ticks
		
		self.CC[0] = self.parent.sbCC1.value()
		self.CC[1] = self.parent.sbCC2.value()
		self.CC[2] = self.parent.sbCC3.value()
		self.CC[3] = self.parent.sbCC4.value()
		self.CC[4] = self.parent.sbCC5.value()
		self.CC[5] = self.parent.sbCC6.value()
		self.CC[6] = self.parent.sbCC7.value()
		self.CC[7] = self.parent.sbCC8.value()
		self.CC[8] = self.parent.sbCC9.value()
		self.CC[9] = self.parent.sbCC10.value()
		self.CC[10] = self.parent.sbCC11.value()
		self.CC[11] = self.parent.sbCC12.value()
		self.CC[12] = self.parent.sbCC13.value()
		self.CC[13] = self.parent.sbCC14.value()
		self.CC[14] = self.parent.sbCC15.value()
		self.CC[15] = self.parent.sbCC16.value()
		
		
		if(self.bRecording == True):			
			for i in range(16):
				msg[1] = self.CC[i]
				msg[2] = self.Motions[i][self.cur_tick]
				midi_output.send(MSG(msg))
		
		
	def ControlCapture(self,control,value):
		n = abs(self.cur_tick - self.last_capture)
		n = n+1
		for i in range(1,n):
			x = 1.0 / float(i)
			v = (1.0-x)*self.last_sample + x*self.last_sample
			self.Motions[control][(self.last_capture+i) % self.ticks] = int(v*127.0)
		
		self.last_sample = value/127.0
		self.last_capture = self.cur_tick
		
	def Clear(self):
		for i in range(16):
			self.Motions[i] = [0]*self.ticks
	
				
		
###############################################################################
# GUI
###############################################################################

# thread for handling MIDI i/o		
class Worker(QtCore.QThread):
	
	def __init__(self,mainwindow,parent=None):
		QtCore.QThread.__init__(self,parent)
		self.exiting = False
		self.mainwindow = mainwindow
		self.scene_len = PLAY_LEN
		self.ppq = -1
		self.cur_ppq = -1
		self.input_buffer = [0]*256
		self.cur_step = 0
		self.note = 0
		self.repeats = 0
		self.cur_note = 0
		self.rest = 0
		self.midi_channel = MIDI_CHANNEL
		self.kb_channel    = MIDIKB_CHANNEL
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
				if(self.mainwindow.bStopped == True): continue
				
				if(key[0] == 248):
					self.ppq = self.ppq+1					
					self.mainwindow.motion.Update(self.ppq,self.midi_channel)
					seq = self.mainwindow.GetSequencer()
					seq.Update(self.ppq)
					sync = MIDI_GetSyncPorts()
					if(not sync is None): sync.send(msg)
							
				elif(key[0] >= 0x90 and key[0] <= 0x9F):
					
					if(key[0] == 0x90 + self.kb_channel):
						self.start_ppq = self.ppq
						note = key[1]
						if(note < 0): note = 0
						seq = self.mainwindow.GetSequencer()												
						seq.SetNoteStep(self.cur_note,note)
						self.key_ppq[key[1]] = self.ppq
						self.key_last[key[1]] = self.cur_note
						self.cur_note = self.cur_note + 1
						self.cur_note = self.cur_note % self.num_steps 
						self.emit(QtCore.SIGNAL("UpdateUi()"))
						
				#elif(key[0] >= 0x80 and key[0] <= 0x8F):
				#	if(key[0] == 0x80 + self.kb_channel):	
				#		ppq = self.ppq - self.key_ppq[key[1]]						
				#		seq = self.mainwindow.GetSequencer()
				#		seq.SetPPQ(self.key_last[key[1]],ppq)
						
						
				self.midi_output.send(msg)

class Ui_SyncDialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(295, 212)
		self.buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.buttonBox.setGeometry(QtCore.QRect(70, 170, 211, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(30, 20, 61, 16))
		self.label.setObjectName(_fromUtf8("label"))
		self.widget = QtGui.QWidget(Dialog)
		self.widget.setGeometry(QtCore.QRect(40, 50, 241, 111))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.widget)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.chkPort1 = QtGui.QCheckBox(self.widget)
		self.chkPort1.setObjectName(_fromUtf8("chkPort1"))
		self.horizontalLayout.addWidget(self.chkPort1)
		self.cbPort1 = QtGui.QComboBox(self.widget)
		self.cbPort1.setObjectName(_fromUtf8("cbPort1"))
		self.horizontalLayout.addWidget(self.cbPort1)
		self.verticalLayout.addLayout(self.horizontalLayout)
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.chkPort2 = QtGui.QCheckBox(self.widget)
		self.chkPort2.setObjectName(_fromUtf8("chkPort2"))
		self.horizontalLayout_2.addWidget(self.chkPort2)
		self.cbPort2 = QtGui.QComboBox(self.widget)
		self.cbPort2.setObjectName(_fromUtf8("cbPort2"))
		self.horizontalLayout_2.addWidget(self.cbPort2)
		self.verticalLayout.addLayout(self.horizontalLayout_2)
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.chkPort3 = QtGui.QCheckBox(self.widget)
		self.chkPort3.setObjectName(_fromUtf8("chkPort3"))
		self.horizontalLayout_3.addWidget(self.chkPort3)
		self.cbPort3 = QtGui.QComboBox(self.widget)
		self.cbPort3.setObjectName(_fromUtf8("cbPort3"))
		self.horizontalLayout_3.addWidget(self.cbPort3)
		self.verticalLayout.addLayout(self.horizontalLayout_3)
		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.chkPort4 = QtGui.QCheckBox(self.widget)
		self.chkPort4.setObjectName(_fromUtf8("chkPort4"))
		self.horizontalLayout_4.addWidget(self.chkPort4)
		self.cbPort4 = QtGui.QComboBox(self.widget)
		self.cbPort4.setObjectName(_fromUtf8("cbPort4"))
		self.horizontalLayout_4.addWidget(self.cbPort4)
		self.verticalLayout.addLayout(self.horizontalLayout_4)

		outp= mido.get_output_names()
		for i in outp:
			self.cbPort1.addItem(i)
			self.cbPort2.addItem(i)
			self.cbPort3.addItem(i)
			self.cbPort4.addItem(i)

		
		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.Accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.Reject)
		self.dlg = Dialog
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label.setText(_translate("Dialog", "Sync Ports", None))
		self.chkPort1.setText(_translate("Dialog", "Port 1", None))
		self.chkPort2.setText(_translate("Dialog", "Port 2", None))
		self.chkPort3.setText(_translate("Dialog", "Port 3", None))
		self.chkPort4.setText(_translate("Dialog", "Port 4", None))

	def Accept(self):
		clk1 = None
		clk2 = None
		clk3 = None
		clk4 = None
		
		if(self.chkPort1.isChecked()):
			clk1 = mido.open_output(self.cbPort1.currentText())
		if(self.chkPort2.isChecked()):
			clk2 = mido.open_output(self.cbPort2.currentText())
		if(self.chkPort3.isChecked()):
			clk3 = mido.open_output(self.cbPort3.currentText())
		if(self.chkPort4.isChecked()):
			clk4 = mido.open_output(self.cbPort4.currentText())
		
		syncs = []
		if(not clk1 is None): syncs.append(clk1)
		if(not clk2 is None): syncs.append(clk2)
		if(not clk3 is None): syncs.append(clk3)
		if(not clk4 is None): syncs.append(clk4)
		
		if(len(syncs)> 0): MIDI_SetSyncPorts(syncs)
		self.dlg.close()
		
	def Reject(self):
		self.dlg.close()
		
		
class Ui_PNameDialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(400, 113)
		self.buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.buttonBox.setGeometry(QtCore.QRect(40, 60, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(10, 30, 71, 16))
		self.label.setObjectName(_fromUtf8("label"))
		self.textEdit = QtGui.QTextEdit(Dialog)
		self.textEdit.setGeometry(QtCore.QRect(90, 30, 291, 21))
		self.textEdit.setObjectName(_fromUtf8("textEdit"))
		self.sbRepeats = QtGui.QSpinBox(Dialog)
		self.sbRepeats.setGeometry(QtCore.QRect(90, 60, 50, 21))
		self.sbRepeats.setObjectName(_fromUtf8("textEdit"))
		self.sbRepeats.setMinimum(1)
		self.sbRepeats.setMaximum(99)
		
		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.Accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.Reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)
		self.dlg = Dialog
		
	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label.setText(_translate("Dialog", "Pattern Name", None))

	def Accept(self):
		self.pname= str(self.textEdit.toPlainText())
		self.repeats = self.sbRepeats.value()
		self.cancel = False
		self.dlg.close()
		
	def Reject(self):
		self.cancel = True
		self.dlg.close()
		
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
	
# transpose dialog
class Ui_TransposeDialog(object):
	
	def setupUi(self, Dialog):
		self.dlg = Dialog
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(385, 114)
		self.buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.buttonBox.setGeometry(QtCore.QRect(10, 50, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
		self.label = QtGui.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(20, 20, 71, 16))
		self.label.setObjectName(_fromUtf8("label"))
		self.spinBox = QtGui.QSpinBox(Dialog)
		self.spinBox.setGeometry(QtCore.QRect(100, 20, 42, 22))
		self.spinBox.setObjectName(_fromUtf8("spinBox"))
		self.spinBox.setMinimum(-80)
		self.spinBox.setMaximum(80)
		
		self.retranslateUi(Dialog)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
		self.label.setText(_translate("Dialog", "Semitones", None))

	def accept(self):
		self.mainwindow.Transpose(self.spinBox.value())
		self.dlg.close()
		
	def reject(self):
		self.dlg.close()
		

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(974, 511)
        MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(80, 80, 80);\n"
"color: rgb(255, 255, 255);\n"
"QMenuBar {\n"
"         background-color: blue;\n"
"        }\n"
"\n"
"     QMenuBar::item {\n"
"         background: blue;\n"
"     }"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(830, 10, 64, 23))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.pbStart = QtGui.QPushButton(self.centralwidget)
        self.pbStart.setGeometry(QtCore.QRect(750, 10, 75, 23))
        self.pbStart.setObjectName(_fromUtf8("pbStart"))
        self.cbNote15 = QtGui.QComboBox(self.centralwidget)
        self.cbNote15.setGeometry(QtCore.QRect(850, 60, 61, 22))
        self.cbNote15.setObjectName(_fromUtf8("cbNote15"))
        self.cbNote1 = QtGui.QComboBox(self.centralwidget)
        self.cbNote1.setGeometry(QtCore.QRect(10, 60, 61, 22))
        self.cbNote1.setObjectName(_fromUtf8("cbNote1"))
        self.cbNote8 = QtGui.QComboBox(self.centralwidget)
        self.cbNote8.setGeometry(QtCore.QRect(430, 60, 61, 22))
        self.cbNote8.setObjectName(_fromUtf8("cbNote8"))
        self.cbNote7 = QtGui.QComboBox(self.centralwidget)
        self.cbNote7.setGeometry(QtCore.QRect(370, 60, 61, 22))
        self.cbNote7.setObjectName(_fromUtf8("cbNote7"))
        self.cbNote12 = QtGui.QComboBox(self.centralwidget)
        self.cbNote12.setGeometry(QtCore.QRect(670, 60, 61, 22))
        self.cbNote12.setObjectName(_fromUtf8("cbNote12"))
        self.cbNote4 = QtGui.QComboBox(self.centralwidget)
        self.cbNote4.setGeometry(QtCore.QRect(190, 60, 61, 22))
        self.cbNote4.setObjectName(_fromUtf8("cbNote4"))
        self.cbNote16 = QtGui.QComboBox(self.centralwidget)
        self.cbNote16.setGeometry(QtCore.QRect(910, 60, 51, 22))
        self.cbNote16.setObjectName(_fromUtf8("cbNote16"))
        self.cbNote2 = QtGui.QComboBox(self.centralwidget)
        self.cbNote2.setGeometry(QtCore.QRect(70, 60, 61, 22))
        self.cbNote2.setObjectName(_fromUtf8("cbNote2"))
        self.cbNote11 = QtGui.QComboBox(self.centralwidget)
        self.cbNote11.setGeometry(QtCore.QRect(610, 60, 61, 22))
        self.cbNote11.setObjectName(_fromUtf8("cbNote11"))
        self.cbNote9 = QtGui.QComboBox(self.centralwidget)
        self.cbNote9.setGeometry(QtCore.QRect(490, 60, 61, 22))
        self.cbNote9.setObjectName(_fromUtf8("cbNote9"))
        self.cbNote13 = QtGui.QComboBox(self.centralwidget)
        self.cbNote13.setGeometry(QtCore.QRect(730, 60, 61, 22))
        self.cbNote13.setObjectName(_fromUtf8("cbNote13"))
        self.cbNote6 = QtGui.QComboBox(self.centralwidget)
        self.cbNote6.setGeometry(QtCore.QRect(310, 60, 61, 22))
        self.cbNote6.setObjectName(_fromUtf8("cbNote6"))
        self.cbNote5 = QtGui.QComboBox(self.centralwidget)
        self.cbNote5.setGeometry(QtCore.QRect(250, 60, 61, 22))
        self.cbNote5.setObjectName(_fromUtf8("cbNote5"))
        self.cbNote10 = QtGui.QComboBox(self.centralwidget)
        self.cbNote10.setGeometry(QtCore.QRect(550, 60, 61, 22))
        self.cbNote10.setObjectName(_fromUtf8("cbNote10"))
        self.cbNote3 = QtGui.QComboBox(self.centralwidget)
        self.cbNote3.setGeometry(QtCore.QRect(130, 60, 61, 22))
        self.cbNote3.setObjectName(_fromUtf8("cbNote3"))
        self.cbNote14 = QtGui.QComboBox(self.centralwidget)
        self.cbNote14.setGeometry(QtCore.QRect(790, 60, 61, 22))
        self.cbNote14.setObjectName(_fromUtf8("cbNote14"))
        self.sbVoices = QtGui.QSpinBox(self.centralwidget)
        self.sbVoices.setGeometry(QtCore.QRect(140, 20, 42, 22))
        self.sbVoices.setObjectName(_fromUtf8("sbVoices"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(290, 0, 24, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.sbVoice = QtGui.QSpinBox(self.centralwidget)
        self.sbVoice.setGeometry(QtCore.QRect(290, 20, 42, 22))
        self.sbVoice.setObjectName(_fromUtf8("sbVoice"))
        self.label_39 = QtGui.QLabel(self.centralwidget)
        self.label_39.setGeometry(QtCore.QRect(90, 0, 46, 13))
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.sbSteps = QtGui.QSpinBox(self.centralwidget)
        self.sbSteps.setGeometry(QtCore.QRect(340, 20, 42, 22))
        self.sbSteps.setObjectName(_fromUtf8("sbSteps"))
        self.sbChannel = QtGui.QSpinBox(self.centralwidget)
        self.sbChannel.setGeometry(QtCore.QRect(20, 20, 42, 22))
        self.sbChannel.setObjectName(_fromUtf8("sbChannel"))
        self.label_40 = QtGui.QLabel(self.centralwidget)
        self.label_40.setGeometry(QtCore.QRect(140, 0, 46, 13))
        self.label_40.setObjectName(_fromUtf8("label_40"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(240, 0, 18, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.sbRow = QtGui.QSpinBox(self.centralwidget)
        self.sbRow.setGeometry(QtCore.QRect(390, 20, 42, 22))
        self.sbRow.setObjectName(_fromUtf8("sbRow"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(340, 0, 34, 14))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.sbSeq = QtGui.QSpinBox(self.centralwidget)
        self.sbSeq.setGeometry(QtCore.QRect(240, 20, 42, 22))
        self.sbSeq.setObjectName(_fromUtf8("sbSeq"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(390, 0, 51, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.sbBanks = QtGui.QSpinBox(self.centralwidget)
        self.sbBanks.setGeometry(QtCore.QRect(90, 20, 42, 22))
        self.sbBanks.setObjectName(_fromUtf8("sbBanks"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(20, 0, 45, 14))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.cbScale = QtGui.QComboBox(self.centralwidget)
        self.cbScale.setGeometry(QtCore.QRect(500, 20, 69, 22))
        self.cbScale.setObjectName(_fromUtf8("cbScale"))
        self.cbChord = QtGui.QComboBox(self.centralwidget)
        self.cbChord.setGeometry(QtCore.QRect(570, 20, 69, 22))
        self.cbChord.setObjectName(_fromUtf8("cbChord"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(640, 20, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.sbAlg = QtGui.QSpinBox(self.centralwidget)
        self.sbAlg.setGeometry(QtCore.QRect(450, 20, 42, 22))
        self.sbAlg.setMaximum(6)
        self.sbAlg.setObjectName(_fromUtf8("sbAlg"))
        self.chkStep1 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1.setGeometry(QtCore.QRect(80, 220, 29, 17))
        self.chkStep1.setObjectName(_fromUtf8("chkStep1"))
        self.chkStep1_2 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_2.setGeometry(QtCore.QRect(115, 220, 29, 17))
        self.chkStep1_2.setObjectName(_fromUtf8("chkStep1_2"))
        self.chkStep1_3 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_3.setGeometry(QtCore.QRect(150, 220, 29, 17))
        self.chkStep1_3.setObjectName(_fromUtf8("chkStep1_3"))
        self.chkStep1_4 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_4.setGeometry(QtCore.QRect(185, 220, 29, 17))
        self.chkStep1_4.setObjectName(_fromUtf8("chkStep1_4"))
        self.chkStep1_5 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_5.setGeometry(QtCore.QRect(290, 220, 29, 17))
        self.chkStep1_5.setObjectName(_fromUtf8("chkStep1_5"))
        self.chkStep1_6 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_6.setGeometry(QtCore.QRect(220, 220, 29, 17))
        self.chkStep1_6.setObjectName(_fromUtf8("chkStep1_6"))
        self.chkStep1_7 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_7.setGeometry(QtCore.QRect(255, 220, 29, 17))
        self.chkStep1_7.setObjectName(_fromUtf8("chkStep1_7"))
        self.chkStep1_8 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_8.setGeometry(QtCore.QRect(325, 220, 29, 17))
        self.chkStep1_8.setObjectName(_fromUtf8("chkStep1_8"))
        self.chkStep1_9 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_9.setGeometry(QtCore.QRect(600, 220, 35, 17))
        self.chkStep1_9.setObjectName(_fromUtf8("chkStep1_9"))
        self.chkStep1_10 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_10.setGeometry(QtCore.QRect(559, 220, 35, 17))
        self.chkStep1_10.setObjectName(_fromUtf8("chkStep1_10"))
        self.chkStep1_11 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_11.setGeometry(QtCore.QRect(436, 220, 35, 17))
        self.chkStep1_11.setObjectName(_fromUtf8("chkStep1_11"))
        self.chkStep1_12 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_12.setGeometry(QtCore.QRect(641, 220, 35, 17))
        self.chkStep1_12.setObjectName(_fromUtf8("chkStep1_12"))
        self.chkStep1_13 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_13.setGeometry(QtCore.QRect(360, 220, 29, 17))
        self.chkStep1_13.setObjectName(_fromUtf8("chkStep1_13"))
        self.chkStep1_14 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_14.setGeometry(QtCore.QRect(395, 220, 35, 17))
        self.chkStep1_14.setObjectName(_fromUtf8("chkStep1_14"))
        self.chkStep1_15 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_15.setGeometry(QtCore.QRect(477, 220, 35, 17))
        self.chkStep1_15.setObjectName(_fromUtf8("chkStep1_15"))
        self.chkStep1_16 = QtGui.QCheckBox(self.centralwidget)
        self.chkStep1_16.setGeometry(QtCore.QRect(518, 220, 35, 17))
        self.chkStep1_16.setObjectName(_fromUtf8("chkStep1_16"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(79, 249, 51, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.spinBox = QtGui.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(139, 249, 42, 22))
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 220, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.cbChord_2 = QtGui.QComboBox(self.centralwidget)
        self.cbChord_2.setGeometry(QtCore.QRect(259, 289, 69, 21))
        self.cbChord_2.setObjectName(_fromUtf8("cbChord_2"))
        self.cbScale_2 = QtGui.QComboBox(self.centralwidget)
        self.cbScale_2.setGeometry(QtCore.QRect(189, 289, 69, 22))
        self.cbScale_2.setObjectName(_fromUtf8("cbScale_2"))
        self.sbAlg_2 = QtGui.QSpinBox(self.centralwidget)
        self.sbAlg_2.setGeometry(QtCore.QRect(139, 289, 42, 22))
        self.sbAlg_2.setMaximum(6)
        self.sbAlg_2.setObjectName(_fromUtf8("sbAlg_2"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(84, 289, 51, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(679, 219, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(190, 250, 70, 17))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(190, 270, 46, 13))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(260, 270, 46, 13))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(70, 330, 46, 13))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 330, 51, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 360, 51, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(70, 360, 46, 13))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(130, 390, 51, 20))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.lineEdit_4 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(130, 420, 51, 20))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(70, 390, 46, 13))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_15 = QtGui.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(70, 420, 46, 13))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.lineEdit_5 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(270, 330, 51, 21))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.label_16 = QtGui.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(210, 420, 46, 13))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.lineEdit_6 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(270, 420, 51, 20))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.lineEdit_7 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(270, 360, 51, 20))
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.label_17 = QtGui.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(210, 390, 46, 13))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.lineEdit_8 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(270, 390, 51, 20))
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.label_18 = QtGui.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(210, 330, 46, 13))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.label_19 = QtGui.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(210, 360, 46, 13))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.checkBox_2 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(350, 250, 101, 17))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.spinBox_2 = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(460, 250, 42, 22))
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(350, 280, 70, 17))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(460, 310, 89, 134))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.radioButton_23 = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_23.setChecked(True)
        self.radioButton_23.setObjectName(_fromUtf8("radioButton_23"))
        self.verticalLayout_3.addWidget(self.radioButton_23)
        self.radioButton_24 = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_24.setObjectName(_fromUtf8("radioButton_24"))
        self.verticalLayout_3.addWidget(self.radioButton_24)
        self.radioButton_25 = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_25.setObjectName(_fromUtf8("radioButton_25"))
        self.verticalLayout_3.addWidget(self.radioButton_25)
        self.radioButton_26 = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_26.setObjectName(_fromUtf8("radioButton_26"))
        self.verticalLayout_3.addWidget(self.radioButton_26)
        self.radioButton_27 = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_27.setObjectName(_fromUtf8("radioButton_27"))
        self.verticalLayout_3.addWidget(self.radioButton_27)
        self.radioButton_28 = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_28.setObjectName(_fromUtf8("radioButton_28"))
        self.verticalLayout_3.addWidget(self.radioButton_28)
        self.checkBox_4 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(460, 280, 70, 17))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.layoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(570, 310, 89, 134))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.radioButton_29 = QtGui.QRadioButton(self.layoutWidget_2)
        self.radioButton_29.setChecked(True)
        self.radioButton_29.setObjectName(_fromUtf8("radioButton_29"))
        self.verticalLayout_4.addWidget(self.radioButton_29)
        self.radioButton_30 = QtGui.QRadioButton(self.layoutWidget_2)
        self.radioButton_30.setObjectName(_fromUtf8("radioButton_30"))
        self.verticalLayout_4.addWidget(self.radioButton_30)
        self.radioButton_31 = QtGui.QRadioButton(self.layoutWidget_2)
        self.radioButton_31.setObjectName(_fromUtf8("radioButton_31"))
        self.verticalLayout_4.addWidget(self.radioButton_31)
        self.radioButton_32 = QtGui.QRadioButton(self.layoutWidget_2)
        self.radioButton_32.setObjectName(_fromUtf8("radioButton_32"))
        self.verticalLayout_4.addWidget(self.radioButton_32)
        self.radioButton_33 = QtGui.QRadioButton(self.layoutWidget_2)
        self.radioButton_33.setObjectName(_fromUtf8("radioButton_33"))
        self.verticalLayout_4.addWidget(self.radioButton_33)
        self.radioButton_34 = QtGui.QRadioButton(self.layoutWidget_2)
        self.radioButton_34.setObjectName(_fromUtf8("radioButton_34"))
        self.verticalLayout_4.addWidget(self.radioButton_34)
        self.checkBox_5 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(570, 280, 70, 17))
        self.checkBox_5.setObjectName(_fromUtf8("checkBox_5"))
        self.layoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(670, 310, 89, 134))
        self.layoutWidget_3.setObjectName(_fromUtf8("layoutWidget_3"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.radioButton_35 = QtGui.QRadioButton(self.layoutWidget_3)
        self.radioButton_35.setChecked(True)
        self.radioButton_35.setObjectName(_fromUtf8("radioButton_35"))
        self.verticalLayout_5.addWidget(self.radioButton_35)
        self.radioButton_36 = QtGui.QRadioButton(self.layoutWidget_3)
        self.radioButton_36.setObjectName(_fromUtf8("radioButton_36"))
        self.verticalLayout_5.addWidget(self.radioButton_36)
        self.radioButton_37 = QtGui.QRadioButton(self.layoutWidget_3)
        self.radioButton_37.setObjectName(_fromUtf8("radioButton_37"))
        self.verticalLayout_5.addWidget(self.radioButton_37)
        self.radioButton_38 = QtGui.QRadioButton(self.layoutWidget_3)
        self.radioButton_38.setObjectName(_fromUtf8("radioButton_38"))
        self.verticalLayout_5.addWidget(self.radioButton_38)
        self.radioButton_39 = QtGui.QRadioButton(self.layoutWidget_3)
        self.radioButton_39.setObjectName(_fromUtf8("radioButton_39"))
        self.verticalLayout_5.addWidget(self.radioButton_39)
        self.radioButton_40 = QtGui.QRadioButton(self.layoutWidget_3)
        self.radioButton_40.setObjectName(_fromUtf8("radioButton_40"))
        self.verticalLayout_5.addWidget(self.radioButton_40)
        self.checkBox_6 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(670, 280, 70, 17))
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(450, 0, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_20 = QtGui.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(500, 0, 46, 13))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.label_21 = QtGui.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(570, 0, 46, 13))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.spinBox_3 = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_3.setGeometry(QtCore.QRect(820, 290, 42, 22))
        self.spinBox_3.setObjectName(_fromUtf8("spinBox_3"))
        self.spinBox_4 = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_4.setGeometry(QtCore.QRect(820, 320, 42, 22))
        self.spinBox_4.setObjectName(_fromUtf8("spinBox_4"))
        self.spinBox_5 = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_5.setGeometry(QtCore.QRect(820, 350, 42, 22))
        self.spinBox_5.setObjectName(_fromUtf8("spinBox_5"))
        self.spinBox_6 = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_6.setGeometry(QtCore.QRect(820, 380, 42, 22))
        self.spinBox_6.setObjectName(_fromUtf8("spinBox_6"))
        self.label_22 = QtGui.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(770, 290, 46, 13))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_23 = QtGui.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(770, 320, 46, 13))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_24 = QtGui.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(770, 350, 46, 13))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.label_25 = QtGui.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(770, 380, 46, 13))
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.label_26 = QtGui.QLabel(self.centralwidget)
        self.label_26.setGeometry(QtCore.QRect(770, 420, 46, 13))
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.spinBox_7 = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_7.setGeometry(QtCore.QRect(820, 410, 42, 22))
        self.spinBox_7.setObjectName(_fromUtf8("spinBox_7"))
        self.chkRest1 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest1.setGeometry(QtCore.QRect(11, 91, 45, 17))
        self.chkRest1.setObjectName(_fromUtf8("chkRest1"))
        self.chkRest2 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest2.setGeometry(QtCore.QRect(71, 91, 45, 17))
        self.chkRest2.setObjectName(_fromUtf8("chkRest2"))
        self.chkRest3 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest3.setGeometry(QtCore.QRect(130, 91, 45, 17))
        self.chkRest3.setObjectName(_fromUtf8("chkRest3"))
        self.chkRest4 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest4.setGeometry(QtCore.QRect(190, 91, 45, 17))
        self.chkRest4.setObjectName(_fromUtf8("chkRest4"))
        self.chkRest5 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest5.setGeometry(QtCore.QRect(250, 91, 45, 17))
        self.chkRest5.setObjectName(_fromUtf8("chkRest5"))
        self.chkRest6 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest6.setGeometry(QtCore.QRect(309, 91, 45, 17))
        self.chkRest6.setObjectName(_fromUtf8("chkRest6"))
        self.chkRest7 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest7.setGeometry(QtCore.QRect(369, 91, 45, 17))
        self.chkRest7.setObjectName(_fromUtf8("chkRest7"))
        self.chkRest8 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest8.setGeometry(QtCore.QRect(429, 91, 45, 17))
        self.chkRest8.setObjectName(_fromUtf8("chkRest8"))
        self.chkRest9 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest9.setGeometry(QtCore.QRect(489, 91, 45, 17))
        self.chkRest9.setObjectName(_fromUtf8("chkRest9"))
        self.chkRest10 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest10.setGeometry(QtCore.QRect(548, 91, 45, 17))
        self.chkRest10.setObjectName(_fromUtf8("chkRest10"))
        self.chkRest11 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest11.setGeometry(QtCore.QRect(608, 91, 45, 17))
        self.chkRest11.setObjectName(_fromUtf8("chkRest11"))
        self.chkRest12 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest12.setGeometry(QtCore.QRect(668, 91, 45, 17))
        self.chkRest12.setObjectName(_fromUtf8("chkRest12"))
        self.chkRest13 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest13.setGeometry(QtCore.QRect(727, 91, 45, 17))
        self.chkRest13.setObjectName(_fromUtf8("chkRest13"))
        self.chkRest14 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest14.setGeometry(QtCore.QRect(787, 91, 45, 17))
        self.chkRest14.setObjectName(_fromUtf8("chkRest14"))
        self.chkRest15 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest15.setGeometry(QtCore.QRect(847, 91, 45, 17))
        self.chkRest15.setObjectName(_fromUtf8("chkRest15"))
        self.chkRest16 = QtGui.QCheckBox(self.centralwidget)
        self.chkRest16.setGeometry(QtCore.QRect(906, 91, 45, 17))
        self.chkRest16.setObjectName(_fromUtf8("chkRest16"))
        self.dRepeat8 = QtGui.QDial(self.centralwidget)
        self.dRepeat8.setGeometry(QtCore.QRect(429, 121, 53, 50))
        self.dRepeat8.setObjectName(_fromUtf8("dRepeat8"))
        self.dRepeat7 = QtGui.QDial(self.centralwidget)
        self.dRepeat7.setGeometry(QtCore.QRect(369, 121, 54, 50))
        self.dRepeat7.setObjectName(_fromUtf8("dRepeat7"))
        self.dRepeat6 = QtGui.QDial(self.centralwidget)
        self.dRepeat6.setGeometry(QtCore.QRect(309, 121, 54, 50))
        self.dRepeat6.setObjectName(_fromUtf8("dRepeat6"))
        self.dRepeat5 = QtGui.QDial(self.centralwidget)
        self.dRepeat5.setGeometry(QtCore.QRect(250, 121, 53, 50))
        self.dRepeat5.setObjectName(_fromUtf8("dRepeat5"))
        self.dRepeat4 = QtGui.QDial(self.centralwidget)
        self.dRepeat4.setGeometry(QtCore.QRect(190, 121, 54, 50))
        self.dRepeat4.setObjectName(_fromUtf8("dRepeat4"))
        self.dRepeat9 = QtGui.QDial(self.centralwidget)
        self.dRepeat9.setGeometry(QtCore.QRect(488, 121, 54, 50))
        self.dRepeat9.setObjectName(_fromUtf8("dRepeat9"))
        self.dRepeat1 = QtGui.QDial(self.centralwidget)
        self.dRepeat1.setGeometry(QtCore.QRect(11, 121, 54, 50))
        self.dRepeat1.setObjectName(_fromUtf8("dRepeat1"))
        self.dRepeat2 = QtGui.QDial(self.centralwidget)
        self.dRepeat2.setGeometry(QtCore.QRect(71, 121, 53, 50))
        self.dRepeat2.setObjectName(_fromUtf8("dRepeat2"))
        self.dRepeat3 = QtGui.QDial(self.centralwidget)
        self.dRepeat3.setGeometry(QtCore.QRect(130, 121, 54, 50))
        self.dRepeat3.setObjectName(_fromUtf8("dRepeat3"))
        self.dRepeat10 = QtGui.QDial(self.centralwidget)
        self.dRepeat10.setGeometry(QtCore.QRect(548, 121, 54, 50))
        self.dRepeat10.setObjectName(_fromUtf8("dRepeat10"))
        self.dRepeat11 = QtGui.QDial(self.centralwidget)
        self.dRepeat11.setGeometry(QtCore.QRect(608, 121, 54, 50))
        self.dRepeat11.setObjectName(_fromUtf8("dRepeat11"))
        self.dRepeat112 = QtGui.QDial(self.centralwidget)
        self.dRepeat112.setGeometry(QtCore.QRect(668, 121, 53, 50))
        self.dRepeat112.setObjectName(_fromUtf8("dRepeat112"))
        self.dRepeat113 = QtGui.QDial(self.centralwidget)
        self.dRepeat113.setGeometry(QtCore.QRect(727, 121, 54, 50))
        self.dRepeat113.setObjectName(_fromUtf8("dRepeat113"))
        self.dRepeat14 = QtGui.QDial(self.centralwidget)
        self.dRepeat14.setGeometry(QtCore.QRect(787, 121, 54, 50))
        self.dRepeat14.setObjectName(_fromUtf8("dRepeat14"))
        self.dRepeat115 = QtGui.QDial(self.centralwidget)
        self.dRepeat115.setGeometry(QtCore.QRect(847, 121, 53, 50))
        self.dRepeat115.setObjectName(_fromUtf8("dRepeat115"))
        self.dRepeat16 = QtGui.QDial(self.centralwidget)
        self.dRepeat16.setGeometry(QtCore.QRect(906, 121, 54, 50))
        self.dRepeat16.setObjectName(_fromUtf8("dRepeat16"))
        self.sbPPQ1 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ1.setGeometry(QtCore.QRect(15, 180, 33, 20))
        self.sbPPQ1.setObjectName(_fromUtf8("sbPPQ1"))
        self.sbPPQ2 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ2.setGeometry(QtCore.QRect(75, 180, 33, 20))
        self.sbPPQ2.setObjectName(_fromUtf8("sbPPQ2"))
        self.sbPPQ3 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ3.setGeometry(QtCore.QRect(134, 180, 33, 20))
        self.sbPPQ3.setObjectName(_fromUtf8("sbPPQ3"))
        self.sbPPQ4 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ4.setGeometry(QtCore.QRect(194, 180, 33, 20))
        self.sbPPQ4.setObjectName(_fromUtf8("sbPPQ4"))
        self.sbPPQ5 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ5.setGeometry(QtCore.QRect(254, 180, 33, 20))
        self.sbPPQ5.setObjectName(_fromUtf8("sbPPQ5"))
        self.sbPPQ6 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ6.setGeometry(QtCore.QRect(313, 180, 33, 20))
        self.sbPPQ6.setObjectName(_fromUtf8("sbPPQ6"))
        self.sbPPQ7 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ7.setGeometry(QtCore.QRect(373, 180, 33, 20))
        self.sbPPQ7.setObjectName(_fromUtf8("sbPPQ7"))
        self.sbPPQ8 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ8.setGeometry(QtCore.QRect(433, 180, 33, 20))
        self.sbPPQ8.setObjectName(_fromUtf8("sbPPQ8"))
        self.sbPPQ9 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ9.setGeometry(QtCore.QRect(493, 180, 33, 20))
        self.sbPPQ9.setObjectName(_fromUtf8("sbPPQ9"))
        self.sbPPQ10 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ10.setGeometry(QtCore.QRect(552, 180, 33, 20))
        self.sbPPQ10.setObjectName(_fromUtf8("sbPPQ10"))
        self.sbPPQ11 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ11.setGeometry(QtCore.QRect(612, 180, 33, 20))
        self.sbPPQ11.setObjectName(_fromUtf8("sbPPQ11"))
        self.sbPPQ12 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ12.setGeometry(QtCore.QRect(672, 180, 33, 20))
        self.sbPPQ12.setObjectName(_fromUtf8("sbPPQ12"))
        self.sbPPQ13 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ13.setGeometry(QtCore.QRect(731, 180, 33, 20))
        self.sbPPQ13.setObjectName(_fromUtf8("sbPPQ13"))
        self.sbPPQ14 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ14.setGeometry(QtCore.QRect(791, 180, 33, 20))
        self.sbPPQ14.setObjectName(_fromUtf8("sbPPQ14"))
        self.sbPPQ15 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ15.setGeometry(QtCore.QRect(851, 180, 33, 20))
        self.sbPPQ15.setObjectName(_fromUtf8("sbPPQ15"))
        self.sbPPQ16 = QtGui.QSpinBox(self.centralwidget)
        self.sbPPQ16.setGeometry(QtCore.QRect(910, 180, 33, 20))
        self.sbPPQ16.setObjectName(_fromUtf8("sbPPQ16"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(350, 310, 89, 134))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioButton = QtGui.QRadioButton(self.widget)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtGui.QRadioButton(self.widget)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtGui.QRadioButton(self.widget)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.verticalLayout.addWidget(self.radioButton_3)
        self.radioButton_4 = QtGui.QRadioButton(self.widget)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.verticalLayout.addWidget(self.radioButton_4)
        self.radioButton_5 = QtGui.QRadioButton(self.widget)
        self.radioButton_5.setObjectName(_fromUtf8("radioButton_5"))
        self.verticalLayout.addWidget(self.radioButton_5)
        self.radioButton_6 = QtGui.QRadioButton(self.widget)
        self.radioButton_6.setObjectName(_fromUtf8("radioButton_6"))
        self.verticalLayout.addWidget(self.radioButton_6)
        self.widget1 = QtGui.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(20, 240, 32, 180))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radioButton_7 = QtGui.QRadioButton(self.widget1)
        self.radioButton_7.setChecked(True)
        self.radioButton_7.setObjectName(_fromUtf8("radioButton_7"))
        self.verticalLayout_2.addWidget(self.radioButton_7)
        self.radioButton_8 = QtGui.QRadioButton(self.widget1)
        self.radioButton_8.setObjectName(_fromUtf8("radioButton_8"))
        self.verticalLayout_2.addWidget(self.radioButton_8)
        self.radioButton_9 = QtGui.QRadioButton(self.widget1)
        self.radioButton_9.setObjectName(_fromUtf8("radioButton_9"))
        self.verticalLayout_2.addWidget(self.radioButton_9)
        self.radioButton_10 = QtGui.QRadioButton(self.widget1)
        self.radioButton_10.setObjectName(_fromUtf8("radioButton_10"))
        self.verticalLayout_2.addWidget(self.radioButton_10)
        self.radioButton_11 = QtGui.QRadioButton(self.widget1)
        self.radioButton_11.setObjectName(_fromUtf8("radioButton_11"))
        self.verticalLayout_2.addWidget(self.radioButton_11)
        self.radioButton_12 = QtGui.QRadioButton(self.widget1)
        self.radioButton_12.setObjectName(_fromUtf8("radioButton_12"))
        self.verticalLayout_2.addWidget(self.radioButton_12)
        self.radioButton_13 = QtGui.QRadioButton(self.widget1)
        self.radioButton_13.setObjectName(_fromUtf8("radioButton_13"))
        self.verticalLayout_2.addWidget(self.radioButton_13)
        self.radioButton_14 = QtGui.QRadioButton(self.widget1)
        self.radioButton_14.setObjectName(_fromUtf8("radioButton_14"))
        self.verticalLayout_2.addWidget(self.radioButton_14)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 974, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSequencer = QtGui.QMenu(self.menubar)
        self.menuSequencer.setObjectName(_fromUtf8("menuSequencer"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuPattern = QtGui.QMenu(self.menubar)
        self.menuPattern.setObjectName(_fromUtf8("menuPattern"))
        self.menuTracker = QtGui.QMenu(self.menubar)
        self.menuTracker.setObjectName(_fromUtf8("menuTracker"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionOptions = QtGui.QAction(MainWindow)
        self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
        self.actionSync_Ports = QtGui.QAction(MainWindow)
        self.actionSync_Ports.setObjectName(_fromUtf8("actionSync_Ports"))
        self.actionAdd_Pattern = QtGui.QAction(MainWindow)
        self.actionAdd_Pattern.setObjectName(_fromUtf8("actionAdd_Pattern"))
        self.actionRandomize = QtGui.QAction(MainWindow)
        self.actionRandomize.setObjectName(_fromUtf8("actionRandomize"))
        self.actionRandomize_PPQ = QtGui.QAction(MainWindow)
        self.actionRandomize_PPQ.setObjectName(_fromUtf8("actionRandomize_PPQ"))
        self.actionRandomize_Repeats = QtGui.QAction(MainWindow)
        self.actionRandomize_Repeats.setObjectName(_fromUtf8("actionRandomize_Repeats"))
        self.actionRandomize_Rests = QtGui.QAction(MainWindow)
        self.actionRandomize_Rests.setObjectName(_fromUtf8("actionRandomize_Rests"))
        self.actionHalf_Notes = QtGui.QAction(MainWindow)
        self.actionHalf_Notes.setObjectName(_fromUtf8("actionHalf_Notes"))
        self.actionQuarter_Notes = QtGui.QAction(MainWindow)
        self.actionQuarter_Notes.setObjectName(_fromUtf8("actionQuarter_Notes"))
        self.actionEigth_Notes = QtGui.QAction(MainWindow)
        self.actionEigth_Notes.setObjectName(_fromUtf8("actionEigth_Notes"))
        self.actionSixteenth_Notes = QtGui.QAction(MainWindow)
        self.actionSixteenth_Notes.setObjectName(_fromUtf8("actionSixteenth_Notes"))
        self.actionTranspose = QtGui.QAction(MainWindow)
        self.actionTranspose.setObjectName(_fromUtf8("actionTranspose"))
        self.actionShift_Left = QtGui.QAction(MainWindow)
        self.actionShift_Left.setObjectName(_fromUtf8("actionShift_Left"))
        self.actionShift_Right = QtGui.QAction(MainWindow)
        self.actionShift_Right.setObjectName(_fromUtf8("actionShift_Right"))
        self.actionPlay = QtGui.QAction(MainWindow)
        self.actionPlay.setCheckable(True)
        self.actionPlay.setObjectName(_fromUtf8("actionPlay"))
        self.menuFile.addAction(self.actionExit)
        self.menuSequencer.addAction(self.actionRandomize)
        self.menuSequencer.addAction(self.actionRandomize_PPQ)
        self.menuSequencer.addAction(self.actionRandomize_Repeats)
        self.menuSequencer.addAction(self.actionRandomize_Rests)
        self.menuSequencer.addSeparator()
        self.menuSequencer.addAction(self.actionHalf_Notes)
        self.menuSequencer.addAction(self.actionQuarter_Notes)
        self.menuSequencer.addAction(self.actionEigth_Notes)
        self.menuSequencer.addAction(self.actionSixteenth_Notes)
        self.menuSequencer.addSeparator()
        self.menuSequencer.addAction(self.actionTranspose)
        self.menuSequencer.addAction(self.actionShift_Left)
        self.menuSequencer.addAction(self.actionShift_Right)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionOptions)
        self.menuEdit.addAction(self.actionSync_Ports)
        self.menuTracker.addAction(self.actionAdd_Pattern)
        self.menuTracker.addAction(self.actionPlay)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSequencer.menuAction())
        self.menubar.addAction(self.menuPattern.menuAction())
        self.menubar.addAction(self.menuTracker.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pbStart.setText(_translate("MainWindow", "Start", None))
        self.label_5.setText(_translate("MainWindow", "Voice", None))
        self.label_39.setText(_translate("MainWindow", "Banks", None))
        self.label_40.setText(_translate("MainWindow", "Voices", None))
        self.label_11.setText(_translate("MainWindow", "Seq", None))
        self.label_6.setText(_translate("MainWindow", "steps", None))
        self.label_12.setText(_translate("MainWindow", "row offset", None))
        self.label_13.setText(_translate("MainWindow", "channel", None))
        self.pushButton.setText(_translate("MainWindow", "Gen", None))
        self.chkStep1.setText(_translate("MainWindow", "1", None))
        self.chkStep1_2.setText(_translate("MainWindow", "2", None))
        self.chkStep1_3.setText(_translate("MainWindow", "3", None))
        self.chkStep1_4.setText(_translate("MainWindow", "4", None))
        self.chkStep1_5.setText(_translate("MainWindow", "7", None))
        self.chkStep1_6.setText(_translate("MainWindow", "5", None))
        self.chkStep1_7.setText(_translate("MainWindow", "6", None))
        self.chkStep1_8.setText(_translate("MainWindow", "8", None))
        self.chkStep1_9.setText(_translate("MainWindow", "15", None))
        self.chkStep1_10.setText(_translate("MainWindow", "14", None))
        self.chkStep1_11.setText(_translate("MainWindow", "11", None))
        self.chkStep1_12.setText(_translate("MainWindow", "16", None))
        self.chkStep1_13.setText(_translate("MainWindow", "9", None))
        self.chkStep1_14.setText(_translate("MainWindow", "10", None))
        self.chkStep1_15.setText(_translate("MainWindow", "12", None))
        self.chkStep1_16.setText(_translate("MainWindow", "13", None))
        self.label.setText(_translate("MainWindow", "Transpose", None))
        self.label_2.setText(_translate("MainWindow", "Var", None))
        self.label_4.setText(_translate("MainWindow", "Alg", None))
        self.pushButton_2.setText(_translate("MainWindow", "Enter", None))
        self.checkBox.setText(_translate("MainWindow", "Fractalize", None))
        self.label_7.setText(_translate("MainWindow", "Scale", None))
        self.label_8.setText(_translate("MainWindow", "Chord", None))
        self.label_9.setText(_translate("MainWindow", "PROB1", None))
        self.lineEdit.setText(_translate("MainWindow", "0.0", None))
        self.lineEdit_2.setText(_translate("MainWindow", "0.0", None))
        self.label_10.setText(_translate("MainWindow", "PROB2", None))
        self.lineEdit_3.setText(_translate("MainWindow", "0.0", None))
        self.lineEdit_4.setText(_translate("MainWindow", "0.0", None))
        self.label_14.setText(_translate("MainWindow", "PROB3", None))
        self.label_15.setText(_translate("MainWindow", "PROB4", None))
        self.lineEdit_5.setText(_translate("MainWindow", "0", None))
        self.label_16.setText(_translate("MainWindow", "OCT5", None))
        self.lineEdit_6.setText(_translate("MainWindow", "0", None))
        self.lineEdit_7.setText(_translate("MainWindow", "0", None))
        self.label_17.setText(_translate("MainWindow", "OCT4", None))
        self.lineEdit_8.setText(_translate("MainWindow", "0", None))
        self.label_18.setText(_translate("MainWindow", "OCT2", None))
        self.label_19.setText(_translate("MainWindow", "OCT3", None))
        self.checkBox_2.setText(_translate("MainWindow", "Program Change", None))
        self.checkBox_3.setText(_translate("MainWindow", "Op1", None))
        self.radioButton_23.setText(_translate("MainWindow", "Roll", None))
        self.radioButton_24.setText(_translate("MainWindow", "Shift Left", None))
        self.radioButton_25.setText(_translate("MainWindow", "Shift Right", None))
        self.radioButton_26.setText(_translate("MainWindow", "Random Shift", None))
        self.radioButton_27.setText(_translate("MainWindow", "Algorithm", None))
        self.radioButton_28.setText(_translate("MainWindow", "Arp Complex", None))
        self.checkBox_4.setText(_translate("MainWindow", "Op2", None))
        self.radioButton_29.setText(_translate("MainWindow", "Roll", None))
        self.radioButton_30.setText(_translate("MainWindow", "Shift Left", None))
        self.radioButton_31.setText(_translate("MainWindow", "Shift Right", None))
        self.radioButton_32.setText(_translate("MainWindow", "Random Shift", None))
        self.radioButton_33.setText(_translate("MainWindow", "Algorithm", None))
        self.radioButton_34.setText(_translate("MainWindow", "Arp Complex", None))
        self.checkBox_5.setText(_translate("MainWindow", "Op3", None))
        self.radioButton_35.setText(_translate("MainWindow", "Roll", None))
        self.radioButton_36.setText(_translate("MainWindow", "Shift Left", None))
        self.radioButton_37.setText(_translate("MainWindow", "Shift Right", None))
        self.radioButton_38.setText(_translate("MainWindow", "Random Shift", None))
        self.radioButton_39.setText(_translate("MainWindow", "Algorithm", None))
        self.radioButton_40.setText(_translate("MainWindow", "Arp Complex", None))
        self.checkBox_6.setText(_translate("MainWindow", "Op4", None))
        self.label_3.setText(_translate("MainWindow", "Alg", None))
        self.label_20.setText(_translate("MainWindow", "Scale", None))
        self.label_21.setText(_translate("MainWindow", "Chord", None))
        self.label_22.setText(_translate("MainWindow", "Lead1", None))
        self.label_23.setText(_translate("MainWindow", "Follow1", None))
        self.label_24.setText(_translate("MainWindow", "Lead2", None))
        self.label_25.setText(_translate("MainWindow", "Follow2", None))
        self.label_26.setText(_translate("MainWindow", "UDA", None))
        self.chkRest1.setText(_translate("MainWindow", "Rest", None))
        self.chkRest2.setText(_translate("MainWindow", "Rest", None))
        self.chkRest3.setText(_translate("MainWindow", "Rest", None))
        self.chkRest4.setText(_translate("MainWindow", "Rest", None))
        self.chkRest5.setText(_translate("MainWindow", "Rest", None))
        self.chkRest6.setText(_translate("MainWindow", "Rest", None))
        self.chkRest7.setText(_translate("MainWindow", "Rest", None))
        self.chkRest8.setText(_translate("MainWindow", "Rest", None))
        self.chkRest9.setText(_translate("MainWindow", "Rest", None))
        self.chkRest10.setText(_translate("MainWindow", "Rest", None))
        self.chkRest11.setText(_translate("MainWindow", "Rest", None))
        self.chkRest12.setText(_translate("MainWindow", "Rest", None))
        self.chkRest13.setText(_translate("MainWindow", "Rest", None))
        self.chkRest14.setText(_translate("MainWindow", "Rest", None))
        self.chkRest15.setText(_translate("MainWindow", "Rest", None))
        self.chkRest16.setText(_translate("MainWindow", "Rest", None))
        self.radioButton.setText(_translate("MainWindow", "Roll", None))
        self.radioButton_2.setText(_translate("MainWindow", "Shift Left", None))
        self.radioButton_3.setText(_translate("MainWindow", "Shift Right", None))
        self.radioButton_4.setText(_translate("MainWindow", "Random Shift", None))
        self.radioButton_5.setText(_translate("MainWindow", "Algorithm", None))
        self.radioButton_6.setText(_translate("MainWindow", "Arp Complex", None))
        self.radioButton_7.setText(_translate("MainWindow", "A", None))
        self.radioButton_8.setText(_translate("MainWindow", "B", None))
        self.radioButton_9.setText(_translate("MainWindow", "C", None))
        self.radioButton_10.setText(_translate("MainWindow", "D", None))
        self.radioButton_11.setText(_translate("MainWindow", "E", None))
        self.radioButton_12.setText(_translate("MainWindow", "F", None))
        self.radioButton_13.setText(_translate("MainWindow", "G", None))
        self.radioButton_14.setText(_translate("MainWindow", "H", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuSequencer.setTitle(_translate("MainWindow", "Sequencer", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuPattern.setTitle(_translate("MainWindow", "Pattern", None))
        self.menuTracker.setTitle(_translate("MainWindow", "Chain", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionCut.setText(_translate("MainWindow", "Cut", None))
        self.actionPaste.setText(_translate("MainWindow", "Paste", None))
        self.actionOptions.setText(_translate("MainWindow", "Options", None))
        self.actionSync_Ports.setText(_translate("MainWindow", "Sync Ports", None))
        self.actionAdd_Pattern.setText(_translate("MainWindow", "Add Pattern To Chain", None))
        self.actionRandomize.setText(_translate("MainWindow", "Randomize", None))
        self.actionRandomize_PPQ.setText(_translate("MainWindow", "Randomize PPQ", None))
        self.actionRandomize_Repeats.setText(_translate("MainWindow", "Randomize Repeats", None))
        self.actionRandomize_Rests.setText(_translate("MainWindow", "Randomize Rests", None))
        self.actionHalf_Notes.setText(_translate("MainWindow", "Half Notes", None))
        self.actionQuarter_Notes.setText(_translate("MainWindow", "Quarter Notes", None))
        self.actionEigth_Notes.setText(_translate("MainWindow", "Eigth Notes", None))
        self.actionSixteenth_Notes.setText(_translate("MainWindow", "Sixteenth Notes", None))
        self.actionTranspose.setText(_translate("MainWindow", "Transpose", None))
        self.actionShift_Left.setText(_translate("MainWindow", "Shift Left", None))
        self.actionShift_Right.setText(_translate("MainWindow", "Shift Right", None))
        self.actionPlay.setText(_translate("MainWindow", "Play", None))



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
	