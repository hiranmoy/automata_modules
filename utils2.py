#!/usr/bin/python

import os
import time
import datetime

from sense_hat import SenseHat

from enums import *
from gpioSetup import *


gDumpArea = "/home/pi/automation/dump/"
gLogFile = "activity.log"
gSettingsFile = "settings.ini"
gSurvDir = "/home/backups/surveillance/motion_detection/"
gRecDir = "/home/backups/surveillance/recordings/"

gDebugMode = 0

gEnableMotionSensor = 0
gDisableVideo = 0
gDisableAudio = 0
gEnableBluetooth = 0
gPowerOnFluLight = 0
gPowerOnPlug0 = 0
gPowerOnFan = 0
gPowerOnBalconyLight = 0
gPowerOnBulb0 = 0
gPowerOnPlug1 = 0

gPowerOnLED = 0
gCameraOn = 0
gMicOn = 0



# ===================================	functions	================================
def IsDebugMode():
	return gDebugMode


def SetDebugMode(on=1):
	global gDebugMode
	gDebugMode = on


def GetSurvDir():
	return gSurvDir


def GetDumpArea():
	return gDumpArea


def GetLogFile():
	return (gDumpArea + gLogFile)


def GetSettingsFile():
	return (gDumpArea + gSettingsFile)


def GetTime():
	now = time.strftime("%H:%M:%S")
	return now


def GetIsEnableMotionSensor():
	return gEnableMotionSensor


def SetEnableMotionSensor(val=1):
	if (IsMotionSensorAdded() != 1):
		return

	global gEnableMotionSensor
	gEnableMotionSensor = val
	SaveSettings()


def GetIsDisableVideo():
	return gDisableVideo


def SetDisableVideo(val=1):
	if (IsCameraAdded() != 1):
		return

	global gDisableVideo
	gDisableVideo = val
	SaveSettings()


def GetIsDisableAudio():
	return gDisableAudio


def SetDisableAudio(val=1):
	if (IsCameraAdded() != 1):
		return

	global gDisableAudio
	gDisableAudio= val
	SaveSettings()


def SetBluetooth(val):
	global gEnableBluetooth
	gEnableBluetooth = val
	SaveSettings()

	#if (gEnableBluetooth):
	#	GPIO.output(bluetoothGPIO, True)
	#else:
	#	GPIO.output(bluetoothGPIO, False)


def CheckIfOnFluLight():
	return gPowerOnFluLight


def SwitchOnFluLight(val):
	if (GetAddedLightings() != 1):
		return

	global gPowerOnFluLight
	gPowerOnFluLight = val
	SaveSettings()

	if (gPowerOnFluLight):
		GPIO.output(fluLightGPIO, True)
	else:
		GPIO.output(fluLightGPIO, False)


def CheckIfOnPlug0():
	return gPowerOnPlug0


def SwitchOnPlug0(val):
	if (GetAddedLightings() != 1):
		return

	global gPowerOnPlug0
	gPowerOnPlug0 = val
	SaveSettings()

	if (gPowerOnPlug0):
		GPIO.output(plug0GPIO, True)
	else:
		GPIO.output(plug0GPIO, False)


def CheckIfOnFan():
	return gPowerOnFan


def SwitchOnFan(val):
	if (GetAddedLightings() != 1):
		return

	global gPowerOnFan
	gPowerOnFan = val
	SaveSettings()

	if (gPowerOnFan):
		GPIO.output(fanGPIO, True)
	else:
		GPIO.output(fanGPIO, False)


def CheckIfOnBalconyLight():
	return gPowerOnBalconyLight


def SwitchOnBalconyLight(val):
	if (GetAddedLightings() != 1):
		return

	global gPowerOnBalconyLight
	gPowerOnBalconyLight = val
	SaveSettings()

	if (gPowerOnBalconyLight):
		GPIO.output(balconyLightGPIO, True)
	else:
		GPIO.output(balconyLightGPIO, False)


def CheckIfOnBulb0():
	return gPowerOnBulb0


