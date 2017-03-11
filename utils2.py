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



from lirc import *



gEnableMotionSensor = 0
gDisableVideo = 0
gDisableAudio = 0
#gEnableBluetooth = 0

gFluLight = Appliance(1, fluLightGPIO, "fluLight")
gPlug0 = Appliance(1, plug0GPIO, "plug0")
gFan = Appliance(1, fanGPIO, "fan")
gBalconyLight = Appliance(1, balconyLightGPIO, "balconyLight")
gBulb0 = Appliance(1, bulb0GPIO, "bulb0")
gPlug1 = Appliance(1, plug1GPIO, "plug1")
gLEDFlood = LEDFloodLight(1, ledFloodGPIO, "LED_flood_light")

gPowerOnLED = 0
gCameraOn = 0
gMicOn = 0
gExit = 0



# ===================================	functions	================================
def ExitThread(exit=1):
	global gExit
	gExit = exit


def IsExitTread():
	return gExit


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


#def SetBluetooth(val):
#	global gEnableBluetooth
#	gEnableBluetooth = val
#	SaveSettings()

#	if (gEnableBluetooth):
#		GPIO.output(bluetoothGPIO, True)
#	else:
#		GPIO.output(bluetoothGPIO, False)


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


def SaveSettings():
	pSettingsFile = open(GetSettingsFile(), "w")

	pSettingsFile.write(str(gEnableMotionSensor) + "    : Enable Motion Sensor\n")			# 1
	pSettingsFile.write(str(gDisableVideo) + "    : Disable Video\n")										# 2
	pSettingsFile.write(str(gDisableAudio) + "    : Disable Audio\n")										# 3

	#pSettingsFile.write(str(gEnableBluetooth) + "    : Enable Bluetooth\n")									

	pSettingsFile.close()


def SaveProfileOfAll():
	pProfileFile = open(GetPowerLogFile(), "w")

	gFluLight.SaveProfile(pProfileFile)							# 1
	gPlug0.SaveProfile(pProfileFile)								# 2
	gFan.SaveProfile(pProfileFile)									# 3
	gBalconyLight.SaveProfile(pProfileFile)					# 4
	gBulb0.SaveProfile(pProfileFile)								# 5
	gPlug1.SaveProfile(pProfileFile)								# 6
	gLEDFlood.SaveProfile(pProfileFile)							# 7

	pProfileFile.close()


def RestorePowerOfAll():
	# check for power log
	if (os.path.isfile(GetPowerLogFile()) == 0):
		DumpActivity("No power info", color.cCyan)
		return

	pProfileFile = open(GetPowerLogFile(), "r")

	lineNum = 0
	for line in pProfileFile:
		lineNum += 1

		if (lineNum == 1):
			gFluLight.RestoreProfile(line)

		if (lineNum == 2):
			gPlug0.RestoreProfile(line)

		if (lineNum == 3):
			gFan.RestoreProfile(line)

		if (lineNum == 4):
			gBalconyLight.RestoreProfile(line)

		if (lineNum == 5):
			gBulb0.RestoreProfile(line)

		if (lineNum == 6):
			gPlug1.RestoreProfile(line)

		if (lineNum == 7):
			gLEDFlood.RestoreProfile(line)

			# press on "off" button (3) if switched on
			gLEDFlood.SendIRSignal(gLEDFlood.GetLEDKEYs(3))

	pProfileFile.close()


def GetPowerOnLED():
	return gPowerOnLED


def SetPowerLED(on=1):
	global gPowerOnLED

	if (GetAddedLightings() != 2):
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
	return True


def TakeSnapshot():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableVideo() == 1):
		return

	if (gCameraOn == 1):
		return

	# snapshot command
	command = "raspistill -o " + GetSurvDir() + CurDateStr() + "/" + CurTimeStr() + ".jpg"
	os.system(command)

	DumpActivity("Snapshot taken", color.cYellow)


def TakeShortClip():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableVideo() == 1):
		return

	if (gCameraOn == 1):
		return

	# command of taking 3 sec video clip
	command = "raspivid -o " + GetSurvDir() + CurDateStr() + "/"  + CurTimeStr() + ".h264 -t 3000"
	os.system(command)

	DumpActivity("Short clip captured", color.cYellow)


def RecordAudio():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableAudio() == 1):
		return

	if (gMicOn == 1):
		return

	# command of recording 3 sec audio clip
	command = "arecord -D hw:1,0 -r 48000 -d 3 -c 1 -f S16_LE " + \
						GetSurvDir() + CurDateStr() + "/"  + CurTimeStr() + ".wav"
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
	curRecDir = GetRecordDir() + str(curDateTime.date())

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
	curRecDir = GetRecordDir() + str(curDateTime.date())

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
