
from patterns import *
import os

pat = "TB3_PTN"
PROB_PATTERN=0.15
PROB1 = 0.195
PROB2 = 0.175
PROB3 = 0.1275
PROB_CLEAR = 0.05
PROB_SLIDE = 0.15
PROB_ACCENT = 0.3625
PROB_OCT3 = 0.2
PROB_OCT4 = 0.1
PROB_OCT5 = 0.05
PROB_NOTE = 0.1

trp1 =[1,0,0,0]
trp2 =[1,1,0,0]
trp3 =[1,0,1,0]
trp4 = [1,0,0,1]
trp5 = [1,1,1,0]
trp6 = [1,0,1,1]
trp7 = [1,1,1,1]

patterns = [trp1,trp2,trp3,trp7,trp4,trp5,trp6]

p1 = [0,1,0,0]
p2 = [0,1,1,0]
p3 = [0,1,0,1]
p4 = [0,1,1,1]
p5 = [0,0,1,0]
p6 = [0,0,1,1]
p7 = [0,0,0,1]

offp = [p1,p2,p3,p4,p5,p6,p7]

PROB_PAT1 = 0.8
PROB_PAT2 = 0.7
PROB_PAT3 = 0.6
PROB_PAT4 = 0.4
PROB_PAT3 = 0.5
PROB_PAT2 = 0.5
PROB_PAT1 = 0.1


	
def TB3_OffPattern():
	return choice(offp)
	
def TB3_ProbPattern():
	x = random()
	if(x < PROB_PAT1):  return trp7
	elif(x < PROB_PAT2):  return trp6
	elif(x < PROB_PAT3): return trp5
	elif(x < PROB_PAT3): return trp4
	elif(x < PROB_PAT3): return trp3
	elif(x < PROB_PAT3): return trp2
	elif(x < PROB_PAT3): return trp1
	return trp7
	
	
def TB3_PickPattern():
	return choice(patterns)
	
def TB3_GenPattern():
	pattern1 = TB3_PickPattern()
	pattern2 = TB3_PickPattern()
	pattern3 = TB3_PickPattern()
	pattern4 = TB3_PickPattern()
	return pattern1 + pattern2 + pattern3 + pattern4
	
def TB3_GenOffPattern():
	pattern1 = TB3_OffPattern()
	pattern2 = TB3_OffPattern()
	pattern3 = TB3_OffPattern()
	pattern4 = TB3_OffPattern()
	return pattern1 + pattern2 + pattern3 + pattern4



ud1 = [0,0,0,0]
ud2 = [0,1,0,0]
ud3 = [0,0,1,0]
ud4 = [0,0,0,1]
ud5 = [1,0,0,0]
ud6 = [1,1,0,0]
ud7 = [1,0,1,0]
ud8 = [1,0,0,1]
ud9 = [1,1,1,0]
ud10 = [1,0,1,1]
ud11 = [1,1,0,1]
ud12 = [0,1,0,1]
ud13 = [0,1,1,0]
ud14 = [0,1,1,1]
ud15 = [0,0,1,1]
ud16 = [1,1,1,1]
ud = [ud1,ud2,ud3,ud4,ud5,ud6,ud7,ud8,ud9,ud10,ud11,ud12,ud13,ud14,ud15,ud16]

def UD1():
	x = choice(ud) 
	y = choice(ud) 
	z = x+x+x+x+y+y+y+y
	out = []
	for n in z:
		if(n == 1):
			if(random() > 0.5):
				n = -1
		out.append(n)
		
	return out
	