def SwitchOnBulb0(val):
	if (GetAddedLightings() != 1):
		return

	global gPowerOnBulb0
	gPowerOnBulb0 = val
	SaveSettings()

	if (gPowerOnBulb0):
		GPIO.output(bulb0GPIO, True)
	else:
		GPIO.output(bulb0GPIO, False)


def CheckIfOnPlug1():
	return gPowerOnPlug1


def SwitchOnPlug1(val):
	if (GetAddedLightings() != 1):
		return

	global gPowerOnPlug1
	gPowerOnPlug1 = val
	SaveSettings()

	if (gPowerOnPlug1):
		GPIO.output(plug1GPIO, True)
	else:
		GPIO.output(plug1GPIO, False)


def CurDateStr():
	curDateTime = datetime.datetime.now()

	curDateStr = str(curDateTime.date())
	return curDateStr


def CurTimeStr():
	curDateTime = datetime.datetime.now()

	curTimeStr = str(curDateTime.hour) + "-" + \
							 str(curDateTime.minute) + "-" + \
							 str(curDateTime.second)
	return curTimeStr


def CurDateTimeStr():
	curDateTime = datetime.datetime.now()

	curDateTimeStr = str(curDateTime.date()) + "-" + \
									 str(curDateTime.hour) + "-" + \
									 str(curDateTime.minute) + "-" + \
									 str(curDateTime.second)
	return curDateTimeStr


def DumpActivity(dumpStr, colorCode):
	pLogFile = open(GetLogFile(), "a")
	print colorCode.value + dumpStr + color.cEnd.value
	pLogFile.write("%s\n" % dumpStr)
	pLogFile.close()


def SaveSettings():
	pSettingsFile = open(GetSettingsFile(), "w")

	pSettingsFile.write(str(gEnableMotionSensor) + "    : Enable Motion Sensor\n")			# 1
	pSettingsFile.write(str(gDisableVideo) + "    : Disable Video\n")										# 2
	pSettingsFile.write(str(gDisableAudio) + "    : Disable Audio\n")										# 3
	pSettingsFile.write(str(gEnableBluetooth) + "    : Enable Bluetooth\n")							# 4
	pSettingsFile.write(str(gPowerOnFluLight) + "    : Switch on Fluorescent Light\n")	# 5
	pSettingsFile.write(str(gPowerOnPlug0) + "    : Switch on Plug0\n")									# 6
	pSettingsFile.write(str(gPowerOnFan) + "    : Switch on Fan\n")											# 7
	pSettingsFile.write(str(gPowerOnBalconyLight) + "    : Switch on BalconyLight\n")		# 8
	pSettingsFile.write(str(gPowerOnBulb0) + "    : Switch on Bulb0\n")									# 9
	pSettingsFile.write(str(gPowerOnPlug1) + "    : Switch on Plug1\n")									# 10

	pSettingsFile.close()

def GetPowerOnLED():
	return gPowerOnLED


def SetPowerLED(on=1):
	global gPowerOnLED

	if (GetAddedLightings() != 1):
		return

	gPowerOnLED = on

	if on:
		GPIO.output(lightGPIO, True)
	else:
		GPIO.output(lightGPIO, False)


def CheckForGlitch(channel, high):
	gpioState = GPIO.HIGH if high else GPIO.LOW

	# count number of msec
	time_ms = 0
	while (GPIO.input(channel) == gpioState):
		time.sleep(0.001)
		time_ms += 1
		if (time_ms >= 10):
			return False

	# glitch out if the gpio state lasts less than 10 ms
	#print "glitch at pin %d" % channel
	return True


def TakeSnapshot():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableVideo() == 1):
		return

	if (gCameraOn == 1):
		return

	# snapshot command
	command = "raspistill -o " + gSurvDir + CurDateStr() + "/" + CurTimeStr() + ".jpg"
	os.system(command)

	print color.cYellow.value + "Snapshot taken" + color.cEnd.value


