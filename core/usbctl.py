import wmi
import pythoncom
c=wmi.WMI ()
def monitor_connected:
	pythoncom.CoInitialize()
	device_connected_wql="SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
	csound=sound.sound()
	csound.load("s/usbadded.wav")
	while True:
		time.sleep(0.5)
		connected = connected_watcher()
		if connected:
			pnot("device connected","a device has been connected to your computer")
			if getopt('usb_monitor_options','sounds',type='b'): csound.play()
			if getopt('usb_monitor_options','speech',type='b'): output.speak("device connected")


def monitor_connected:
	dsound=sound.sound()
	dsound.load("s/usbremoved.wav")
	device_disconnected_wql="SELECT * FROM __InstanceDeletionEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
	disconnected_watcher = c.watch_for(raw_wql=device_disconnected_wql)
	while True:
		if disconnected:
			pnot("device disconnected","a device has been disconnected from your computer")
			if getopt('usb_monitor_options','sounds',type='b'): dsound.play()
			if getopt('usb_monitor_options','speech',type='b'): output.speak("device disconnected")