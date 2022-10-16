
#imports
import os
import time
import win32api
from core import sound,idle,output
from core import file_manager as fm
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
import os
#config parser initialisation
config = configparser.ConfigParser()
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
def main():
#init stuff
#	usb=usbctl.usbctl()
	if fm.file_exists(fm.get_working_directory()+"\\np.cf"):
		if not fm.directory_exists(os.environ['appdata']+"\\blindelectron"): fm.directory_create(os.environ['appdata']+"\\blindelectron")
		if not fm.file_exists(os.environ['appdata']+"\\blindelectron\\estarter.ini"): fm.file_copy(fm.get_working_directory()+"\\config_default.ini",os.environ['appdata']+"\\blindelectron\\estarter.ini",True)
		config.read(os.environ['appdata']+"\\blindelectron\\estarter.ini")
	else:
		config.read("config.ini")
	if float(getcopt('version'))>=1.1:
		pass
	else:
		print ('error, your config file is to old, version '+getcopt('version')+', is to old fore this version of estarter.')
		es.play_wait()
		exit()
	if getopt('system monitor options','notify_prowl',type='b')==True:
		set_prowl_key()
	if getopt('system monitor options','idle_closing',type='b')==True or getopt('idle_options','mute_wen_idle',type='b')==True or getopt('system monitor options','notify_prowl',type='b')==True:
		idle=Thread(target=idleloop)
		idle.start()
	fsync=Thread(target=back_folders,args="s")
	volmon=Thread(target=vmon)
	fsync.start()
	volmon.start()
	if getopt('system monitor options','battery_announce',type='b')==True:
		bthread=Thread(target=batrloop)
		bthread.start()
	if getopt('system monitor options','usb_monitor',type='b')==True:
		uthread=Thread(target=monitor_disconnected)
		utwothread=Thread(target=monitor_connected)
		uthread.start()
		utwothread.start()
	if getopt('git_options','gitupdater',type='b'):
		gthread=Thread(target=repoloop)
		gthread.start()

def closeapps():
	capps=getapps()
	for procloop in capps:
		subprocess.Popen("taskkill.exe /im "+getopt("clapp "+procloop,procloop+"@file"),shell=True,stdout=None)

def back_folders(mode="s"):
	folders=getfolders()
	for foldloop in folders:
		foldera=getopt("folder "+foldloop,foldloop+"@source")
#		print(foldera)
		folderb=getopt("folder "+foldloop,foldloop+"@dest")
#		print(folderb)
		if mode=="s":
			sp=Thread(target=syncfolder,args=("s",foldera,folderb))
			sp.start
			while True:
				if not sp.is_alive():
					time.sleep(.5000)
					sp=Thread(target=syncfolder,args=("s",foldera,folderb,))
					sp.start()
			else:
				continue
		elif mode=="u":
			syncfolder("u",foldera,folderb,)

def syncfolder(mode,folder1,folder2):
	if mode=="s":
		saved_stdout, saved_stderr = sys.stdout, sys.stderr
		sys.stdout = sys.stderr = open(os.devnull, "w")
		sync (folder1,folder2,"sync")
		sys.stdout, sys.stderr = saved_stdout, saved_stderr
		if mode=="u":
			sync (folder1,folder2,"update")

def getfolders():
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

def getcopt(option):
	cfg_object=open('config.ini','r')
	cfg=cfg_object.readlines()
	cfg_object.close()
	opt=''
	for cl in cfg:
		cll=cl.split(' ')
		if cll[0]==';!'+option:
			cll=cl.split(' ')
			clll=cll[1].split('\n')
			opt=clll[	0]
			break
		else:
			continue
	return opt

def idleloop():
	#init stuff
	global donethings
	s=sound.sound()
	s.load('s/warn.wav')
	afktime=getopt('idle_options','afk_time',type='i')
	warntime=getopt('idle_options','warn_time',type='i')
	soundplayed=False
	while True:
		if idle.get_idle_duration()>=afktime:
			if not soundplayed:
				s.play()
				soundplayed=True
			if idle.get_idle_duration()>=afktime+warntime and donethings==False:
				if getopt('system monitor options','idle_closing',type='b')==True: closeapps()
				if getopt('idle_options','mute_wen_idle',type='b')==True: volume.SetMute(1,None)
				donethings=True
			elif idle.get_idle_duration()<afktime and soundplayed==True:
				if getopt('system monitor options','notify_prowl',type='b')==True and donethings==True: pnot('computer not idle','some one is interacting with your computer')
				donethings=False
				soundplayed=False
				if getopt('idle_options','mute_wen_idle',type='b')==True: volume.SetMute(0,None)


def getapps():
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
	vl =volume.GetMasterVolumeLevel()
	vs=sound.sound()
	if getopt('system monitor options','volume_sound_enabled',type='b')==True:
		vs.load("s/volume.wav")
