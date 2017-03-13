#!/usr/bin/python


# -*- Python -*-

#*****************************************************************
#
#        			 Copyright 2016 Hiranmoy Basak
#
#                  All Rights Reserved.
#
#           THIS WORK CONTAINS TRADE SECRET And
#       PROPRIETARY INFORMATION WHICH Is THE PROPERTY
#            OF HIRANMOY BASAK OR ITS LICENSOR
#            AND IS SUBJECT TO LICENSE TERMS.
#
#*****************************************************************/
#
# No part of this file may be reproduced, stored in a retrieval system,
# Or transmitted in any form Or by any means --- electronic, mechanical,
# photocopying, recording, Or otherwise --- without prior written permission
# of Hiranmoy Basak.
#
# WARRANTY:
# Use all material in this file at your own risk. Hiranmoy Basak.
# makes no claims about any material contained in this file.
# 
# Author: Hiranmoy Basak (hiranmoy.iitkgp@gmail.com)


import os
import time
import datetime

from enums import *



gDisableVideo = 0
gDisableAudio = 0
#gEnableBluetooth = 0

gAddMotionSensor = 0
gAddCamera = 0
gAddLightings = 0
gAddLirc = 0
gDebugMode = 0
gAddSenseHat = 0
gAddTouchSensor = 0
gAddGasSensor = 0

# checks whether camera/mic is busy
gCameraOn = 0
gMicOn = 0

gSurvDir = "/home/backups/surveillance/motion_detection/"
gRecDir = "/home/backups/surveillance/recordings/"
gAutomataDir = "/home/pi/automation/"

gDumpArea = "dump/"
gSettingsArea = "settings/"

gLogFile = "activity.log"
gSettingsFile = "settings.ini"
gPowerLog = "power.log"
gSensorLog = "sensor.log"



# ===================================	functions	================================
def DumpActivity(dumpStr, colorCode):
	print colorCode.value + dumpStr + color.cEnd.value

	# check for log file
	if (os.path.isdir(GetDumpArea()) == 0):
		return

	pLogFile = open(GetLogFile(), "a")
	pLogFile.write("%s\n" % dumpStr)
	pLogFile.close()


def GetSurvDir():
	return gSurvDir


def GetRecordDir():
	return gRecDir


def GetAutomataDir():
	return gAutomataDir


def GetDumpArea():
	return (gAutomataDir + gDumpArea)


def GetSettingsArea():
	return (gAutomataDir + gSettingsArea)


def GetPowerLogFile():
	return (GetSettingsArea() + gPowerLog)


def GetSensorLogFile():
	return (GetSettingsArea() + gSensorLog)


def GetSettingsFile():
	return (GetSettingsArea() + gSettingsFile)


def GetLogFile():
	return (GetDumpArea() + gLogFile)


def GetTime():
	now = time.strftime("%H:%M:%S")
	return now


def SetCamBusy(busy=1):
	global gCameraOn
	gCameraOn = busy


def IsCamBusy():
	return gCameraOn


def SetMicBusy(busy=1):
	global gMicOn
	gMicOn = busy


def IsMicBusy():
	return gMicOn


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


def GetIsDisableVideo():
	return gDisableVideo


def SetDisableVideo(val=1):
	if (IsCameraAdded() != 1):
		return

	global gDisableVideo
	gDisableVideo = val


def GetIsDisableAudio():
	return gDisableAudio


def SetDisableAudio(val=1):
	if (IsCameraAdded() != 1):
		return

	global gDisableAudio
	gDisableAudio= val


#def SetBluetooth(val):
#	global gEnableBluetooth
#	gEnableBluetooth = val

#	if (gEnableBluetooth):
#		GPIO.output(bluetoothGPIO, True)
#	else:
#		GPIO.output(bluetoothGPIO, False)


def AddMotionSensor(add=1):
	global gAddMotionSensor
	gAddMotionSensor = add


def IsMotionSensorAdded():
	return gAddMotionSensor


def AddCamera(add=1):
	global gAddCamera
	gAddCamera = add


def IsCameraAdded():
	return gAddCamera


def AddLightings(add):
	global gAddLightings
	gAddLightings = add


def GetAddedLightings():
	return gAddLightings


def AddLirc(add):
	global gAddLirc
	gAddLirc = add


def GetAddedLirc():
	return gAddLirc


def IsDebugMode():
	return gDebugMode


def SetDebugMode(on=1):
	global gDebugMode
	gDebugMode = on


def AddSenseHat(add=1):
	global gAddSenseHat
	gAddSenseHat = add


def IsSenseHatAdded():
	return gAddSenseHat


def AddTouchSensor(add):
	global gAddTouchSensor
	gAddTouchSensor = add


def GetAddedTouchSensor():
	return gAddTouchSensor


def AddGasSensor(add=1):
	global gAddGasSensor
	gAddGasSensor = add


def IsGasSensorAdded():
	return gAddGasSensor
