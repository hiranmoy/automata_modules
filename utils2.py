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
from sensors import *



gFluLight = Appliance(1, fluLightGPIO, "fluLight")
gPlug0 = Appliance(1, plug0GPIO, "plug0")
gFan = Appliance(1, fanGPIO, "fan")
gBalconyLight = Appliance(1, balconyLightGPIO, "balconyLight")
gBulb0 = Appliance(1, bulb0GPIO, "bulb0")
gPlug1 = Appliance(1, plug1GPIO, "plug1")
gLEDFlood = LEDFloodLight(1, ledFloodGPIO, "LED_flood_light")

gTouchSensor = TouchSensor(1, touchGPIO, "Touch_sensor")
gMotionSensor = MotionSensor(motionGPIO, "Motion_sensor")

gWeather = Weather("Weather")

gAlcoholSensor = AlcoholSensor("Alcohol_sensor")
gCOSensor = COSensor("CO_sensor")
gSmokeSensor = SmokeSensor("Smoke_sensor")

gPowerOnLED = 0

gExit = 0


# ===================================	functions	================================
def ExitThread(exit=1):
	global gExit
	gExit = exit


def IsExitTread():
	return gExit


def SaveSettings():
	pSettingsFile = open(GetSettingsFile(), "w")

	pSettingsFile.write(str(gMotionSensor.IsEnabled()) + "    : Enable Motion Sensor\n")			# 1
	pSettingsFile.write(str(GetIsDisableVideo()) + "    : Disable Video\n")													# 2
	pSettingsFile.write(str(GetIsDisableAudio()) + "    : Disable Audio\n")													# 3
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


	pProfileFile = open(GetSensorLogFile(), "w")

	gWeather.SaveReadings(pProfileFile)							# 1-3
	gAlcoholSensor.SaveReadings(pProfileFile)				# 4
	gCOSensor.SaveReadings(pProfileFile)						# 5
	gSmokeSensor.SaveReadings(pProfileFile)					# 6

	pProfileFile.close()


def RestoreProfileOfAll():
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


	# check for sensor log
	if (os.path.isfile(GetSensorLogFile()) == 0):
		DumpActivity("No sensor info", color.cCyan)
		return

	pProfileFile = open(GetSensorLogFile(), "r")

	lineNum = 0
	for line in pProfileFile:
		lineNum += 1

		if (lineNum < 4):
			gWeather.RestoreReadings(lineNum, line)

		if (lineNum == 4):
			gAlcoholSensor.RestoreReadings(line)

		if (lineNum == 5):
			gCOSensor.RestoreReadings(line)

		if (lineNum == 6):
			gSmokeSensor.RestoreReadings(line)

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


def TakeSnapshot():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableVideo() == 1):
		return

	if IsCamBusy():
		return

	# snapshot command
	command = "raspistill -o " + GetSurvDir() + CurDateStr() + "/" + CurTimeStr() + ".jpg"
	os.system(command)

	DumpActivity("Snapshot taken", color.cYellow)


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

	if IsCamBusy():
		return
	SetCamBusy()

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

	if ((forced == 0) & (IsCamBusy() == 0)):
		return
	SetCamBusy(0)

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

	if IsCamBusy():
		return
	SetCamBusy()

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

	if ((forced == 0) & (IsCamBusy() == 0)):
		return
	SetCamBusy(0)

	# kill camera on script
	if (os.path.isfile(GetDumpArea() + "video_rec_on_script.process")):
		command = "kill -2 `cat " + GetDumpArea() + "video_rec_on_script.process`"
		os.system(command)


def StartAudioRecording():
	if (IsCameraAdded() != 1):
		return

	if (GetIsDisableAudio() == 1):
		return

	if IsMicBusy():
		return
	SetMicBusy()

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

	if ((forced == 0) & (IsMicBusy() == 0)):
		return
	SetMicBusy(0)

	# kill camera on script
	if (os.path.isfile(GetDumpArea() + "audio_rec_on_script.process")):
		command = "kill -2 `cat " + GetDumpArea() + "audio_rec_on_script.process`"
		os.system(command)



# ===================================	timer	===================================
def Timer1Min():
	timeInSec = 0

	while(1):
		if gExit:
			break

		time.sleep(1)
		timeInSec += 1

		if (timeInSec % 10 == 9):
			SaveSettings()

		if (timeInSec == 60):
			timeInSec = 0

			# unset touch sensor pressed status
			gTouchSensor.ClearTriggeredStatus()

			if (GetAddedLightings() == 1):
				gFluLight.UpdateSwitchedProfile()
				gPlug0.UpdateSwitchedProfile()
				gFan.UpdateSwitchedProfile()
				gBalconyLight.UpdateSwitchedProfile()
				gBulb0.UpdateSwitchedProfile()
				gPlug1.UpdateSwitchedProfile()

			if (GetAddedLirc() == 1):
				gLEDFlood.UpdateSwitchedProfile()

			if IsSenseHatAdded():
				gWeather.UpdateReadings()

			SaveProfileOfAll()
