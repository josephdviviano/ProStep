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
    
	def __init__(self):
		
		self.sequencers = []
		self.motion = MotionData(self)
		self.bStopped = False
		self.num_sequencers = 32
		for i in range(32):
			self.sequencers.append(Sequencer())
			
		self.cur_sequencer = 0
		self.ppq = 0
		
	def UpdateMIDI(self):
		self.ppq = self.ppq+1
		seq = self.GetSequencer()
		seq.parent = self
		seq.Update(self.ppq)
		
	def UpdateMIDIInput(self,msg):
		seq = self.GetSequencer()
		seq.parent = self
		seq.UpdateMIDIInput(msg)
				
	
	def PrevStep(self):
		pass
		
	def NextStep(self):
		pass
		
	def ShiftLeft(self):
		pass
		
	def ShiftRight(self):
		pass
	
	def SetMidiPort(self,index):
		pass
	
	def GetSequencer(self):
		self.sequencers[self.cur_sequencer].Activate()
		return self.sequencers[self.cur_sequencer]


	def HalfNotes(self):
		seq = self.GetSequencer()
		seq.HalfNotes()
	
	def QuarterNotes(self):
		seq = self.GetSequencer()
		seq.QuarterNotes()
	
	def EigthNotes(self):
		seq = self.GetSequencer()
		seq.EigthNotes()
	
	def SixteenthNotes(self):
		seq = self.GetSequencer()
		seq.SixteenthNotes()
	
	def MotionRecord(self):
		if( self.actionRecord.isChecked() ) : self.motion.bRecording = True
		else: self.motion.bRecording = False
		
	def MotionClear(self):
		self.motion.Clear()
				
	def Options(self):
		dlg = QtGui.QDialog()
		qdlg = Ui_ConfigDialog()		
		qdlg.setupUi(dlg)
		qdlg.parent = self
		dlg.show()
		dlg.exec_()
			
		try:
			self.thread.midi_input, self.thread.midi_output = MIDI_GetInOut()
			
			self.thread.kb_channel = self.input_channel 
			self.thread.midi_channel = self.midi_channel
			self.thread.num_steps = self.num_banks*16
		except:
			pass
			
		self.sbRow.setMaximum(self.num_banks-1)
		self.sbVoice.setMaximum(self.num_voices-1)
		
		seq = self.GetSequencer()		
		seq.Init(self.num_voices, self.num_banks,self.midi_channel)
		seq.midi_output = self.midi_output
		for i in range(self.num_sequencers):
			self.sequencers[i].parent= self
		
		self.sbSteps.setValue(self.num_banks*16)
		self.sbSteps.setMaximum(self.num_banks*16)
		
		self.motion.Init(self.num_banks*16)
		
		self.UpdateUi()
		
		
	def SyncDlg(self):
		dlg = QtGui.QDialog()
		qdlg = Ui_SyncDialog()		
		qdlg.mainwindow = self
		qdlg.setupUi(dlg)
		qdlg.parent = self
		dlg.show()
		dlg.exec_()
		
	def TransposeDlg(self):
		dlg = QtGui.QDialog()
		qdlg = Ui_TransposeDialog()		
		qdlg.mainwindow = self
		qdlg.setupUi(dlg)
		qdlg.parent = self
		dlg.show()
		dlg.exec_()
		
	def Transpose(self,value):
		
		seq = self.GetSequencer()				
		seq.Transpose(value)		
		self.UpdateUi()
		
			
	
	def Randomize(self):		
		seq = self.GetSequencer()				
		seq.Randomize()
		self.UpdateUi()
	
	def RandomizePPQ(self):
		seq = self.GetSequencer()				
		seq.RandomizePPQ()
		self.UpdateUi()
	
	def RandomizeRests(self):
		seq = self.GetSequencer()				
		seq.RandomizeRests()
		self.UpdateUi()
			
	def RandomizeRepeats(self):
		seq = self.GetSequencer()				
		seq.RandomizeRepeats()
		self.UpdateUi()			
	
	
	def SetMidiChannel(self,ch):
		seq = self.GetSequencer()
		seq.SetMidiChannel(ch)
		
	def Panic(self):
		self.midi_output.reset()
		
	def SetSteps(self,value):
		seq = self.GetSequencer()						
		seq.SetNumSteps(value)
	
	def CurSeq(self,value):				
		self.cur_seq = value-1
		self.UpdateUi()
	
	def ChangeBanks(self,value):
		seq = self.GetSequencer()
		seq.ChangeBanks(value)
	
	def ChangeVoices(self,value):
		seq = self.GetSequencer()
		seq.ChangeVoices(value)
		
	def CurVoice(self,value):		
		seq = self.GetSequencer()				
		seq.ChangeVoice(value)
		self.UpdateUi()
	
	def CurBank(self,value):
		seq = self.GetSequencer()										
		seq.SetBank(value)
		self.UpdateUi()		
		
	def GenerateVariations(self):
		seq = self.GetSequencer()								
		seq.GenerateVariations()
		self.UpdateUi()		
		
	def VarA(self):
		seq = self.GetSequencer()								
		seq.ChangeVar(0)
	
	def VarB(self):
		seq = self.GetSequencer()
		seq.ChangeVar(1)
			
	def VarC(self):
		seq = self.GetSequencer()								
		seq.ChangeVar(2)
		
	def VarD(self):
		seq = self.GetSequencer()								
		seq.ChangeVar(3)
	
	def VarE(self):
		seq = self.GetSequencer()								
		seq.ChangeVar(4)
	
	def VarF(self):
		seq = self.GetSequencer()								
		seq.ChangeVar(5)
	
	def VarG(self):
		seq = self.GetSequencer()								
		seq.ChangeVar(6)
	
	def VarH(self):
		seq = self.GetSequencer()								
		seq.ChangeVar(7)
		
	
	
	def SetRest(self,n,value):
		seq = self.GetSequencer()
		seq.SetRest(n,value)
		
	def SetRest1(self,value):
		self.SetRest(0,value)
		
	def SetRest2(self,value):
		self.SetRest(1,value)
		
	def SetRest3(self,value):
		self.SetRest(2,value)
		
	def SetRest4(self,value):
		self.SetRest(3,value)
		
	def SetRest5(self,value):
		self.SetRest(4,value)
		
	def SetRest6(self,value):
		self.SetRest(5,value)
		
	def SetRest7(self,value):
		self.SetRest(6,value)
		
	def SetRest8(self,value):
		self.SetRest(7,value)
		
	def SetRest9(self,value):
		self.SetRest(8,value)
		
	def SetRest10(self,value):
		self.SetRest(9,value)
		
	def SetRest11(self,value):
		self.SetRest(10,value)
		
	def SetRest12(self,value):
		self.SetRest(11,value)
		
	def SetRest13(self,value):
		self.SetRest(12,value)
		
	def SetRest14(self,value):
		self.SetRest(13,value)
		
	def SetRest15(self,value):
		self.SetRest(14,value)
		
	def SetRest16(self,value):
		self.SetRest(15,value)
	
	def SetPPQ(self,n,value):
		seq = self.GetSequencer()
		seq.SetPPQ(n,value)
		
		
	def SetPPQ1(self,value):
		self.SetPPQ(0,value)
		
	def SetPPQ2(self,value):
		self.SetPPQ(1,value)
			
	def SetPPQ3(self,value):
		self.SetPPQ(2,value)
		
	def SetPPQ4(self,value):
		self.SetPPQ(3,value)
		
	def SetPPQ5(self,value):
		self.SetPPQ(4,value)
		
	def SetPPQ6(self,value):
		self.SetPPQ(5,value)
		
	def SetPPQ7(self,value):
		self.SetPPQ(6,value)
		
	def SetPPQ8(self,value):
		self.SetPPQ(7,value)
		
	def SetPPQ9(self,value):
		self.SetPPQ(8,value)
		
	def SetPPQ10(self,value):
		self.SetPPQ(9,value)
		
	def SetPPQ11(self,value):
		self.SetPPQ(10,value)
		
	def SetPPQ12(self,value):
		self.SetPPQ(11,value)
		
	def SetPPQ13(self,value):
		self.SetPPQ(12,value)
		
	def SetPPQ14(self,value):
		self.SetPPQ(13,value)
		
	def SetPPQ15(self,value):
		self.SetPPQ(14,value)
		
	def SetPPQ16(self,value):
		self.SetPPQ(15,value)
		
	def SetRepeat(self,n,value):
		seq = self.GetSequencer()
		seq.SetRepeat(n,value)
		
	def SetRepeat1(self,value):
		self.SetRepeat(0,value)
	def SetRepeat2(self,value):
		self.SetRepeat(1,value)
	def SetRepeat3(self,value):
		self.SetRepeat(2,value)
	def SetRepeat4(self,value):
		self.SetRepeat(3,value)
	def SetRepeat5(self,value):
		self.SetRepeat(4,value)
	def SetRepeat6(self,value):
		self.SetRepeat(5,value)
	def SetRepeat7(self,value):
		self.SetRepeat(6,value)
	def SetRepeat8(self,value):
		self.SetRepeat(7,value)
	def SetRepeat9(self,value):
		self.SetRepeat(8,value)
	def SetRepeat10(self,value):
		self.SetRepeat(9,value)
	def SetRepeat11(self,value):
		self.SetRepeat(10,value)
	def SetRepeat12(self,value):
		self.SetRepeat(11,value)
	def SetRepeat13(self,value):
		self.SetRepeat(12,value)
	def SetRepeat14(self,value):
		self.SetRepeat(13,value)
	def SetRepeat15(self,value):
		self.SetRepeat(14,value)
	def SetRepeat16(self,value):
		self.SetRepeat(15,value)
	
	def SetNote(self,n,value):
		seq = self.GetSequencer()						
		seq.SetNote(n,value)
		self.lcdNumber.display(note_names[value])
		
	def SetNote1(self,value):
		self.SetNote(0,value)
		
	def SetNote2(self,value):
		self.SetNote(1,value)
		
	def SetNote3(self,value):
		self.SetNote(2,value)
		
	def SetNote4(self,value):
		self.SetNote(3,value)		
		
	def SetNote5(self,value):
		self.SetNote(4,value)
		
	def SetNote6(self,value):
		self.SetNote(5,value)
		
	def SetNote7(self,value):
		self.SetNote(6,value)
		
	def SetNote8(self,value):
		self.SetNote(7,value)
		
	def SetNote9(self,value):
		self.SetNote(8,value)
		
	def SetNote10(self,value):
		self.SetNote(9,value)
		
	def SetNote11(self,value):
		self.SetNote(10,value)
		
	def SetNote12(self,value):
		self.SetNote(11,value)
		
	def SetNote13(self,value):
		self.SetNote(12,value)
		
	def SetNote14(self,value):
		self.SetNote(13,value)
		
	def SetNote15(self,value):
		self.SetNote(14,value)
		
	def SetNote16(self,value):		
		self.SetNote(15,value)
	
	def Motion1(self,value):
		self.motion.ControlCapture(0,value)		
	def Motion2(self,value):
		self.motion.ControlCapture(1,value)
	def Motion3(self,value):
		self.motion.ControlCapture(2,value)
	def Motion4(self,value):
		self.motion.ControlCapture(3,value)
		
	def Motion5(self,value):
		self.motion.ControlCapture(4,value)		
	def Motion6(self,value):
		self.motion.ControlCapture(5,value)
	def Motion7(self,value):
		self.motion.ControlCapture(6,value)
	def Motion8(self,value):
		self.motion.ControlCapture(7,value)
	def Motion9(self,value):
		self.motion.ControlCapture(8,value)		
	def Motion10(self,value):
		self.motion.ControlCapture(9,value)
	def Motion11(self,value):
		self.motion.ControlCapture(10,value)
	def Motion12(self,value):
		self.motion.ControlCapture(11,value)
	def Motion13(self,value):
		self.motion.ControlCapture(12,value)		
	def Motion14(self,value):
		self.motion.ControlCapture(13,value)
	def Motion15(self,value):
		self.motion.ControlCapture(14,value)
	def Motion16(self,value):
		self.motion.ControlCapture(15,value)
		
	def UpdateUi(self):
		
		seq = self.GetSequencer()
		
		self.cbNote1.setCurrentIndex(seq.GetNote(0))
		self.cbNote2.setCurrentIndex(seq.GetNote(1))
		self.cbNote3.setCurrentIndex(seq.GetNote(2))
		self.cbNote4.setCurrentIndex(seq.GetNote(3))
		self.cbNote5.setCurrentIndex(seq.GetNote(4))
		self.cbNote6.setCurrentIndex(seq.GetNote(5))
		self.cbNote7.setCurrentIndex(seq.GetNote(6))
		self.cbNote8.setCurrentIndex(seq.GetNote(7))
		self.cbNote9.setCurrentIndex(seq.GetNote(8))
		self.cbNote10.setCurrentIndex(seq.GetNote(9))
		self.cbNote11.setCurrentIndex(seq.GetNote(10))
		self.cbNote12.setCurrentIndex(seq.GetNote(11))
		self.cbNote13.setCurrentIndex(seq.GetNote(12))
		self.cbNote14.setCurrentIndex(seq.GetNote(13))
		self.cbNote15.setCurrentIndex(seq.GetNote(14))
		self.cbNote16.setCurrentIndex(seq.GetNote(15))
		
		self.sbPPQ1.setValue(seq.GetPPQ(0))
		self.sbPPQ2.setValue(seq.GetPPQ(1))
		self.sbPPQ3.setValue(seq.GetPPQ(2))
		self.sbPPQ4.setValue(seq.GetPPQ(3))
		self.sbPPQ5.setValue(seq.GetPPQ(4))
		self.sbPPQ6.setValue(seq.GetPPQ(5))
		self.sbPPQ7.setValue(seq.GetPPQ(6))
		self.sbPPQ8.setValue(seq.GetPPQ(7))
		self.sbPPQ9.setValue(seq.GetPPQ(8))
		self.sbPPQ10.setValue(seq.GetPPQ(9))
		self.sbPPQ11.setValue(seq.GetPPQ(10))
		self.sbPPQ12.setValue(seq.GetPPQ(11))
		self.sbPPQ13.setValue(seq.GetPPQ(12))
		self.sbPPQ14.setValue(seq.GetPPQ(13))
		self.sbPPQ15.setValue(seq.GetPPQ(14))
		self.sbPPQ16.setValue(seq.GetPPQ(15))
		
		self.dRepeat1.setValue(seq.GetRepeat(0))
		self.dRepeat2.setValue(seq.GetRepeat(1))
		self.dRepeat3.setValue(seq.GetRepeat(2))
		self.dRepeat4.setValue(seq.GetRepeat(3))
		self.dRepeat5.setValue(seq.GetRepeat(4))
		self.dRepeat6.setValue(seq.GetRepeat(5))
		self.dRepeat7.setValue(seq.GetRepeat(6))
		self.dRepeat8.setValue(seq.GetRepeat(7))
		self.dRepeat9.setValue(seq.GetRepeat(8))
		self.dRepeat10.setValue(seq.GetRepeat(9))
		self.dRepeat11.setValue(seq.GetRepeat(10))
		self.dRepeat12.setValue(seq.GetRepeat(11))
		self.dRepeat13.setValue(seq.GetRepeat(12))
		self.dRepeat14.setValue(seq.GetRepeat(13))
		self.dRepeat15.setValue(seq.GetRepeat(14))
		self.dRepeat16.setValue(seq.GetRepeat(15))
		
		self.chkRest1.setChecked(seq.GetRest(0))
		self.chkRest2.setChecked(seq.GetRest(1))
		self.chkRest3.setChecked(seq.GetRest(2))
		self.chkRest4.setChecked(seq.GetRest(3))
		self.chkRest5.setChecked(seq.GetRest(4))
		self.chkRest6.setChecked(seq.GetRest(5))
		self.chkRest7.setChecked(seq.GetRest(6))
		self.chkRest8.setChecked(seq.GetRest(7))
		self.chkRest9.setChecked(seq.GetRest(8))
		self.chkRest10.setChecked(seq.GetRest(9))
		self.chkRest11.setChecked(seq.GetRest(10))
		self.chkRest12.setChecked(seq.GetRest(11))
		self.chkRest13.setChecked(seq.GetRest(12))
		self.chkRest14.setChecked(seq.GetRest(13))
		self.chkRest15.setChecked(seq.GetRest(14))
		self.chkRest16.setChecked(seq.GetRest(15))
		
	def setupUi(self, MainWindow, bMDIChild=False):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(1005, 518)
		MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(93, 93, 93);\n"
		"color: rgb(255, 255, 255);\n"
		"QMenuBar { color: rgb(0,0,0);}"))
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.lcdNumber = QtGui.QLCDNumber(self.centralwidget)
		self.lcdNumber.setGeometry(QtCore.QRect(840, 10, 101, 23))
		self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
		self.layoutWidget = QtGui.QWidget(self.centralwidget)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 100, 961, 41))
		self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		
		if(bMDIChild == False):
			self.thread = Worker(self)
			MainWindow.connect(self.thread, QtCore.SIGNAL("finished()"), self.UpdateUi)
			MainWindow.connect(self.thread, QtCore.SIGNAL("terminated()"), self.UpdateUi)
			MainWindow.connect(self.thread, QtCore.SIGNAL("UpdateUi()"), self.UpdateUi)
			self.mainwindow = MainWindow
			
			self.thread.start()
			
		self.chkRest1 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest1.setObjectName(_fromUtf8("chkRest1"))
		self.chkRest1.stateChanged.connect(self.SetRest1)
		
		self.horizontalLayout_2.addWidget(self.chkRest1)
		self.chkRest2 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest2.setObjectName(_fromUtf8("chkRest2"))
		self.chkRest2.stateChanged.connect(self.SetRest2)
		
		self.horizontalLayout_2.addWidget(self.chkRest2)
		self.chkRest3 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest3.setObjectName(_fromUtf8("chkRest3"))
		self.chkRest3.stateChanged.connect(self.SetRest3)
		
		self.horizontalLayout_2.addWidget(self.chkRest3)
		self.chkRest4 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest4.setObjectName(_fromUtf8("chkRest4"))
		self.chkRest4.stateChanged.connect(self.SetRest4)
		
		self.horizontalLayout_2.addWidget(self.chkRest4)
		self.chkRest5 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest5.setObjectName(_fromUtf8("chkRest5"))
		self.chkRest5.stateChanged.connect(self.SetRest5)
		
		self.horizontalLayout_2.addWidget(self.chkRest5)
		self.chkRest6 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest6.setObjectName(_fromUtf8("chkRest6"))
		self.chkRest6.stateChanged.connect(self.SetRest6)
		
		self.horizontalLayout_2.addWidget(self.chkRest6)
		self.chkRest7 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest7.setObjectName(_fromUtf8("chkRest7"))
		self.chkRest7.stateChanged.connect(self.SetRest7)
		
		self.horizontalLayout_2.addWidget(self.chkRest7)
		self.chkRest8 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest8.setObjectName(_fromUtf8("chkRest8"))
		self.chkRest8.stateChanged.connect(self.SetRest8)
		
		self.horizontalLayout_2.addWidget(self.chkRest8)
		self.chkRest9 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest9.setObjectName(_fromUtf8("chkRest9"))
		self.chkRest9.stateChanged.connect(self.SetRest9)
		
		self.horizontalLayout_2.addWidget(self.chkRest9)
		self.chkRest10 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest10.setObjectName(_fromUtf8("chkRest10"))
		self.chkRest10.stateChanged.connect(self.SetRest10)
		
		self.horizontalLayout_2.addWidget(self.chkRest10)
		self.chkRest11 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest11.setObjectName(_fromUtf8("chkRest11"))
		self.horizontalLayout_2.addWidget(self.chkRest11)
		self.chkRest11.stateChanged.connect(self.SetRest11)
		
		self.chkRest12 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest12.setObjectName(_fromUtf8("chkRest12"))
		self.horizontalLayout_2.addWidget(self.chkRest12)
		self.chkRest12.stateChanged.connect(self.SetRest12)
		
		self.chkRest13 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest13.setObjectName(_fromUtf8("chkRest13"))
		self.horizontalLayout_2.addWidget(self.chkRest13)
		self.chkRest13.stateChanged.connect(self.SetRest13)
		
		self.chkRest14 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest14.setObjectName(_fromUtf8("chkRest14"))
		self.horizontalLayout_2.addWidget(self.chkRest14)
		self.chkRest14.stateChanged.connect(self.SetRest14)
		
		
		self.chkRest15 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest15.setObjectName(_fromUtf8("chkRest15"))
		self.horizontalLayout_2.addWidget(self.chkRest15)
		self.chkRest15.stateChanged.connect(self.SetRest15)
		
		self.chkRest16 = QtGui.QCheckBox(self.layoutWidget)
		self.chkRest16.setObjectName(_fromUtf8("chkRest16"))
		self.horizontalLayout_2.addWidget(self.chkRest16)
		self.chkRest16.stateChanged.connect(self.SetRest16)
		
		self.layoutWidget1 = QtGui.QWidget(self.centralwidget)
		self.layoutWidget1.setGeometry(QtCore.QRect(10, 210, 951, 41))
		self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
		self.horizontalLayout_4 = QtGui.QHBoxLayout(self.layoutWidget1)
		self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		self.sbPPQ1 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ1.setObjectName(_fromUtf8("sbPPQ1"))
		self.sbPPQ1.valueChanged.connect(self.SetPPQ1)
		
		self.horizontalLayout_4.addWidget(self.sbPPQ1)
		self.sbPPQ2 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ2.setObjectName(_fromUtf8("sbPPQ2"))
		self.sbPPQ2.valueChanged.connect(self.SetPPQ2)
		
		self.horizontalLayout_4.addWidget(self.sbPPQ2)
		self.sbPPQ3 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ3.setObjectName(_fromUtf8("sbPPQ3"))
		self.sbPPQ3.valueChanged.connect(self.SetPPQ3)
		
		self.horizontalLayout_4.addWidget(self.sbPPQ3)
		self.sbPPQ4 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ4.setObjectName(_fromUtf8("sbPPQ4"))
		self.horizontalLayout_4.addWidget(self.sbPPQ4)
		self.sbPPQ4.valueChanged.connect(self.SetPPQ4)
		
		self.sbPPQ5 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ5.setObjectName(_fromUtf8("sbPPQ5"))
		self.horizontalLayout_4.addWidget(self.sbPPQ5)
		self.sbPPQ5.valueChanged.connect(self.SetPPQ5)
		
		self.sbPPQ6 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ6.setObjectName(_fromUtf8("sbPPQ6"))
		self.sbPPQ6.valueChanged.connect(self.SetPPQ6)
		
		self.horizontalLayout_4.addWidget(self.sbPPQ6)
		self.sbPPQ7 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ7.setObjectName(_fromUtf8("sbPPQ7"))
		self.sbPPQ7.valueChanged.connect(self.SetPPQ7)
		
		self.horizontalLayout_4.addWidget(self.sbPPQ7)
		self.sbPPQ8 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ8.setObjectName(_fromUtf8("sbPPQ8"))
		self.sbPPQ8.valueChanged.connect(self.SetPPQ8)
		
		self.horizontalLayout_4.addWidget(self.sbPPQ8)
		self.sbPPQ9 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ9.setObjectName(_fromUtf8("sbPPQ9"))
		self.sbPPQ9.valueChanged.connect(self.SetPPQ9)
		
		self.horizontalLayout_4.addWidget(self.sbPPQ9)
		self.sbPPQ10 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ10.setObjectName(_fromUtf8("sbPPQ10"))
		self.horizontalLayout_4.addWidget(self.sbPPQ10)
		self.sbPPQ10.valueChanged.connect(self.SetPPQ10)
		
		self.sbPPQ11 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ11.setObjectName(_fromUtf8("sbPPQ11"))
		self.horizontalLayout_4.addWidget(self.sbPPQ11)
		self.sbPPQ11.valueChanged.connect(self.SetPPQ11)
		
		self.sbPPQ12 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ12.setObjectName(_fromUtf8("sbPPQ12"))
		self.horizontalLayout_4.addWidget(self.sbPPQ12)
		self.sbPPQ12.valueChanged.connect(self.SetPPQ12)
		
		self.sbPPQ13 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ13.setObjectName(_fromUtf8("sbPPQ13"))
		self.horizontalLayout_4.addWidget(self.sbPPQ13)
		self.sbPPQ13.valueChanged.connect(self.SetPPQ13)
		
		self.sbPPQ14 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ14.setObjectName(_fromUtf8("sbPPQ14"))
		self.horizontalLayout_4.addWidget(self.sbPPQ14)
		self.sbPPQ14.valueChanged.connect(self.SetPPQ14)
		
		self.sbPPQ15 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ15.setObjectName(_fromUtf8("sbPPQ15"))
		self.horizontalLayout_4.addWidget(self.sbPPQ15)
		self.sbPPQ15.valueChanged.connect(self.SetPPQ15)
		
		self.sbPPQ16 = QtGui.QSpinBox(self.layoutWidget1)
		self.sbPPQ16.setObjectName(_fromUtf8("sbPPQ16"))
		self.horizontalLayout_4.addWidget(self.sbPPQ16)
		self.sbPPQ16.valueChanged.connect(self.SetPPQ16)
		
		self.dRepeat3 = QtGui.QDial(self.centralwidget)
		self.dRepeat3.setGeometry(QtCore.QRect(130, 140, 50, 64))
		self.dRepeat3.setMaximum(7)
		self.dRepeat3.setObjectName(_fromUtf8("dRepeat3"))
		self.dRepeat3.valueChanged.connect(self.SetRepeat3)
		
		self.dRepeat8 = QtGui.QDial(self.centralwidget)
		self.dRepeat8.setGeometry(QtCore.QRect(430, 140, 50, 64))
		self.dRepeat8.setMaximum(7)		
		self.dRepeat8.setObjectName(_fromUtf8("dRepeat8"))
		self.dRepeat8.valueChanged.connect(self.SetRepeat8)
		
		self.dRepeat15 = QtGui.QDial(self.centralwidget)
		self.dRepeat15.setGeometry(QtCore.QRect(850, 140, 50, 64))
		self.dRepeat15.setMaximum(7)
		self.dRepeat15.setObjectName(_fromUtf8("dRepeat15"))
		self.dRepeat15.valueChanged.connect(self.SetRepeat15)
		self.dRepeat10 = QtGui.QDial(self.centralwidget)
		self.dRepeat10.setGeometry(QtCore.QRect(550, 140, 50, 64))
		self.dRepeat10.setMaximum(7)
		self.dRepeat10.setObjectName(_fromUtf8("dRepeat10"))
		self.dRepeat10.valueChanged.connect(self.SetRepeat10)
		self.dRepeat9 = QtGui.QDial(self.centralwidget)
		self.dRepeat9.setGeometry(QtCore.QRect(490, 140, 50, 64))
		self.dRepeat9.setMaximum(7)
		self.dRepeat9.setObjectName(_fromUtf8("dRepeat9"))
		self.dRepeat9.valueChanged.connect(self.SetRepeat9)
		self.dRepeat2 = QtGui.QDial(self.centralwidget)
		self.dRepeat2.setGeometry(QtCore.QRect(70, 140, 50, 64))
		self.dRepeat2.setMaximum(7)
		self.dRepeat2.setObjectName(_fromUtf8("dRepeat2"))
		self.dRepeat2.valueChanged.connect(self.SetRepeat2)
		self.dRepeat14 = QtGui.QDial(self.centralwidget)
		self.dRepeat14.setGeometry(QtCore.QRect(790, 140, 50, 64))
		self.dRepeat14.setMaximum(7)
		self.dRepeat14.setObjectName(_fromUtf8("dRepeat14"))
		self.dRepeat14.valueChanged.connect(self.SetRepeat14)
		self.dRepeat13 = QtGui.QDial(self.centralwidget)
		self.dRepeat13.setGeometry(QtCore.QRect(730, 140, 50, 64))
		self.dRepeat13.setMaximum(7)
		self.dRepeat13.setObjectName(_fromUtf8("dRepeat13"))
		self.dRepeat13.valueChanged.connect(self.SetRepeat13)
		self.dRepeat1 = QtGui.QDial(self.centralwidget)
		self.dRepeat1.setGeometry(QtCore.QRect(10, 140, 50, 64))
		self.dRepeat1.setMaximum(7)
		self.dRepeat1.setObjectName(_fromUtf8("dRepeat1"))
		self.dRepeat1.valueChanged.connect(self.SetRepeat1)
		self.dRepeat7 = QtGui.QDial(self.centralwidget)
		self.dRepeat7.setGeometry(QtCore.QRect(370, 140, 50, 64))
		self.dRepeat7.setMaximum(7)
		self.dRepeat7.setObjectName(_fromUtf8("dRepeat7"))
		self.dRepeat7.valueChanged.connect(self.SetRepeat7)
		self.dRepeat5 = QtGui.QDial(self.centralwidget)
		self.dRepeat5.setGeometry(QtCore.QRect(250, 140, 50, 64))
		self.dRepeat5.setMaximum(7)
		self.dRepeat5.setObjectName(_fromUtf8("dRepeat5"))
		self.dRepeat5.valueChanged.connect(self.SetRepeat5)
		self.dRepeat6 = QtGui.QDial(self.centralwidget)
		self.dRepeat6.setGeometry(QtCore.QRect(310, 140, 50, 64))
		self.dRepeat6.setMaximum(7)
		self.dRepeat6.setObjectName(_fromUtf8("dRepeat6"))
		self.dRepeat6.valueChanged.connect(self.SetRepeat6)
		self.dRepeat16 = QtGui.QDial(self.centralwidget)
		self.dRepeat16.setGeometry(QtCore.QRect(910, 140, 50, 64))
		self.dRepeat16.setMaximum(7)
		self.dRepeat16.setObjectName(_fromUtf8("dRepeat16"))
		self.dRepeat15.valueChanged.connect(self.SetRepeat16)
		self.dRepeat12 = QtGui.QDial(self.centralwidget)
		self.dRepeat12.setGeometry(QtCore.QRect(670, 140, 50, 64))
		self.dRepeat12.setMaximum(7)
		self.dRepeat12.setObjectName(_fromUtf8("dRepeat12"))
		self.dRepeat12.valueChanged.connect(self.SetRepeat12)
		self.dRepeat4 = QtGui.QDial(self.centralwidget)
		self.dRepeat4.setGeometry(QtCore.QRect(190, 140, 50, 64))
		self.dRepeat4.setMaximum(7)
		self.dRepeat4.setObjectName(_fromUtf8("dRepeat4"))
		self.dRepeat4.valueChanged.connect(self.SetRepeat4)
		self.dRepeat11 = QtGui.QDial(self.centralwidget)
		self.dRepeat11.setGeometry(QtCore.QRect(610, 140, 50, 64))
		self.dRepeat11.setMaximum(7)
		self.dRepeat11.setObjectName(_fromUtf8("dRepeat11"))
		self.dRepeat11.valueChanged.connect(self.SetRepeat11)
		
		self.cbMidiPort = QtGui.QComboBox(self.centralwidget)
		self.cbMidiPort.setGeometry(QtCore.QRect(20, 20, 161, 22))
		self.cbMidiPort.setObjectName(_fromUtf8("cbMidiPort"))
		self.cbMidiPort.currentIndexChanged.connect(self.SetMidiPort)
		
		outp = mido.get_output_names()
		self.cbMidiPort.addItem('None')
		for o in outp:
			self.cbMidiPort.addItem(o)
			
		self.label = QtGui.QLabel(self.centralwidget)		
		self.label.setGeometry(QtCore.QRect(20, 0, 71, 16))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(190, 0, 46, 13))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		
		self.sbChannel = QtGui.QSpinBox(self.centralwidget)
		self.sbChannel.setGeometry(QtCore.QRect(190, 20, 42, 22))
		self.sbChannel.setObjectName(_fromUtf8("sbChannel"))
		self.sbChannel.valueChanged.connect(self.SetMidiChannel)
		
		self.labelBanks = QtGui.QLabel(self.centralwidget)
		self.labelBanks.setGeometry(QtCore.QRect(250, 0, 46, 13))
		self.labelBanks.setObjectName(_fromUtf8("label_6"))
		
		self.sbBanks = QtGui.QSpinBox(self.centralwidget)
		self.sbBanks.setGeometry(QtCore.QRect(250, 20, 42, 22))
		self.sbBanks.setObjectName(_fromUtf8("sbVoice"))
		self.sbBanks.valueChanged.connect(self.ChangeBanks)
		
		self.labelVoices = QtGui.QLabel(self.centralwidget)
		self.labelVoices.setGeometry(QtCore.QRect(300, 0, 46, 13))
		self.labelVoices.setObjectName(_fromUtf8("labelVoices"))
		
		self.sbVoices = QtGui.QSpinBox(self.centralwidget)
		self.sbVoices.setGeometry(QtCore.QRect(300, 20, 42, 22))
		self.sbVoices.setObjectName(_fromUtf8("sbVoice"))
		self.sbBanks.valueChanged.connect(self.ChangeVoices)
		
		self.label_3 = QtGui.QLabel(self.centralwidget)
		self.label_3.setGeometry(QtCore.QRect(400, 0, 46, 13))
		self.label_3.setObjectName(_fromUtf8("label_4"))
		
		self.sbSeq = QtGui.QSpinBox(self.centralwidget)
		self.sbSeq.setGeometry(QtCore.QRect(400, 20, 42, 22))
		self.sbSeq.setObjectName(_fromUtf8("sbSeq"))
		self.sbSeq.valueChanged.connect(self.CurSeq)
		self.sbSeq.setMinimum(1)
		self.sbSeq.setMaximum(512)
		
		self.label_4 = QtGui.QLabel(self.centralwidget)
		self.label_4.setGeometry(QtCore.QRect(500, 0, 46, 13))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		
		self.sbRow = QtGui.QSpinBox(self.centralwidget)
		self.sbRow.setGeometry(QtCore.QRect(500, 20, 42, 22))
		self.sbRow.setObjectName(_fromUtf8("sbRow"))
		self.sbRow.valueChanged.connect(self.CurBank)
		
		self.label_5 = QtGui.QLabel(self.centralwidget)
		self.label_5.setGeometry(QtCore.QRect(550, 0, 46, 13))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		
		self.sbSteps = QtGui.QSpinBox(self.centralwidget)
		self.sbSteps.setGeometry(QtCore.QRect(550, 20, 42, 22))
		self.sbSteps.setObjectName(_fromUtf8("sbSteps"))
		self.sbSteps.valueChanged.connect(self.SetSteps)
		
		self.pbStart = QtGui.QPushButton(self.centralwidget)
		self.pbStart.setGeometry(QtCore.QRect(750, 10, 75, 23))
		self.pbStart.setObjectName(_fromUtf8("pbStart"))
		self.pbStart.toggled.connect(self.Panic)
		
		self.label_6 = QtGui.QLabel(self.centralwidget)
		self.label_6.setGeometry(QtCore.QRect(450, 0, 46, 13))
		self.label_6.setObjectName(_fromUtf8("label_6"))
		
		self.sbVoice = QtGui.QSpinBox(self.centralwidget)
		self.sbVoice.setGeometry(QtCore.QRect(450, 20, 42, 22))
		self.sbVoice.setObjectName(_fromUtf8("sbVoice"))
		self.sbVoice.valueChanged.connect(self.CurVoice)
		
		self.groupBox = QtGui.QGroupBox(self.centralwidget)
		self.groupBox.setGeometry(QtCore.QRect(20, 250, 111, 225))
		self.groupBox.setObjectName(_fromUtf8("groupBox"))
		self.widget = QtGui.QWidget(self.groupBox)
		self.widget.setGeometry(QtCore.QRect(10, 20, 91, 201))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.widget)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.rbA = QtGui.QRadioButton(self.widget)
		self.rbA.setChecked(True)
		self.rbA.setObjectName(_fromUtf8("rbA"))
		self.rbA.toggled.connect(self.VarA)
		self.verticalLayout.addWidget(self.rbA)
		self.rbB = QtGui.QRadioButton(self.widget)
		self.rbB.setObjectName(_fromUtf8("rbB"))
		self.rbB.toggled.connect(self.VarB)
		self.verticalLayout.addWidget(self.rbB)
		self.rbC = QtGui.QRadioButton(self.widget)
		self.rbC.setObjectName(_fromUtf8("rbC"))
		self.rbC.toggled.connect(self.VarC)
		self.verticalLayout.addWidget(self.rbC)
		self.rbD = QtGui.QRadioButton(self.widget)
		self.rbD.setObjectName(_fromUtf8("rbD"))
		self.rbD.toggled.connect(self.VarD)
		self.verticalLayout.addWidget(self.rbD)
		self.rbE = QtGui.QRadioButton(self.widget)
		self.rbE.setObjectName(_fromUtf8("rbE"))
		self.rbE.toggled.connect(self.VarE)
		self.verticalLayout.addWidget(self.rbE)
		self.rbF = QtGui.QRadioButton(self.widget)
		self.rbF.setObjectName(_fromUtf8("rbF"))
		self.rbF.toggled.connect(self.VarF)
		self.verticalLayout.addWidget(self.rbF)
		self.rbG = QtGui.QRadioButton(self.widget)
		self.rbG.setObjectName(_fromUtf8("rbG"))
		self.rbG.toggled.connect(self.VarG)
		self.verticalLayout.addWidget(self.rbG)
		self.rbH = QtGui.QRadioButton(self.widget)
		self.rbH.setObjectName(_fromUtf8("rbH"))
		self.verticalLayout.addWidget(self.rbH)
		self.rbH.toggled.connect(self.VarH)
		self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
		self.groupBox_2.setGeometry(QtCore.QRect(140, 250, 521, 221))
		self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
		
		self.sbCC5 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC5.setGeometry(QtCore.QRect(270, 90, 42, 22))
		self.sbCC5.setObjectName(_fromUtf8("sbCC5"))
		self.sbCC5.setMinimum(0)
		self.sbCC5.setMaximum(127)
		self.sbCC5.setValue(106)
		
		self.sbCC1 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC1.setGeometry(QtCore.QRect(10, 90, 42, 22))
		self.sbCC1.setObjectName(_fromUtf8("sbCC1"))
		self.sbCC1.setMinimum(0)
		self.sbCC1.setMaximum(127)
		self.sbCC1.setValue(102)
		
		self.sbCC8 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC8.setGeometry(QtCore.QRect(460, 90, 42, 22))
		self.sbCC8.setObjectName(_fromUtf8("sbCC8"))
		self.sbCC8.setMinimum(0)
		self.sbCC8.setMaximum(127)
		self.sbCC8.setValue(109)
		
		self.dMotion16 = QtGui.QDial(self.groupBox_2)
		self.dMotion16.setGeometry(QtCore.QRect(450, 120, 50, 64))
		self.dMotion16.setObjectName(_fromUtf8("dMotion16"))
		self.dMotion16.setMinimum(0)
		self.dMotion16.setMaximum(127)
		self.dMotion16.valueChanged.connect(self.Motion16)
		
		self.sbCC11 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC11.setGeometry(QtCore.QRect(140, 190, 42, 22))
		self.sbCC11.setObjectName(_fromUtf8("sbCC11"))
		self.sbCC11.setMinimum(0)
		self.sbCC11.setMaximum(127)
		self.sbCC11.setValue(112)
		
		self.sbCC14 = QtGui.QSpinBox(self.groupBox_2)		
		self.sbCC14.setGeometry(QtCore.QRect(330, 190, 42, 22))
		self.sbCC14.setObjectName(_fromUtf8("sbCC14"))
		self.sbCC14.setMinimum(0)
		self.sbCC14.setMaximum(127)
		
		self.sbCC7 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC7.setGeometry(QtCore.QRect(400, 90, 42, 22))
		self.sbCC7.setObjectName(_fromUtf8("sbCC7"))
		self.sbCC7.setMinimum(0)
		self.sbCC7.setMaximum(127)
		self.sbCC7.setValue(108)
		
		self.dMotion15 = QtGui.QDial(self.groupBox_2)
		self.dMotion15.setGeometry(QtCore.QRect(390, 120, 50, 64))
		self.dMotion15.setObjectName(_fromUtf8("dMotion15"))
		self.dMotion15.setMinimum(0)
		self.dMotion15.setMaximum(127)
		self.dMotion15.valueChanged.connect(self.Motion15)
		
		self.sbCC9 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC9.setGeometry(QtCore.QRect(10, 190, 42, 22))
		self.sbCC9.setObjectName(_fromUtf8("sbCC9"))
		self.sbCC9.setMinimum(0)
		self.sbCC9.setMaximum(127)
		self.sbCC9.setValue(110)
		
		self.dMotion8 = QtGui.QDial(self.groupBox_2)
		self.dMotion8.setGeometry(QtCore.QRect(450, 20, 50, 64))
		self.dMotion8.setObjectName(_fromUtf8("dMotion8"))
		self.dMotion8.setMinimum(0)
		self.dMotion8.setMaximum(127)
		self.dMotion8.valueChanged.connect(self.Motion8)
		
		self.dMotion2 = QtGui.QDial(self.groupBox_2)
		self.dMotion2.setGeometry(QtCore.QRect(60, 20, 50, 64))
		self.dMotion2.setObjectName(_fromUtf8("dMotion2"))
		self.dMotion2.setMinimum(0)
		self.dMotion2.setMaximum(127)
		self.dMotion2.valueChanged.connect(self.Motion2)
		
		
		self.dMotion10 = QtGui.QDial(self.groupBox_2)
		self.dMotion10.setGeometry(QtCore.QRect(60, 120, 50, 64))
		self.dMotion10.setObjectName(_fromUtf8("dMotion10"))
		self.dMotion10.setMinimum(0)
		self.dMotion10.setMaximum(127)
		self.dMotion10.valueChanged.connect(self.Motion10)
		
		
		self.sbCC10 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC10.setGeometry(QtCore.QRect(70, 190, 42, 22))
		self.sbCC10.setObjectName(_fromUtf8("sbCC10"))
		self.sbCC10.setMinimum(0)
		self.sbCC10.setMaximum(127)
		self.sbCC10.setValue(111)
		
		self.sbCC4 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC4.setGeometry(QtCore.QRect(200, 90, 42, 22))
		self.sbCC4.setObjectName(_fromUtf8("sbCC4"))
		self.sbCC4.setMinimum(0)
		self.sbCC4.setMaximum(127)
		self.sbCC4.setValue(105)
		
		self.dMotion4 = QtGui.QDial(self.groupBox_2)
		self.dMotion4.setGeometry(QtCore.QRect(190, 20, 50, 64))
		self.dMotion4.setObjectName(_fromUtf8("dMotion4"))
		self.dMotion4.setMinimum(0)
		self.dMotion4.setMaximum(127)
		self.dMotion4.valueChanged.connect(self.Motion4)
		
		self.dMotion6 = QtGui.QDial(self.groupBox_2)
		self.dMotion6.setGeometry(QtCore.QRect(320, 20, 50, 64))
		self.dMotion6.setObjectName(_fromUtf8("dMotion6"))
		self.dMotion6.setMinimum(0)
		self.dMotion6.setMaximum(127)
		self.dMotion6.valueChanged.connect(self.Motion6)
		
		self.sbCC3 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC3.setGeometry(QtCore.QRect(140, 90, 42, 22))
		self.sbCC3.setObjectName(_fromUtf8("sbCC3"))
		self.sbCC3.setMinimum(0)
		self.sbCC3.setMaximum(127)		
		self.sbCC3.setValue(104)
		
		self.dMotion14 = QtGui.QDial(self.groupBox_2)
		self.dMotion14.setGeometry(QtCore.QRect(320, 120, 50, 64))
		self.dMotion14.setObjectName(_fromUtf8("dMotion14"))
		self.dMotion14.setMinimum(0)
		self.dMotion14.setMaximum(127)
		self.dMotion14.valueChanged.connect(self.Motion14)
		
		
		self.dMotion12 = QtGui.QDial(self.groupBox_2)
		self.dMotion12.setGeometry(QtCore.QRect(190, 120, 50, 64))
		self.dMotion12.setObjectName(_fromUtf8("dMotion12"))
		self.dMotion12.setMinimum(0)
		self.dMotion12.setMaximum(127)
		self.dMotion12.valueChanged.connect(self.Motion12)
		
		
		self.dMotion1 = QtGui.QDial(self.groupBox_2)
		self.dMotion1.setGeometry(QtCore.QRect(0, 20, 50, 64))
		self.dMotion1.setObjectName(_fromUtf8("dMotion1"))
		self.dMotion1.setMinimum(0)
		self.dMotion1.setMaximum(127)
		self.dMotion1.valueChanged.connect(self.Motion1)
		
		
		self.dMotion7 = QtGui.QDial(self.groupBox_2)
		self.dMotion7.setGeometry(QtCore.QRect(390, 20, 50, 64))
		self.dMotion7.setObjectName(_fromUtf8("dMotion7"))
		self.dMotion7.setMinimum(0)
		self.dMotion7.setMaximum(127)
		self.dMotion7.valueChanged.connect(self.Motion7)
		
		self.sbCC12 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC12.setGeometry(QtCore.QRect(200, 190, 42, 22))
		self.sbCC12.setObjectName(_fromUtf8("sbCC12"))
		self.sbCC12.setMinimum(0)
		self.sbCC12.setMaximum(127)
		
		self.sbCC6 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC6.setGeometry(QtCore.QRect(330, 90, 42, 22))
		self.sbCC6.setObjectName(_fromUtf8("sbCC6"))
		self.sbCC6.setMinimum(0)
		self.sbCC6.setMaximum(127)
		self.sbCC6.setValue(107)
		
		self.dMotion9 = QtGui.QDial(self.groupBox_2)
		self.dMotion9.setGeometry(QtCore.QRect(0, 120, 50, 64))
		self.dMotion9.setObjectName(_fromUtf8("dMotion9"))
		self.dMotion9.setMinimum(0)
		self.dMotion9.setMaximum(127)
		self.dMotion9.valueChanged.connect(self.Motion9)
		
		self.sbCC16 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC16.setGeometry(QtCore.QRect(460, 190, 42, 22))
		self.sbCC16.setObjectName(_fromUtf8("sbCC16"))
		self.sbCC16.setMinimum(0)
		self.sbCC16.setMaximum(127)
		
		self.dMotion13 = QtGui.QDial(self.groupBox_2)
		self.dMotion13.setGeometry(QtCore.QRect(260, 120, 50, 64))
		self.dMotion13.setObjectName(_fromUtf8("dMotion13"))
		self.dMotion13.setMinimum(0)
		self.dMotion13.setMaximum(1024)
		self.dMotion13.valueChanged.connect(self.Motion13)
		
		self.sbCC2 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC2.setGeometry(QtCore.QRect(70, 90, 42, 22))
		self.sbCC2.setObjectName(_fromUtf8("sbCC2"))
		self.sbCC2.setMinimum(0)
		self.sbCC2.setMaximum(127)
		self.sbCC2.setValue(103)
		
		self.dMotion3 = QtGui.QDial(self.groupBox_2)
		self.dMotion3.setGeometry(QtCore.QRect(130, 20, 50, 64))
		self.dMotion3.setObjectName(_fromUtf8("dMotion3"))
		self.dMotion3.setMinimum(0)
		self.dMotion3.setMaximum(127)
		self.dMotion3.valueChanged.connect(self.Motion3)
		
		self.dMotion5 = QtGui.QDial(self.groupBox_2)
		self.dMotion5.setGeometry(QtCore.QRect(260, 20, 50, 64))
		self.dMotion5.setObjectName(_fromUtf8("dMotion5"))
		self.dMotion5.setMinimum(0)
		self.dMotion5.setMaximum(127)
		self.dMotion5.valueChanged.connect(self.Motion5)
		
		self.sbCC15 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC15.setGeometry(QtCore.QRect(400, 190, 42, 22))
		self.sbCC15.setObjectName(_fromUtf8("sbCC15"))
		self.sbCC15.setMinimum(0)
		self.sbCC15.setMaximum(127)
		
		self.sbCC13 = QtGui.QSpinBox(self.groupBox_2)
		self.sbCC13.setGeometry(QtCore.QRect(270, 190, 42, 22))
		self.sbCC13.setObjectName(_fromUtf8("sbCC13"))
		self.sbCC13.setMinimum(0)
		self.sbCC13.setMaximum(127)
		
		self.dMotion11 = QtGui.QDial(self.groupBox_2)
		self.dMotion11.setGeometry(QtCore.QRect(130, 120, 50, 64))
		self.dMotion11.setObjectName(_fromUtf8("dMotion11"))
		self.dMotion11.setMinimum(0)
		self.dMotion11.setMaximum(127)
		self.dMotion11.valueChanged.connect(self.Motion11)
		
		self.cbNote1 = QtGui.QComboBox(self.centralwidget)
		self.cbNote1.setGeometry(QtCore.QRect(10, 70, 61, 22))
		self.cbNote1.setObjectName(_fromUtf8("cbNote1"))
		self.cbNote2 = QtGui.QComboBox(self.centralwidget)
		self.cbNote2.setGeometry(QtCore.QRect(70, 70, 61, 22))
		self.cbNote2.setObjectName(_fromUtf8("cbNote2"))
		self.cbNote3 = QtGui.QComboBox(self.centralwidget)
		self.cbNote3.setGeometry(QtCore.QRect(130, 70, 61, 22))
		self.cbNote3.setObjectName(_fromUtf8("cbNote3"))
		self.cbNote4 = QtGui.QComboBox(self.centralwidget)
		self.cbNote4.setGeometry(QtCore.QRect(190, 70, 61, 22))
		self.cbNote4.setObjectName(_fromUtf8("cbNote4"))
		self.cbNote5 = QtGui.QComboBox(self.centralwidget)
		self.cbNote5.setGeometry(QtCore.QRect(250, 70, 61, 22))
		self.cbNote5.setObjectName(_fromUtf8("cbNote5"))
		self.cbNote7 = QtGui.QComboBox(self.centralwidget)
		self.cbNote7.setGeometry(QtCore.QRect(370, 70, 61, 22))
		self.cbNote7.setObjectName(_fromUtf8("cbNote7"))
		self.cbNote6 = QtGui.QComboBox(self.centralwidget)
		self.cbNote6.setGeometry(QtCore.QRect(310, 70, 61, 22))
		self.cbNote6.setObjectName(_fromUtf8("cbNote6"))
		self.cbNote8 = QtGui.QComboBox(self.centralwidget)
		self.cbNote8.setGeometry(QtCore.QRect(430, 70, 61, 22))
		self.cbNote8.setObjectName(_fromUtf8("cbNote8"))
		self.cbNote9 = QtGui.QComboBox(self.centralwidget)
		self.cbNote9.setGeometry(QtCore.QRect(490, 70, 61, 22))
		self.cbNote9.setObjectName(_fromUtf8("cbNote9"))
		self.cbNote15 = QtGui.QComboBox(self.centralwidget)
		self.cbNote15.setGeometry(QtCore.QRect(850, 70, 61, 22))
		self.cbNote15.setObjectName(_fromUtf8("cbNote15"))
		self.cbNote11 = QtGui.QComboBox(self.centralwidget)
		self.cbNote11.setGeometry(QtCore.QRect(610, 70, 61, 22))
		self.cbNote11.setObjectName(_fromUtf8("cbNote11"))
		self.cbNote14 = QtGui.QComboBox(self.centralwidget)
		self.cbNote14.setGeometry(QtCore.QRect(790, 70, 61, 22))
		self.cbNote14.setObjectName(_fromUtf8("cbNote14"))
		self.cbNote16 = QtGui.QComboBox(self.centralwidget)
		self.cbNote16.setGeometry(QtCore.QRect(910, 70, 61, 22))
		self.cbNote16.setObjectName(_fromUtf8("cbNote16"))
		self.cbNote10 = QtGui.QComboBox(self.centralwidget)
		self.cbNote10.setGeometry(QtCore.QRect(550, 70, 61, 22))
		self.cbNote10.setObjectName(_fromUtf8("cbNote10"))
		self.cbNote12 = QtGui.QComboBox(self.centralwidget)
		self.cbNote12.setGeometry(QtCore.QRect(670, 70, 61, 22))
		self.cbNote12.setObjectName(_fromUtf8("cbNote12"))
		self.cbNote13 = QtGui.QComboBox(self.centralwidget)
		self.cbNote13.setGeometry(QtCore.QRect(730, 70, 61, 22))
		self.cbNote13.setObjectName(_fromUtf8("cbNote13"))
		
		self.cbNote1.currentIndexChanged.connect(self.SetNote1)
		self.cbNote2.currentIndexChanged.connect(self.SetNote2)
		self.cbNote3.currentIndexChanged.connect(self.SetNote3)
		self.cbNote4.currentIndexChanged.connect(self.SetNote4)
		self.cbNote5.currentIndexChanged.connect(self.SetNote5)
		self.cbNote6.currentIndexChanged.connect(self.SetNote6)
		self.cbNote7.currentIndexChanged.connect(self.SetNote7)
		self.cbNote8.currentIndexChanged.connect(self.SetNote8)
		self.cbNote9.currentIndexChanged.connect(self.SetNote9)
		self.cbNote10.currentIndexChanged.connect(self.SetNote10)
		self.cbNote11.currentIndexChanged.connect(self.SetNote11)
		self.cbNote12.currentIndexChanged.connect(self.SetNote12)
		self.cbNote13.currentIndexChanged.connect(self.SetNote13)
		self.cbNote14.currentIndexChanged.connect(self.SetNote14)
		self.cbNote15.currentIndexChanged.connect(self.SetNote15)
		self.cbNote16.currentIndexChanged.connect(self.SetNote16)
		
		for c in note_names:
			
			self.cbNote1.addItem(c)
			self.cbNote2.addItem(c)
			self.cbNote3.addItem(c)
			self.cbNote4.addItem(c)
			self.cbNote5.addItem(c)
			self.cbNote6.addItem(c)
			self.cbNote7.addItem(c)
			self.cbNote8.addItem(c)
			self.cbNote9.addItem(c)
			self.cbNote10.addItem(c)
			self.cbNote11.addItem(c)
			self.cbNote12.addItem(c)
			self.cbNote13.addItem(c)
			self.cbNote14.addItem(c)
			self.cbNote15.addItem(c)
			self.cbNote16.addItem(c)
		
		self.lcdNumber.raise_()
		self.layoutWidget.raise_()
		self.layoutWidget.raise_()
		self.dRepeat3.raise_()
		self.dRepeat8.raise_()
		self.dRepeat15.raise_()
		self.dRepeat10.raise_()
		self.dRepeat9.raise_()
		self.dRepeat2.raise_()
		self.dRepeat14.raise_()
		self.dRepeat13.raise_()
		self.dRepeat1.raise_()
		self.dRepeat7.raise_()
		self.dRepeat5.raise_()
		self.dRepeat6.raise_()
		self.dRepeat16.raise_()
		self.dRepeat12.raise_()
		self.dRepeat4.raise_()
		self.dRepeat11.raise_()
		self.chkRest10.raise_()
		self.chkRest10.raise_()
		self.cbMidiPort.raise_()
		self.label.raise_()
		self.label_2.raise_()
		self.sbChannel.raise_()
		self.label_3.raise_()
		self.sbSeq.raise_()
		self.label_4.raise_()
		self.sbRow.raise_()
		self.label_5.raise_()
		self.sbSteps.raise_()
		self.pbStart.raise_()
		self.label_6.raise_()
		self.sbVoice.raise_()
		self.groupBox.raise_()
		self.groupBox_2.raise_()
		self.cbNote1.raise_()
		self.cbNote2.raise_()
		self.cbNote3.raise_()
		self.cbNote4.raise_()
		self.cbNote5.raise_()
		self.cbNote7.raise_()
		self.cbNote6.raise_()
		self.cbNote8.raise_()
		self.cbNote9.raise_()
		self.cbNote15.raise_()
		self.cbNote11.raise_()
		self.cbNote14.raise_()
		self.cbNote16.raise_()
		self.cbNote10.raise_()
		self.cbNote12.raise_()
		self.cbNote13.raise_()
		

		self.groupBoxMatrix = QtGui.QGroupBox(self.centralwidget)
		self.groupBoxMatrix.setGeometry(QtCore.QRect(660, 250, 61, 221))
		self.groupBoxMatrix.setObjectName(_fromUtf8("groupBoxMatrix"))
		self.chkMatrix = QtGui.QCheckBox(self.groupBoxMatrix)
		self.chkMatrix.setGeometry(QtCore.QRect(10, 200, 50, 16))
		self.chkMatrix.setObjectName(_fromUtf8("chkMatrix"))
		self.widget = QtGui.QWidget(self.groupBoxMatrix)
		self.widget.setGeometry(QtCore.QRect(10, 10, 50, 181))
		self.widget.setObjectName(_fromUtf8("widget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.widget)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.rbMatrix1 = QtGui.QRadioButton(self.widget)
		self.rbMatrix1.setObjectName(_fromUtf8("rbMatrix1"))
		self.verticalLayout.addWidget(self.rbMatrix1)
		self.rbMatrix2 = QtGui.QRadioButton(self.widget)
		self.rbMatrix2.setObjectName(_fromUtf8("rbMatrix2"))
		self.verticalLayout.addWidget(self.rbMatrix2)
		self.rbMatrix3 = QtGui.QRadioButton(self.widget)
		self.rbMatrix3.setObjectName(_fromUtf8("rbMatrix3"))
		self.verticalLayout.addWidget(self.rbMatrix3)
		self.rbMatrix4 = QtGui.QRadioButton(self.widget)
		self.rbMatrix4.setObjectName(_fromUtf8("rbMatrix4"))
		self.verticalLayout.addWidget(self.rbMatrix4)
		self.rbMatrix5 = QtGui.QRadioButton(self.widget)
		self.rbMatrix5.setObjectName(_fromUtf8("rbMatrix5"))
		self.verticalLayout.addWidget(self.rbMatrix5)
		self.rbMatrix6 = QtGui.QRadioButton(self.widget)
		self.rbMatrix6.setObjectName(_fromUtf8("rbMatrix6"))
		self.verticalLayout.addWidget(self.rbMatrix6)
		self.rbMatrix7 = QtGui.QRadioButton(self.widget)
		self.rbMatrix7.setObjectName(_fromUtf8("rbMatrix7"))
		self.verticalLayout.addWidget(self.rbMatrix7)
		self.rbMatrix8 = QtGui.QRadioButton(self.widget)
		self.rbMatrix8.setObjectName(_fromUtf8("rbMatrix8"))
		self.verticalLayout.addWidget(self.rbMatrix8)
		self.groupBoxShiftCore = QtGui.QGroupBox(self.centralwidget)
		self.groupBoxShiftCore.setGeometry(QtCore.QRect(720, 250, 121, 221))
		self.groupBoxShiftCore.setObjectName(_fromUtf8("groupBoxShiftCore"))
		self.chkShiftCore = QtGui.QCheckBox(self.groupBoxShiftCore)
		self.chkShiftCore.setGeometry(QtCore.QRect(20, 200, 70, 17))
		self.chkShiftCore.setObjectName(_fromUtf8("chkShiftCore"))
		self.groupBox_3 = QtGui.QGroupBox(self.groupBoxShiftCore)
		self.groupBox_3.setGeometry(QtCore.QRect(10, 105, 100, 86))
		self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
		self.widget1 = QtGui.QWidget(self.groupBox_3)
		self.widget1.setGeometry(QtCore.QRect(10, 10, 71, 61))
		self.widget1.setObjectName(_fromUtf8("widget1"))
		self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget1)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.rbLeft = QtGui.QRadioButton(self.widget1)
		self.rbLeft.setObjectName(_fromUtf8("rbLeft"))
		self.verticalLayout_2.addWidget(self.rbLeft)
		self.rbRight = QtGui.QRadioButton(self.widget1)
		self.rbRight.setObjectName(_fromUtf8("rbRight"))
		self.verticalLayout_2.addWidget(self.rbRight)
		self.rbRandom = QtGui.QRadioButton(self.widget1)
		self.rbRandom.setObjectName(_fromUtf8("rbRandom"))
		self.verticalLayout_2.addWidget(self.rbRandom)
		self.widget2 = QtGui.QWidget(self.groupBoxShiftCore)
		self.widget2.setGeometry(QtCore.QRect(10, 20, 61, 91))
		self.widget2.setObjectName(_fromUtf8("widget2"))
		self.verticalLayout_6 = QtGui.QVBoxLayout(self.widget2)
		self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
		self.rbShift1 = QtGui.QRadioButton(self.widget2)
		self.rbShift1.setObjectName(_fromUtf8("rbShift1"))
		self.verticalLayout_6.addWidget(self.rbShift1)
		self.rbShift2 = QtGui.QRadioButton(self.widget2)
		self.rbShift2.setObjectName(_fromUtf8("rbShift2"))
		self.verticalLayout_6.addWidget(self.rbShift2)
		self.rbShiftR = QtGui.QRadioButton(self.widget2)
		self.rbShiftR.setObjectName(_fromUtf8("rbShiftR"))
		self.verticalLayout_6.addWidget(self.rbShiftR)
		self.rbShift3 = QtGui.QRadioButton(self.widget2)
		self.rbShift3.setObjectName(_fromUtf8("rbShift3"))
		self.verticalLayout_6.addWidget(self.rbShift3)
		self.rbShift5 = QtGui.QRadioButton(self.widget2)
		self.rbShift5.setObjectName(_fromUtf8("rbShift5"))
		self.verticalLayout_6.addWidget(self.rbShift5)
		self.widget3 = QtGui.QWidget(self.groupBoxShiftCore)
		self.widget3.setGeometry(QtCore.QRect(70, 20, 51, 91))
		self.widget3.setObjectName(_fromUtf8("widget3"))
		self.verticalLayout_7 = QtGui.QVBoxLayout(self.widget3)
		self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
		self.rbShift8 = QtGui.QRadioButton(self.widget3)
		self.rbShift8.setObjectName(_fromUtf8("rbShift8"))
		self.verticalLayout_7.addWidget(self.rbShift8)
		self.rbShift13 = QtGui.QRadioButton(self.widget3)
		self.rbShift13.setObjectName(_fromUtf8("rbShift13"))
		self.verticalLayout_7.addWidget(self.rbShift13)
		self.rbShift21 = QtGui.QRadioButton(self.widget3)
		self.rbShift21.setObjectName(_fromUtf8("rbShift21"))
		self.verticalLayout_7.addWidget(self.rbShift21)
		self.rbShift34 = QtGui.QRadioButton(self.widget3)
		self.rbShift34.setObjectName(_fromUtf8("rbShift34"))
		self.verticalLayout_7.addWidget(self.rbShift34)
		self.rbShift55 = QtGui.QRadioButton(self.widget3)
		self.rbShift55.setObjectName(_fromUtf8("rbShift55"))
		self.verticalLayout_7.addWidget(self.rbShift55)
		self.groupBoxTranspose = QtGui.QGroupBox(self.centralwidget)
		self.groupBoxTranspose.setGeometry(QtCore.QRect(840, 250, 161, 221))
		self.groupBoxTranspose.setObjectName(_fromUtf8("groupBoxTranspose"))
		self.layoutWidget = QtGui.QWidget(self.groupBoxTranspose)
		self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 71, 181))
		self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
		self.verticalLayout_8 = QtGui.QVBoxLayout(self.layoutWidget)
		self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
		
		self.sbTransOct1 = QtGui.QSpinBox(self.layoutWidget)
		self.sbTransOct1.setObjectName(_fromUtf8("sbTransOct1"))		
		self.sbTransOct1.setMinimum(-96)
		self.sbTransOct1.setMaximum(96)
		
		self.verticalLayout_8.addWidget(self.sbTransOct1)
		self.sbTransOct2 = QtGui.QSpinBox(self.layoutWidget)
		self.sbTransOct2.setObjectName(_fromUtf8("sbTransOct2"))
		self.sbTransOct2.setMinimum(-96)
		self.sbTransOct2.setMaximum(96)
		
		self.verticalLayout_8.addWidget(self.sbTransOct2)
		self.sbTransOct3 = QtGui.QSpinBox(self.layoutWidget)
		self.sbTransOct3.setObjectName(_fromUtf8("sbTransOct3"))
		self.sbTransOct3.setMinimum(-96)
		self.sbTransOct3.setMaximum(96)
		
		self.verticalLayout_8.addWidget(self.sbTransOct3)
		self.sbTransOct4 = QtGui.QSpinBox(self.layoutWidget)
		self.sbTransOct4.setObjectName(_fromUtf8("sbTransOct4"))
		self.sbTransOct4.setMinimum(-96)
		self.sbTransOct4.setMaximum(96)
		
		self.verticalLayout_8.addWidget(self.sbTransOct4)
		self.sbTransOct5 = QtGui.QSpinBox(self.layoutWidget)
		self.sbTransOct5.setObjectName(_fromUtf8("sbTransOct5"))
		self.sbTransOct5.setMinimum(-96)
		self.sbTransOct5.setMaximum(96)
		
		self.verticalLayout_8.addWidget(self.sbTransOct5)
		self.sbTransOct6 = QtGui.QSpinBox(self.layoutWidget)
		self.sbTransOct6.setObjectName(_fromUtf8("sbTransOct6"))
		self.sbTransOct6.setMinimum(-96)
		self.sbTransOct6.setMaximum(96)
		
		self.verticalLayout_8.addWidget(self.sbTransOct6)
		self.sbTransOct7 = QtGui.QSpinBox(self.layoutWidget)
		self.sbTransOct7.setObjectName(_fromUtf8("sbTransOct7"))
		self.sbTransOct7.setMinimum(-96)
		self.sbTransOct7.setMaximum(96)
		
		self.verticalLayout_8.addWidget(self.sbTransOct7)
		self.sbTransOct8 = QtGui.QSpinBox(self.layoutWidget)
		self.sbTransOct8.setObjectName(_fromUtf8("sbTransOct8"))
		self.sbTransOct8.setMinimum(-96)
		self.sbTransOct8.setMaximum(96)
		
		self.verticalLayout_8.addWidget(self.sbTransOct8)
		self.chkTranspose = QtGui.QCheckBox(self.groupBoxTranspose)
		self.chkTranspose.setGeometry(QtCore.QRect(40, 200, 70, 17))
		self.chkTranspose.setObjectName(_fromUtf8("chkTranspose"))
		self.widget4 = QtGui.QWidget(self.groupBoxTranspose)
		self.widget4.setGeometry(QtCore.QRect(10, 20, 42, 180))
		self.widget4.setObjectName(_fromUtf8("widget4"))
		self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget4)
		self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
		self.chkTranspose1 = QtGui.QCheckBox(self.widget4)
		self.chkTranspose1.setObjectName(_fromUtf8("chkTranspose1"))
		self.verticalLayout_3.addWidget(self.chkTranspose1)
		self.chkTranspose2 = QtGui.QCheckBox(self.widget4)
		self.chkTranspose2.setObjectName(_fromUtf8("chkTranspose2"))
		self.verticalLayout_3.addWidget(self.chkTranspose2)
		self.chkTranspose3 = QtGui.QCheckBox(self.widget4)
		self.chkTranspose3.setObjectName(_fromUtf8("chkTranspose3"))
		self.verticalLayout_3.addWidget(self.chkTranspose3)
		self.chkTranspose4 = QtGui.QCheckBox(self.widget4)
		self.chkTranspose4.setObjectName(_fromUtf8("chkTranspose4"))
		self.verticalLayout_3.addWidget(self.chkTranspose4)
		self.chkTranspose5 = QtGui.QCheckBox(self.widget4)
		self.chkTranspose5.setObjectName(_fromUtf8("chkTranspose5"))
		self.verticalLayout_3.addWidget(self.chkTranspose5)
		self.chkTranspose6 = QtGui.QCheckBox(self.widget4)
		self.chkTranspose6.setObjectName(_fromUtf8("chkTranspose6"))
		self.verticalLayout_3.addWidget(self.chkTranspose6)
		self.chkTranspose7 = QtGui.QCheckBox(self.widget4)
		self.chkTranspose7.setObjectName(_fromUtf8("chkTranspose7"))
		self.verticalLayout_3.addWidget(self.chkTranspose7)
		self.chkTranspose8 = QtGui.QCheckBox(self.widget4)
		self.chkTranspose8.setObjectName(_fromUtf8("chkTranspose8"))
		self.verticalLayout_3.addWidget(self.chkTranspose8)
		self.widget5 = QtGui.QWidget(self.groupBoxTranspose)
		self.widget5.setGeometry(QtCore.QRect(90, 20, 71, 181))
		self.widget5.setObjectName(_fromUtf8("widget5"))
		self.verticalLayout_5 = QtGui.QVBoxLayout(self.widget5)
		self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
		self.sbTransRep1 = QtGui.QSpinBox(self.widget5)
		self.sbTransRep1.setObjectName(_fromUtf8("sbTransRep1"))
		
		self.verticalLayout_5.addWidget(self.sbTransRep1)
		self.sbTransRep2 = QtGui.QSpinBox(self.widget5)
		self.sbTransRep2.setObjectName(_fromUtf8("sbTransRep2"))
		self.verticalLayout_5.addWidget(self.sbTransRep2)
		self.sbTransRep3 = QtGui.QSpinBox(self.widget5)
		self.sbTransRep3.setObjectName(_fromUtf8("sbTransRep3"))
		self.verticalLayout_5.addWidget(self.sbTransRep3)
		self.sbTransRep4 = QtGui.QSpinBox(self.widget5)
		self.sbTransRep4.setObjectName(_fromUtf8("sbTransRep4"))
		self.verticalLayout_5.addWidget(self.sbTransRep4)
		self.sbTransRep5 = QtGui.QSpinBox(self.widget5)
		self.sbTransRep5.setObjectName(_fromUtf8("sbTransRep5"))
		self.verticalLayout_5.addWidget(self.sbTransRep5)
		self.sbTransRep6 = QtGui.QSpinBox(self.widget5)
		self.sbTransRep6.setObjectName(_fromUtf8("sbTransRep6"))
		self.verticalLayout_5.addWidget(self.sbTransRep6)
		self.sbTransRep7 = QtGui.QSpinBox(self.widget5)
		self.sbTransRep7.setObjectName(_fromUtf8("sbTransRep7"))
		self.verticalLayout_5.addWidget(self.sbTransRep7)
		self.sbTransRep8 = QtGui.QSpinBox(self.widget5)
		self.sbTransRep8.setObjectName(_fromUtf8("sbTransRep8"))
		self.verticalLayout_5.addWidget(self.sbTransRep8)
		
		
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1005, 21))
		self.menubar.setObjectName(_fromUtf8("menubar"))
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName(_fromUtf8("menuFile"))
		self.menuEdit = QtGui.QMenu(self.menubar)
		self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
		self.menuSequencer = QtGui.QMenu(self.menubar)
		self.menuSequencer.setObjectName(_fromUtf8("menuSequencer"))
		self.menuMotion = QtGui.QMenu(self.menubar)
		self.menuMotion.setObjectName(_fromUtf8("menuMotion"))
		
		MainWindow.setMenuBar(self.menubar)
		
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)

		self.actionSave_MIDI = QtGui.QAction(MainWindow)
		self.actionSave_MIDI.setObjectName(_fromUtf8("actionSave_MIDI"))
		self.actionSave_Sequencer = QtGui.QAction(MainWindow)
		self.actionSave_Sequencer.setObjectName(_fromUtf8("actionSave_Sequencer"))
		self.actionSave_Patterns = QtGui.QAction(MainWindow)
		self.actionSave_Patterns.setObjectName(_fromUtf8("actionSave_Patterns"))
		self.actionSave_Tracker = QtGui.QAction(MainWindow)
		self.actionSave_Tracker.setObjectName(_fromUtf8("actionSave_Tracker"))
		self.actionLoad_Sequencer = QtGui.QAction(MainWindow)
		self.actionLoad_Sequencer.setObjectName(_fromUtf8("actionLoad_Sequencer"))
		self.actionLoad_Patterns = QtGui.QAction(MainWindow)
		self.actionLoad_Patterns.setObjectName(_fromUtf8("actionLoad_Patterns"))
		self.actionLoad_Tracker = QtGui.QAction(MainWindow)
		self.actionLoad_Tracker.setObjectName(_fromUtf8("actionLoad_Tracker"))
		self.actionExit = QtGui.QAction(MainWindow)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionCut = QtGui.QAction(MainWindow)
		self.actionCut.setObjectName(_fromUtf8("actionCut"))
		self.actionPaste = QtGui.QAction(MainWindow)
		self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
		
		self.actionOptions = QtGui.QAction(MainWindow)
		self.actionOptions.setObjectName(_fromUtf8("actionOptions"))
		self.actionOptions.triggered.connect(self.Options)
		
		self.actionSync = QtGui.QAction(MainWindow)
		self.actionSync.setObjectName(_fromUtf8("actionSync"))
		self.actionSync.triggered.connect(self.SyncDlg)
		
		self.actionRansomize = QtGui.QAction(MainWindow)
		self.actionRansomize.setObjectName(_fromUtf8("actionRansomize"))
		self.actionRansomize.triggered.connect(self.Randomize)
		self.actionRandomize_PPQ = QtGui.QAction(MainWindow)
		self.actionRandomize_PPQ.setObjectName(_fromUtf8("actionRandomize_PPQ"))
		self.actionRandomize_PPQ.triggered.connect(self.RandomizePPQ)
		
		self.actionRandomize_Rests = QtGui.QAction(MainWindow)
		self.actionRandomize_Rests.setObjectName(_fromUtf8("actionRandomize_Rests"))
		self.actionRandomize_Rests.triggered.connect(self.RandomizeRests)
		
		self.actionRandomize_Repeats = QtGui.QAction(MainWindow)
		self.actionRandomize_Repeats.setObjectName(_fromUtf8("actionRandomize_Repeats"))
		self.actionRandomize_Repeats.triggered.connect(self.RandomizeRepeats)
		
		self.actionPrev_Step = QtGui.QAction(MainWindow)
		self.actionPrev_Step.setObjectName(_fromUtf8("actionPrev_Step"))
		self.actionPrev_Step.triggered.connect(self.PrevStep)
		
		self.actionNext_Step = QtGui.QAction(MainWindow)
		self.actionNext_Step.setObjectName(_fromUtf8("actionNext_Step"))
		self.actionNext_Step.triggered.connect(self.NextStep)
		
		self.actionTranspose = QtGui.QAction(MainWindow)
		self.actionTranspose.setObjectName(_fromUtf8("actionTranspose"))
		self.actionTranspose.triggered.connect(self.TransposeDlg)
		
		self.actionHalf = QtGui.QAction(MainWindow)
		self.actionHalf.setObjectName(_fromUtf8("actionHalf"))
		self.actionHalf.triggered.connect(self.HalfNotes)
		
		self.actionQuarter = QtGui.QAction(MainWindow)
		self.actionQuarter.setObjectName(_fromUtf8("actionQuarter"))
		self.actionQuarter.triggered.connect(self.QuarterNotes)
		
		self.actionEigth = QtGui.QAction(MainWindow)
		self.actionEigth.setObjectName(_fromUtf8("actionEigth"))
		self.actionEigth.triggered.connect(self.EigthNotes)
		
		self.actionSixteenth = QtGui.QAction(MainWindow)
		self.actionSixteenth.setObjectName(_fromUtf8("actionSixteenth"))
		self.actionSixteenth.triggered.connect(self.SixteenthNotes)
		
		self.actionThirty_Second = QtGui.QAction(MainWindow)
		self.actionThirty_Second.setObjectName(_fromUtf8("actionThirty_Second"))
		self.actionEight_Triplets = QtGui.QAction(MainWindow)
		self.actionEight_Triplets.setObjectName(_fromUtf8("actionEight_Triplets"))
		self.actionQuarter_Triplets = QtGui.QAction(MainWindow)
		self.actionQuarter_Triplets.setObjectName(_fromUtf8("actionQuarter_Triplets"))
		
		self.actionShift_Left = QtGui.QAction(MainWindow)
		self.actionShift_Left.setObjectName(_fromUtf8("actionShift_Left"))
		self.actionShift_Left.triggered.connect(self.ShiftLeft)
		
		self.actionShift_Right = QtGui.QAction(MainWindow)
		self.actionShift_Right.setObjectName(_fromUtf8("actionShift_Right"))
		self.actionShift_Right.triggered.connect(self.ShiftRight)
		
		self.actionGenerateVariations = QtGui.QAction(MainWindow)
		self.actionGenerateVariations.setObjectName(_fromUtf8("actionGenerateVariations"))
		self.actionGenerateVariations.triggered.connect(self.GenerateVariations)
		
		self.actionAdd = QtGui.QAction(MainWindow)
		self.actionAdd.setObjectName(_fromUtf8("actionAdd"))
		self.actionRemove = QtGui.QAction(MainWindow)
		self.actionRemove.setObjectName(_fromUtf8("actionRemove"))
		self.actionNext = QtGui.QAction(MainWindow)
		self.actionNext.setObjectName(_fromUtf8("actionNext"))
		self.actionPrev = QtGui.QAction(MainWindow)
		self.actionPrev.setObjectName(_fromUtf8("actionPrev"))
		self.actionAdd_Pattern = QtGui.QAction(MainWindow)
		self.actionAdd_Pattern.setObjectName(_fromUtf8("actionAdd_Pattern"))
		self.actionChain_Pattern = QtGui.QAction(MainWindow)
		self.actionChain_Pattern.setObjectName(_fromUtf8("actionChain_Pattern"))
		self.actionTracker_On = QtGui.QAction(MainWindow)
		self.actionTracker_On.setCheckable(True)
		self.actionTracker_On.setObjectName(_fromUtf8("actionTracker_On"))
		self.actionSequencer_On = QtGui.QAction(MainWindow)
		self.actionSequencer_On.setCheckable(True)
		self.actionSequencer_On.setChecked(True)
		self.actionSequencer_On.setObjectName(_fromUtf8("actionSequencer_On"))
		self.actionStart_Stop_Sync = QtGui.QAction(MainWindow)
		self.actionStart_Stop_Sync.setCheckable(True)
		self.actionStart_Stop_Sync.setObjectName(_fromUtf8("actionStart_Stop_Sync"))
		
		self.actionClear = QtGui.QAction(MainWindow)
		self.actionClear.setObjectName(_fromUtf8("actionClear"))
		self.actionClear.triggered.connect(self.MotionClear)
		
		self.actionRecord = QtGui.QAction(MainWindow)
		self.actionRecord.setCheckable(True)
		self.actionRecord.setObjectName(_fromUtf8("actionRecord"))
		self.actionRecord.triggered.connect(self.MotionRecord)

		self.menuFile.addAction(self.actionSave_MIDI)
		self.menuFile.addAction(self.actionSave_Sequencer)
		self.menuFile.addAction(self.actionSave_Patterns)
		self.menuFile.addAction(self.actionSave_Tracker)
		self.menuFile.addAction(self.actionLoad_Sequencer)
		self.menuFile.addAction(self.actionLoad_Patterns)
		self.menuFile.addAction(self.actionLoad_Tracker)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionExit)
		self.menuEdit.addAction(self.actionCut)
		self.menuEdit.addAction(self.actionPaste)
		self.menuEdit.addSeparator()
		self.menuEdit.addAction(self.actionOptions)
		self.menuEdit.addAction(self.actionSync)
		self.menuSequencer.addAction(self.actionRansomize)
		self.menuSequencer.addAction(self.actionRandomize_PPQ)
		self.menuSequencer.addAction(self.actionRandomize_Rests)
		self.menuSequencer.addAction(self.actionRandomize_Repeats)
		self.menuSequencer.addSeparator()
		self.menuSequencer.addAction(self.actionPrev_Step)
		self.menuSequencer.addAction(self.actionNext_Step)
		self.menuSequencer.addSeparator()
		self.menuSequencer.addAction(self.actionTranspose)
		self.menuSequencer.addAction(self.actionShift_Left)
		self.menuSequencer.addAction(self.actionShift_Right)
		self.menuSequencer.addSeparator()
		self.menuSequencer.addAction(self.actionHalf)
		self.menuSequencer.addAction(self.actionQuarter)
		self.menuSequencer.addAction(self.actionEigth)
		self.menuSequencer.addAction(self.actionSixteenth)
		self.menuSequencer.addAction(self.actionThirty_Second)
		self.menuSequencer.addAction(self.actionEight_Triplets)
		self.menuSequencer.addAction(self.actionQuarter_Triplets)
		self.menuSequencer.addSeparator()
		self.menuSequencer.addAction(self.actionSequencer_On)
		self.menuSequencer.addAction(self.actionGenerateVariations)
		self.menuMotion.addAction(self.actionClear)
		self.menuMotion.addAction(self.actionRecord)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuEdit.menuAction())
		self.menubar.addAction(self.menuSequencer.menuAction())
		self.menubar.addAction(self.menuMotion.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
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
		self.label.setText(_translate("MainWindow", "MIDI Port", None))
		self.label_2.setText(_translate("MainWindow", "Channel", None))
		self.label_3.setText(_translate("MainWindow", "Sequencer", None))
		self.label_4.setText(_translate("MainWindow", "Row x16", None))
		self.label_5.setText(_translate("MainWindow", "Steps", None))
		self.pbStart.setText(_translate("MainWindow", "Panic", None))
		self.label_6.setText(_translate("MainWindow", "Voice", None))
		self.labelBanks.setText(_translate("MainWindow", "Banks", None))
		self.labelVoices.setText(_translate("MainWindow", "Voices", None))
		self.groupBox.setTitle(_translate("MainWindow", "Pattern Variation", None))
		self.rbA.setText(_translate("MainWindow", "A", None))
		self.rbB.setText(_translate("MainWindow", "B", None))
		self.rbC.setText(_translate("MainWindow", "C", None))
		self.rbD.setText(_translate("MainWindow", "D", None))
		self.rbE.setText(_translate("MainWindow", "E", None))
		self.rbF.setText(_translate("MainWindow", "F", None))
		self.rbG.setText(_translate("MainWindow", "G", None))
		self.rbH.setText(_translate("MainWindow", "H", None))
		self.groupBox_2.setTitle(_translate("MainWindow", "Motion 1", None))
		

		self.menuFile.setTitle(_translate("MainWindow", "File", None))
		self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
		self.menuSequencer.setTitle(_translate("MainWindow", "Sequencer", None))
		self.menuMotion.setTitle(_translate("MainWindow", "Motion", None))
		self.actionSave_MIDI.setText(_translate("MainWindow", "Save MIDI", None))
		self.actionSave_Sequencer.setText(_translate("MainWindow", "Save Sequencer", None))
		self.actionSave_Patterns.setText(_translate("MainWindow", "Save Patterns", None))
		self.actionSave_Tracker.setText(_translate("MainWindow", "Save Tracker", None))
		self.actionLoad_Sequencer.setText(_translate("MainWindow", "Load Sequencer", None))
		self.actionLoad_Patterns.setText(_translate("MainWindow", "Load Patterns", None))
		self.actionLoad_Tracker.setText(_translate("MainWindow", "Load Tracker", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionCut.setText(_translate("MainWindow", "Cut", None))
		self.actionPaste.setText(_translate("MainWindow", "Paste", None))
		self.actionOptions.setText(_translate("MainWindow", "Options", None))
		self.actionSync.setText(_translate("MainWindow", "Sync", None))
		self.actionRansomize.setText(_translate("MainWindow", "Randomize", None))
		self.actionRandomize_PPQ.setText(_translate("MainWindow", "Randomize PPQ", None))
		self.actionRandomize_Rests.setText(_translate("MainWindow", "Randomize Rests", None))
		self.actionRandomize_Repeats.setText(_translate("MainWindow", "Randomize Repeats", None))
		self.actionPrev_Step.setText(_translate("MainWindow", "Prev Step", None))
		self.actionNext_Step.setText(_translate("MainWindow", "Next Step", None))
		self.actionTranspose.setText(_translate("MainWindow", "Transpose", None))
		self.actionHalf.setText(_translate("MainWindow", "Half", None))
		self.actionQuarter.setText(_translate("MainWindow", "Quarter", None))
		self.actionEigth.setText(_translate("MainWindow", "Eigth", None))
		self.actionSixteenth.setText(_translate("MainWindow", "Sixteenth", None))
		self.actionThirty_Second.setText(_translate("MainWindow", "Thirty Second", None))
		self.actionEight_Triplets.setText(_translate("MainWindow", "Eight Triplets", None))
		self.actionQuarter_Triplets.setText(_translate("MainWindow", "Quarter Triplets", None))
		self.actionShift_Left.setText(_translate("MainWindow", "Shift Left", None))
		self.actionShift_Right.setText(_translate("MainWindow", "Shift Right", None))
		self.actionAdd.setText(_translate("MainWindow", "Add", None))
		self.actionRemove.setText(_translate("MainWindow", "Remove", None))
		self.actionNext.setText(_translate("MainWindow", "Next", None))
		self.actionPrev.setText(_translate("MainWindow", "Prev", None))
		self.actionAdd_Pattern.setText(_translate("MainWindow", "Add Pattern", None))
		self.actionChain_Pattern.setText(_translate("MainWindow", "Chain Pattern", None))
		self.actionTracker_On.setText(_translate("MainWindow", "Tracker On", None))
		self.actionSequencer_On.setText(_translate("MainWindow", "Sequencer On", None))
		self.actionStart_Stop_Sync.setText(_translate("MainWindow", "Start/Stop Sync", None))
		self.actionClear.setText(_translate("MainWindow", "Clear", None))
		self.actionRecord.setText(_translate("MainWindow", "Record", None))
		self.actionGenerateVariations.setText(_translate("MainWindow", "Generate Variations", None))


		self.groupBoxMatrix.setTitle(_translate("MainWindow", "Matrix", None))
		self.chkMatrix.setText(_translate("MainWindow", "On", None))
		self.rbMatrix1.setText(_translate("MainWindow", "1", None))
		self.rbMatrix2.setText(_translate("MainWindow", "2", None))
		self.rbMatrix3.setText(_translate("MainWindow", "3", None))
		self.rbMatrix4.setText(_translate("MainWindow", "4", None))
		self.rbMatrix5.setText(_translate("MainWindow", "5", None))
		self.rbMatrix6.setText(_translate("MainWindow", "6", None))
		self.rbMatrix7.setText(_translate("MainWindow", "7", None))
		self.rbMatrix8.setText(_translate("MainWindow", "8", None))
		self.groupBoxShiftCore.setTitle(_translate("MainWindow", "Shift Core", None))
		self.chkShiftCore.setText(_translate("MainWindow", "On/Off", None))
		self.groupBox_3.setTitle(_translate("MainWindow", "Direction", None))
		self.rbLeft.setText(_translate("MainWindow", "Left", None))
		self.rbRight.setText(_translate("MainWindow", "Right", None))
		self.rbRandom.setText(_translate("MainWindow", "Random", None))
		self.rbShift1.setText(_translate("MainWindow", "1", None))
		self.rbShift2.setText(_translate("MainWindow", "2", None))
		self.rbShiftR.setText(_translate("MainWindow", "R", None))
		self.rbShift3.setText(_translate("MainWindow", "3", None))
		self.rbShift5.setText(_translate("MainWindow", "5", None))
		self.rbShift8.setText(_translate("MainWindow", "8", None))
		self.rbShift13.setText(_translate("MainWindow", "13", None))
		self.rbShift21.setText(_translate("MainWindow", "21", None))
		self.rbShift34.setText(_translate("MainWindow", "34", None))
		self.rbShift55.setText(_translate("MainWindow", "55", None))
		self.groupBoxTranspose.setTitle(_translate("MainWindow", "Transpose Matrix", None))
		self.chkTranspose.setText(_translate("MainWindow", "On/Off", None))
		self.chkTranspose1.setText(_translate("MainWindow", "1", None))
		self.chkTranspose2.setText(_translate("MainWindow", "2", None))
		self.chkTranspose3.setText(_translate("MainWindow", "3", None))
		self.chkTranspose4.setText(_translate("MainWindow", "4", None))
		self.chkTranspose5.setText(_translate("MainWindow", "5", None))
		self.chkTranspose6.setText(_translate("MainWindow", "6", None))
		self.chkTranspose7.setText(_translate("MainWindow", "7", None))
		self.chkTranspose8.setText(_translate("MainWindow", "8", None))




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
	