def TakeShortClip():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableVideo() == 1):
		return

	if (gCameraOn == 1):
		return

	# command of taking 3 sec video clip
	command = "raspivid -o " + gSurvDir + CurDateStr() + "/"  + CurTimeStr() + ".h264 -t 3000"
	os.system(command)

	print color.cYellow.value + "Short clip captured" + color.cEnd.value


def RecordAudio():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableAudio() == 1):
		return

	if (gMicOn == 1):
		return

	# command of recording 3 sec audio clip
	command = "arecord -D hw:1,0 -r 48000 -d 3 -c 1 -f S16_LE " + \
						gSurvDir + CurDateStr() + "/"  + CurTimeStr() + ".wav"
	os.system(command)


# toggle LED light
def ToggleLED():
	if gPowerOnLED:
		SetPowerLED(0)
	else:
		SetPowerLED(1)


def StartStreaming():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableVideo() == 1):
		return

	global gCameraOn
	if (gCameraOn == 1):
		return
	gCameraOn = 1

	# camera on command
	command = "/home/pi/automation/cam_on.sh &"
	os.system(command)

	# streaming video
	command = "/home/pi/automation/stream.sh &"
	os.system(command)


def EndStreaming(forced=0):
	if (IsCameraAdded() != 1):
		return

	if ((forced == 0) & (GetIsDisableVideo() == 1)):
		return

	global gCameraOn
	if ((forced == 0) & (gCameraOn == 0)):
		return
	gCameraOn = 0

	# kill camera on script
	if (os.path.isfile(GetDumpArea() + "cam_on_script.process")):
		command = "kill -2 `cat " + GetDumpArea() + "cam_on_script.process`"
		os.system(command)

	# kill streaming script
	if (os.path.isfile(GetDumpArea() + "stream_on_script.process")):
		command = "kill -2 `cat " + GetDumpArea() + "stream_script.process`"
		os.system(command)


def StartVideoRecording():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableVideo() == 1):
		return

	global gCameraOn
	if (gCameraOn == 1):
		return
	gCameraOn = 1

	curDateTime = datetime.datetime.now()
	curRecDir = gRecDir + str(curDateTime.date())

	# create current date directory if doesn't exist
	if (os.path.isdir(curRecDir) == 0):
		os.makedirs(curRecDir)

	# camera on command
	command = "/home/pi/automation/video_rec_on.sh " + curRecDir + "/" + CurTimeStr() + ".h264 &"
	os.system(command)


def EndVideoRecording(forced=0):
	if (IsCameraAdded() != 1):
		return

	if ((forced == 0) & (GetIsDisableVideo() == 1)):
		return

	global gCameraOn
	if ((forced == 0) & (gCameraOn == 0)):
		return
	gCameraOn = 0

	# kill camera on script
	if (os.path.isfile(GetDumpArea() + "video_rec_on_script.process")):
		command = "kill -2 `cat " + GetDumpArea() + "video_rec_on_script.process`"
		os.system(command)


def StartAudioRecording():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableAudio() == 1):
		return

	global gMicOn
	if (gMicOn == 1):
		return
	gMicOn = 1

	curDateTime = datetime.datetime.now()
	curRecDir = gRecDir + str(curDateTime.date())

	# create current date directory if doesn't exist
	if (os.path.isdir(curRecDir) == 0):
		os.makedirs(curRecDir)

	# camera on command
	command = "/home/pi/automation/audio_rec_on.sh " + curRecDir + "/" + CurTimeStr() + ".wav &"
	os.system(command)


def EndAudioRecording(forced=0):
	if (IsCameraAdded() != 1):
		return

	if ((forced == 0) & (GetIsDisableAudio() == 1)):
		return

	global gMicOn
	if ((forced == 0) & (gMicOn == 0)):
		return
	gMicOn = 0

	# kill camera on script
	if (os.path.isfile(GetDumpArea() + "audio_rec_on_script.process")):
		command = "kill -2 `cat " + GetDumpArea() + "audio_rec_on_script.process`"
		os.system(command)