#		callback for watch
	def volwatch(a,ab,abc):
		if getopt('system monitor options','volume_tone_enabled',type='b')==True:
			toneplay()
		if getopt('system monitor options','volume_sound_enabled',type='b')==True:
			vs.play()
	watch(vl,callback=volwatch)
	while True:
		vl =volume.GetMasterVolumeLevel()
		time.sleep(0.5)
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
		time.sleep(0.5)
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
		pr.notify(event,message,priority=getopt('prowl options','priority',type='i'),appName='EStarter')
		print("notification sent to prowl")
	except Exception as  e:
		print ("Error sending notification to Prowl:",e)
		es.play()


def monitor_connected():
	pythoncom.CoInitialize()
	cone=wmi.WMI ()
	device_connected_wql="SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
	csound=sound.sound()
	csound.load("s/usbadded.wav")
	connected_watcher = cone.watch_for(raw_wql=device_connected_wql)
	while True:
		time.sleep(0.5)
		connected = connected_watcher()
		if connected:
			pnot("device connected","a device has been connected to your computer")
			if getopt('usb_monitor_options','sounds',type='b'): csound.play()
			if getopt('usb_monitor_options','speech',type='b'): output.speak("device connected")

def monitor_disconnected():
	pythoncom.CoInitialize()
	ctwo=wmi.WMI ()
	dsound=sound.sound()
	dsound.load("s/usbremoved.wav")
	device_disconnected_wql="SELECT * FROM __InstanceDeletionEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
	disconnected_watcher = ctwo.watch_for(raw_wql=device_disconnected_wql)
	while True:
		disconnected = disconnected_watcher()
		if disconnected:
			pnot("device disconnected","a device has been disconnected from your computer")
			if getopt('usb_monitor_options','sounds',type='b'): dsound.play()
			if getopt('usb_monitor_options','speech',type='b'): output.speak("device disconnected")

def usbloop():
	pythoncom.CoInitialize()
	device_connected_wql="SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
	csound=sound.sound()
	dsound=sound.sound()
	csound.load("s/usbadded.wav")
	dsound.load("s/usbremoved.wav")
	device_disconnected_wql="SELECT * FROM __InstanceDeletionEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
	c=wmi.WMI ()
	connected_watcher = c.watch_for(raw_wql=device_connected_wql)
	disconnected_watcher = c.watch_for(raw_wql=device_disconnected_wql)
	while 1:
		time.sleep(0.5)
		try:
			connected = connected_watcher(timeout_ms=10)
		except wmi.x_wmi_timed_out:
			pass
		else:
			if connected:
				pnot("device connected","a device has been connected to your computer")
				if getopt('usb_monitor_options','sounds',type='b'): csound.play()
				if getopt('usb_monitor_options','speech',type='b'): output.speak("device connected")
		try:
			disconnected = disconnected_watcher(timeout_ms=10)
		except wmi.x_wmi_timed_out:
			pass
		else:
			if disconnected:
				pnot("device disconnected","a device has been disconnected from your computer")
				if getopt('usb_monitor_options','sounds',type='b'): dsound.play()
				if getopt('usb_monitor_options','speech',type='b'): output.speak("device disconnected")

def repoloop():
	#a function to go thrue a directory in the config file and update all git repos contained with in.
	gitdirs = config.sections()
	gitdirs = [g for g in gitdirs if g.lower().startswith("gitdir ")]
	results = []
	for gitd in gitdirs:
		name=gitd.split(' ',1)[1]
#		print(name)
		results.append(str(name))
	for re in results:
		gitdict={re+"thread":Thread(target=gitloop,args=(re,),)}
#		gitloop(re)
		cthread=gitdict[re+"thread"]
		if not cthread.is_alive():
			cthread.start()
		else:
			continue


def gitloop(r,*args,**kwargs):
	gu=sound.sound()
#	print(r+" initialized")
	gu.load("s/oneup.wav")
	au=sound.sound()
	au.load("s/allup.wav")
	gitrepos=os.listdir(getopt("gitdir "+r,r+"@path",type='s'))
	ps=os.environ['systemroot']+"\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"
	while True:
		time.sleep(getopt('gitdir '+r,r+'@update_interval',type='i')*60)
		for gr in gitrepos:
			subprocess.call(ps+" cd \'"+getopt("gitdir "+r,r+"@path",type='s')+"\\"+gr+"\';git pull",shell=True,stdout=None)
			if getopt('git_options','sounds',type='b'):
				gu.play()
			if getopt('git_options','speech',type='b'):
				output.speak(gr+" repo updated for "+r+".")
		if getopt('git_options','sounds',type='b'):
			au.play()
		if getopt('git_options','speech',type='b'):
			output.speak("all repos updated for "+r+".")
			continue

if __name__=="__main__": main()