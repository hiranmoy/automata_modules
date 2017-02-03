#!/usr/bin/python

import os
import time
import datetime

from enums import *
from gpioSetup import *


gDumpArea = "/home/pi/automation/dump/"
gLogFile = "activity.log"
gSettingsFile = "settings.ini"

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



# ===================================	functions	================================
# dump debug info
def DumpUtilsDebugInfo():
	print "gEnableMotionSensor: %s" % gEnableMotionSensor
	print "gDisableVideo: %s" % gDisableVideo
	print "gDisableAudio: %s" % gDisableAudio
	print "gEnableBluetooth : %s" % gEnableBluetooth
	print "gPowerOnFluLight: %s" % gPowerOnFluLight
	print "gPowerOnPlug0: %s" % gPowerOnPlug0
	print "gPowerOnFan: %s" % gPowerOnFan
	print "gPowerOnBalconyLight: %s" % gPowerOnBalconyLight
	print "gPowerOnBulb0: %s" % gPowerOnBulb0
	print "gPowerOnPlug1: %s" % gPowerOnPlug1


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
	global gEnableMotionSensor
	gEnableMotionSensor = val
	SaveSettings()


def GetIsDisableVideo():
	return gDisableVideo


def SetDisableVideo(val=1):
	global gDisableVideo
	gDisableVideo = val
	SaveSettings()


def GetIsDisableAudio():
	return gDisableAudio


def SetDisableAudio(val=1):
	global gDisableAudio
	gDisableAudio= val
	SaveSettings()


def SetBluetooth(val):
	global gEnableBluetooth
	gEnableBluetooth = val
	SaveSettings()

	if (gEnableBluetooth):
		GPIO.output(bluetoothGPIO, True)
	else:
		GPIO.output(bluetoothGPIO, False)


def CheckIfOnFluLight():
	return gPowerOnFluLight


def SwitchOnFluLight(val):
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