def UD2(c,s):
	n=0
	if(s == 0):
		if(c == 0): n = 0
		elif(c == 1): n = 0
		elif(c == 2): n = 0
	elif(s==1):
		if(c == 0): n = 0
		elif(c == 1): n = 1
		elif(c == 2): n = 0
	elif(s == 2):
		if(c == 0): n = 0
		elif(c == 1): n = 0
		elif(c == 2): n = 1
	elif(s == 3):
		if(c == 0): n = 0
		elif(c == 1): n = 1
		elif(c == 2): n = 1
	elif(s == 4):
		if(c == 0): n = 1
		elif(c == 1): n = 0
		elif(c == 2): n = 0
	elif(s == 5):
		if(c == 0): n = 1
		elif(c == 1): n = 0
		elif(c == 2): n = 1
	elif(s == 6):
		if(c == 0): n = 1
		elif(c == 1): n = 1
		elif(c == 2): n = 0
	elif(s == 7):
		if(c == 0): n = 1
		elif(c == 1): n = 1
		elif(c == 2): n = 1
	elif(s == 8):
		if(c == 0): n = -1
		elif(c == 1): n = 0
		elif(c == 2): n = 0
	elif(s == 9):
		if(c == 0): n = -1
		elif(c == 1): n = -1
		elif(c == 2): n = 0
	elif(s == 10):
		if(c == 0): n = -1
		elif(c == 1): n = 0
		elif(c == 2): n = -1
	elif(s == 11):
		if(c == 0): n = -1
		elif(c == 1): n = -1
		elif(c == 2): n = -1
	elif(s == 12):
		if(c == 0): n = -1
		elif(c == 1): n = 0
		elif(c == 2): n = 1
	elif(s == 13):
		if(c == 0): n = -1
		elif(c == 1): n = 1
		elif(c == 2): n = 0
	elif(s == 14):
		if(c ==0): n = 1
		elif(c == 1): n = -1
		elif(c == 2): n = 0
	elif(s == 16):
		if(c == 0): n = 1
		elif(c == 1): n = 0
		elif(c == 2): n = -1
	
	return n
	
	
	
	
def UD3(c,s1,s2,s3,s4):
	
	note = 0
	if(c == 0):
		note = s1			
	elif(c == 1):
		note = s2
	elif(c == 2):
		note = s3
	elif(c == 3):
		note = s4
		
	return note
	
	
def WritePattern(filename,seq):
	scale,chord = MUSIC_PickScaleChord()
	f = open(filename,'w+')
	f.write('TRIPLET(0);\n')
	f.write('LAST_STEP(15);\n')
	f.write('GATE_WIDTH(67);\n')
	last = 36
	
	pslide = TB3_GenOffPattern()
	paccent = TB3_GenPattern()
	pclear = TB3_GenOffPattern()
	clear = 0
	slide=0
	
	c = 0
	sel = randint(0,16)
	s1  = randint(-1,1)
	s2 = randint(-1,1)
	s3 = randint(-1,1)
	s4 = randint(-1,1)
	uds = randint(0,2)
	ud = UD1()
	
	for i in range(1,len(seq)+1):
		
		note = seq[i-1]+48
		
		slide = 0
		#slide = pslide[(i-1) % len(pslide)]
		#if(slide == -1): slide = 0
		
		accent = paccent[(i-1) % len(paccent)]
		if(accent == -1): accent = 0
		
		clear = 0		
		#if(random() < PROB_CLEAR): clear = pclear[(i-1) % len(pclear)]
		#if(clear == -1): clear = 1
		
		if(note == -1):				
			note = choice(scale) + 36
			
				
		y = 0
		if(uds == 0):
			y = ud[i-1]			
		elif(uds == 1):
			y = UD2(c,sel)
		else:
			y = UD3(c,s1,s2,s3,s4)
			
		if(y == -1): note = note - 12
		elif(y == 1): note = note + 12
		c = c + 1
		c = c % 4
		
		last = note
		
		
		f.write('STEP'+str(i)+'('+str(note)+','+str(slide)+','+str(clear)+','+str(accent)+');\n')
		
		
	f.write('BANK(0);\nPATCH(-1);\n')
	f.close()
		

def TB3_Octave(c,shift=0):		
	if(c != -1):
		oct = 48
		c = oct + c + shift
	return c

def TB3_Octaves(seq,shift=0):
	scale,chord = MUSIC_PickScaleChord()
	o = []	
	shift = choice(scale)
	for i in range(len(seq)):
		c = TB3_Octave(seq[i],shift)		
		o.append(c)
	return o


if __name__ == '__main__':
	
	scale,chord = MUSIC_PickScaleChord()
	MUSIC_SetScaleChord(scale_phrygian_dom,chord_min)


	os.chdir('./tb3')	
	type = -1
	for i in range(8):
		type = 0
		for j in range(8):		
			filename = pat + str(i*8+j+1) + '.PRM'
			
			
			pattern1 = GEN_CreatePattern(type) 
			pattern2= GEN_CreatePattern(type) 
						
			pattern = pattern1 + pattern2
			
			#pattern = TB3_Octaves(pattern)
			WritePattern(filename,pattern[0:32])
		
		