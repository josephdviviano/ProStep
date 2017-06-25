import os,time

os.spawnl(os.P_NOWAIT,"c:/python27/python.exe","python.exe","virtualport.py")

time.sleep(5)

print os.spawnl(os.P_NOWAIT,"c:/python27/python.exe","python.exe","seq16.py")
os.spawnl(os.P_WAIT,"c:/python27/python.exe","python.exe","mophoseq4.py")