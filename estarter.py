
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
import pyprowl
from watchpoints import watch
import sys
import pythoncom
import wmi
#config parser initialisation
config = configparser.ConfigParser()
config.read("config.ini")
#global values
folders=[]
capps=[]
donethings=False
es=sound.sound()
es.load('s/error.wav')
pr=""
#pycaw initialisation
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vr = volume.GetVolumeRange()
def main():
	#init stuff
	if __name__ == '__main__':
		if getopt('system monitor options','notify_prowl',type='b')==True:
			set_prowl_key()
		if getopt('system monitor options','idle_closing',type='b')==True or getopt('idle_options','mute_wen_idle',type='b')==True or getopt('system monitor options','notify_prowl',type='b')==True:
			idle=Thread(target=idleloop)
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
	if getopt('system monitor options','usb_monitor',type='b')==True:
		uthread=Thread(target=usbloop)
		uthread.start()

def closeapps():
	capps=getapps()
	config.read("config.ini")
	for procloop in capps:
		subprocess.Popen("taskkill.exe /im "+getopt("clapp "+procloop,"file"),shell=True,stdout=None)

def back_folders(mode="s"):
	folders=getfolders()
	for foldloop in folders:
		foldera=getopt("folder "+foldloop,"source")
		#print(foldera)
		folderb=getopt("folder "+foldloop,"dest")
		#print(folderb)
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
		elif re.lower() in ['no','n','off','false']:
			re=False
		else:
			print("error, expression\n",re,"is not of a proper bool value")
			es.play_wait()
			es.close()
			exit
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
		elif re.lower() in ['no','n','off','false']:
			re=False
		else:
			print("error, expression\n",re,"is not of a proper bool value")
			es.play_waite()
			es.close()
			exit
	return re

def idleloop():
	#init stuff
	global donethings
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
			fidle=win32api.GetLastInputInfo()
			if lastfidle==fidle:
				if getopt('system monitor options','idle_closing',type='b')==True:
					closeapps()
				donethings=True
				if getopt('idle_options','mute_wen_idle',type='b')==True:
					volume.SetMute(1,None)
		continue

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
	cs_sound=sound.sound()
	ss_sound=sound.sound()
	cs_sound.load("s/charge start.wav")
	ss_sound.load("s/charge stop.wav")
	battery=psutil.sensors_battery()
	chargstat=battery[2]
	bat=battery[0]
	#calback for watch
	def cstat(bla1,bla2,bla3):
		if chargstat==True:
			output.speak("battery charging started",True)
			cs_sound.play()
			if getopt('system monitor options','notify_prowl',type='b')==True:
				pnot('computer started charging','your computer is now charging')
		if chargstat==False:
			output.speak("battery charging stopped",True)
			ss_sound.play()
			if getopt('system monitor options','notify_prowl',type='b')==True:
				pnot('computer stopped charging','your computer is not charging any more')
	def bstat(bla1,bla2,bla3):
		if bat==100 or bat==90 or bat ==80 or bat==70 or bat==60 or bat==50 or bat==40 or bat==30 or bat==20 or bat==10:
			output.speak(str(bat)+"percent battery remaining",True)
	watch(chargstat,callback=cstat)
	watch(bat,callback=bstat)
	while True:
		battery=psutil.sensors_battery()
		bat=battery[0]
		chargstat=battery[2]
		continue

def volloop():
	global donethings
	while True:
		fidle =win32api.GetLastInputInfo()
		time.sleep(0.3)
		lastfidle=fidle
		fidle =win32api.GetLastInputInfo()
		if not lastfidle==fidle and donethings==True:
			donethings=False
			if getopt('idle_options','mute_wen_idle',type='b')==True:					volume.SetMute(0,None)
			if getopt('system monitor options','notify_prowl',type='b')==True:
				pnot('computer not idle','some one is interacting with your computer')
			continue

def set_prowl_key():
	#prowl initialisation
	global pr
	pr=pyprowl.Prowl(getopt('prowl options','key',type='s'))
	try:
		result =pr.verify_key()
		print ("Prowl API key successfully verified")
	except Exception as e:
		print (f"Error verifying Prowl API key:\n{e}")
		es.play_wait()
		es.close()
		exit()

def pnot(event: str,message: str):
	try:
		pr.notify(event,message,priority=getopt('prowl options','priority',type='i'),appName='estarter')
		print("notification sent to prowl")
	except Exception as  e:
		print ("Error sending notification to Prowl:",e)
		es.play()

def usbloop():
	pythoncom.CoInitialize()
	device_connected_wql="SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
	device_disconnected_wql="SELECT * FROM __InstanceDeletionEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
	c=wmi.WMI ()
	connected_watcher = c.watch_for(raw_wql=device_connected_wql)
	disconnected_watcher = c.watch_for(raw_wql=device_disconnected_wql)
	while 1:
		try:
			connected = connected_watcher(timeout_ms=10)
		except wmi.x_wmi_timed_out:
			pass
		else:
			if connected:
				pnot("device connected","a device has been connected to your computer")
		try:
			disconnected = disconnected_watcher(timeout_ms=10)
		except wmi.x_wmi_timed_out:
			pass
		else:
			if disconnected:
				pnot("device disconnected","a device has been disconnected from your computer")

if __name__=="__MAIN__": main()
