
##imports
import os
import time
import output
import win32api
import sound
import subprocess
import configparser
from dirsync import sync
import threading
from threading import Thread
import winsound
import psutil
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#config parser initialisation
config = configparser.ConfigParser()
config.read("config.ini")
#pycaw initialisation
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vr = volume.GetVolumeRange()
#global values
folders=[]
capps=[]
beeped=False
donethings=False
def main():
#init stuff
	if __name__ == '__main__':
		if getopt('system monitor options','idle_closing',type='b')==True:
			idle=Thread(target=idleloop)
			if getopt('idle_options','mute_wen_idle',type='b')==True:
				kv=Thread(target=volloop)
				kv.start()
			idle.start()

		fsync=Thread(target=back_folders,args="s")
		volmon=Thread(target=vmon)
		fsync.start()
		volmon.start()
	if getopt('system monitor options','battery_announce',type='b')==True:
		bthread=Thread(target=batrloop)
		bthread.start()
def closeapps():
	capps=getapps()
	config.read("config.ini")
	for procloop in capps:
		subprocess.Popen("taskkill.exe /im "+getopt("clapp "+procloop,"file"),shell=True,stdout=None)
def back_folders(mode="s"):
	folders=getfolders()
	for foldloop in folders:
		foldera=getopt("folder "+foldloop,"source")
#		print(foldera)
		folderb=getopt("folder "+foldloop,"dest")
#		print(folderb)
		if mode=="s":
			sp=Thread(target=syncfolder,args=("s",foldera,folderb))
			sb.start
			while True:
				if not sp.is_alive():
					time.sleep(.5000)
					sp=Thread(target=syncfolder("s",foldera,folderb,))
					sp.start()
				else:
					continue
		elif mode=="u":
			syncfolder("u",foldera,folderb,)
def syncfolder(mode,folder1,folder2):
		if mode=="s":
			sync (folder1,folder2,"sync")
			os.system("clear")
		elif mode==("u"):
			sync (folder1,folder2,"update")
def getfolders():
	config.read("config.ini")
	folders = config.sections()
	folders = [f for f in folders if f.lower().startswith("folder ")]
	results = []
	for folder in folders:
		name = folder.split(None, 1)[1]
		results.append(name)
	return results
def getopt(sect,opt,type='s'):
	re=config.get(sect,opt,raw=True)
	if isinstance(re,list)==True:
		re=str(re[0])
		if type=='s':
			re=str(re[0])
		elif type=='i':
			re=int(re)
		elif type=='f':
			re=float(re)
		elif type=='b':
			if re.lower() in ['yes','y','on','true']:
				re=True
		else:
			re=False
	else:
		if type=='s':
			re=re
		elif type=='i':
			re=int(re)
		elif type=='f':
			re=float(re)
		elif type=='b':
			if re.lower() in ['yes','y','on','true']:
				re=True
		else:
			re=False
	return re
def idleloop():
#init stuff
	donethings=False
	s=sound.sound()
	s.load('s/warn.wav')
	afktime=getopt('idle_options','afk_time',type='i')
	warntime=getopt('idle_options','warn_time',type='i')
	while True:
		fidle=win32api.GetLastInputInfo()
		lastfidle=fidle
		time.sleep(afktime)
		fidle=win32api.GetLastInputInfo()
		if lastfidle==fidle and donethings==False:
			s.play_wait()
			time.sleep(warntime)
			if lastfidle==fidle:
				closeapps()
				donethings=True
				if getopt('idle_options','mute_wen_idle',type='b')==True:
					volume.SetMute(1,None)
		elif donethings==True:
			if not lastfidle==fidle:
				donethings=False
def getapps():
	config.read("config.ini")
	capps = config.sections()
	capps = [c for c in capps if c.lower().startswith("clapp ")]
	results = []
	for capp in capps:
		name = capp.split(None, 1)[1]
		results.append(name)
	return results
def toneplay():
	vtf=getopt('system monitor options','volume_tone_frequency',type='i')
	vtt=1000
	winsound.Beep(vtf,vtt)
def vmon():
	vs=sound.sound()
	if getopt('system monitor options','volume_sound_enabled',type='b')==True:
		vs.load("s/volume.wav")
	while True:
		vl =volume.GetMasterVolumeLevel()
		ovl=vl
		vl = volume.GetMasterVolumeLevel()
		if not ovl==vl:
			if getopt('system monitor options','volume_tone_enabled',type='b')==True:
				toneplay()
			if getopt('system monitor options','volume_sound_enabled',type='b')==True:
				vs.play()
		else:
			continue
def batrloop():
	while True:
		battery=psutil.sensors_battery()
		bat=battery[0]
		chargstat=battery[2]
		och=chargstat
		battery=psutil.sensors_battery()
		chargstat=battery[2]
		if not och==chargstat:
			if chargstat==True:
				output.speak("battery charging started",True)
				och=chargstat
				chargstat=battery[2]
				continue
			if chargstat==False:
				output.speak("battery charging stopped",True)
				och=chargstat
				chargstat=battery[2]
				continue
		else:
			continue
		battery=psutil.sensors_battery()
		bat=battery[0]
		obat=bat
		battery=psutil.sensors_battery()
		bat=battery[0]
		if not bat==obat:
			if bat==100 or bat==90 or bat ==80 or bat==70 or bat==60 or bat==50 or bat==40 or bat==30 or bat==20 or bat==10:
				output.speak(bat+"percent battery remaining",True)
def volloop():
	while True:
		fidle =win32api.GetLastInputInfo()
		time.sleep(0.3)
		lastfidle=fidle
		fidle =win32api.GetLastInputInfo()
		if not lastfidle==fidle and getopt('idle_options','mute_wen_idle',type='b')==True:
			volume.SetMute(0,None)
			continue
main()