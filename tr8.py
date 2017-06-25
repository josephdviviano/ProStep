from random import *

trp1 =[1,0,0,0]
trp2 =[1,1,0,0]
trp3 =[1,0,1,0]
trp4 = [1,0,0,1]
trp5 = [1,1,1,0]
trp6 = [1,0,1,1]

drum_patterns = [trp1,trp2,trp3,trp4,trp5,trp6]

def TR8_ToHex(p):
	n = 0
	for i in range(len(p)):
		x = p[i] * 2**i
		n = n + x
	return n
	
def TR8_PickPattern():
	n = randint(0,5)
	return TR8_ToHex(drum_patterns[n])
	
def TR8_GenPattern():
	pattern1 = TR8_PickPattern()
	pattern2 = TR8_PickPattern()
	pattern3 = TR8_PickPattern()
	pattern4 = TR8_PickPattern()
	out = pattern1 << 12 | pattern2 << 8| pattern3 << 4 | pattern4
	return out
	

TR8_PAT = 'TR8_PTN'


	
def WritePatterns():	
	for i in range(16):
		f = open( TR8_PAT + str(i) + '.PRM','w+')

		bd1 = TR8_GenPattern()
		bd2 = TR8_GenPattern()
		sd1 =TR8_GenPattern()
		sd2 =TR8_GenPattern()
		lt1 = TR8_GenPattern()
		lt2 = TR8_GenPattern()
		mt1 = TR8_GenPattern()
		mt2 = TR8_GenPattern()
		ht1 = TR8_GenPattern()
		ht2 = TR8_GenPattern()
		rs1 = TR8_GenPattern()
		rs2 = TR8_GenPattern()
		hc1 = TR8_GenPattern()
		hc2 = TR8_GenPattern()
		ch1 = TR8_GenPattern()
		ch2 = TR8_GenPattern()
		oh1 = TR8_GenPattern()
		oh2 = TR8_GenPattern()
		cc1 = TR8_GenPattern()
		cc2 = TR8_GenPattern()
		rc1 = TR8_GenPattern()
		rc2 = TR8_GenPattern()
		acc1 = TR8_GenPattern()
		acc2 = TR8_GenPattern()
		rev1 = TR8_GenPattern()
		rev2 = TR8_GenPattern()
		dly1 = TR8_GenPattern()
		dly2 = TR8_GenPattern()
		
		f.write('VARI(0);\n')
		f.write('SCALE(2);\n')
		f.write('LAST_A(15);\n')
		f.write('LAST_B(15);\n')
		f.write('STEP_ACC1('+str(acc1)+');\n')
		f.write('STEP_ACC2('+str(acc2)+');\n')
		f.write('STEP_REV1('+str(rev1)+');\n')
		f.write('STEP_REV2('+str(rev2)+');\n')
		f.write('STEP_ECHO1('+str(dly1)+');\n')
		f.write('STEP_ECHO2('+str(dly2)+');\n')
		f.write('STEP_BD1('+str(bd1)+');\n')
		f.write('STEP_BD2('+str(bd2)+');\n')
		f.write('STEP_SD1('+str(sd1)+');\n')
		f.write('STEP_SD2('+str(sd2)+');\n')
		f.write('STEP_LT1('+str(lt1)+');\n')
		f.write('STEP_LT2('+str(lt2)+');\n')
		f.write('STEP_MT1('+str(mt1)+');\n')
		f.write('STEP_MT2('+str(mt2)+');\n')
		f.write('STEP_HT1('+str(mt1)+');\n')
		f.write('STEP_HT2('+str(mt2)+');\n')
		f.write('STEP_CH1('+str(ch1)+');\n')
		f.write('STEP_CH2('+str(ch2)+');\n')
		f.write('STEP_OH1('+str(oh1)+');\n')
		f.write('STEP_OH2('+str(oh2)+');\n')
		f.write('STEP_CC1('+str(cc1)+');\n')
		f.write('STEP_CC2('+str(cc2)+');\n')
		f.write('STEP_RC1('+str(rc1)+');\n')
		f.write('STEP_RC2('+str(rc2)+');\n')
		f.write('ACC_BD1(0);\n')
		f.write('ACC_BD2(0);\n')
		f.write('ACC_SD1(0);\n')
		f.write('ACC_SD2(0);\n')
		f.write('ACC_LT1(0);\n')
		f.write('ACC_LT2(0);\n')
		f.write('ACC_MT1(0);\n')
		f.write('ACC_MT2(0);\n')
		f.write('ACC_HT1(0);\n')
		f.write('ACC_HT2(0);\n')
		f.write('ACC_RS1(0);\n')
		f.write('ACC_RS2(0);\n')
		f.write('ACC_HC1(0);\n')
		f.write('ACC_HC2(0);\n')
		f.write('ACC_CH1(0);\n')
		f.write('ACC_CH2(0);\n')
		f.write('ACC_OH1(0);\n')
		f.write('ACC_OH2(0);\n')
		f.write('ACC_CC1(0);\n')
		f.write('ACC_CC2(0);\n')
		f.write('ACC_RC1(0);\n')
		f.write('ACC_RC2(0);\n')
		f.write('WEAK_ACC1(0);\n')
		f.write('WEAK_ACC2(0);\n')
		f.write('FLAM_BD1(0);\n')
		f.write('FLAM_BD2(0);\nFLAM_SD1(0);\nFLAM_SD2(0);\nFLAM_LT1(0);\nFLAM_LT2(0);\nFLAM_MT1(0);\n')
		f.write('FLAM_MT2(0);\nFLAM_HT1(0);\nFLAM_HT2(0);\nFLAM_RS1(0);\nFLAM_RS2(0);\n')
		f.write('FLAM_HC1(0);\nFLAM_HC2(0);\nFLAM_CH1(0);\nFLAM_CH2(0);\nFLAM_OH1(0);\n')
		f.write('FLAM_OH2(0);\nFLAM_CC1(0);\nFLAM_CC2(0);\nFLAM_RC1(0);\nFLAM_RC2(0);\n')

		f.close()
		
WritePatterns()
		
