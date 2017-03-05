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



import shutil
import sys

from tcp import *



gTcpMonitorThread = threading.Thread(target=MonitorTcpConnection)
gTimer1MinThread = threading.Thread(target=Timer1Min)



# ===================================	functions	================================
def OnClosing():
	# switch off bluetooth speaker and all appliances
	ClearGPIO()

	# stop tcp thread
	ExitThread()

	# end streaming/video, audio recording
	EndStreaming()
	EndVideoRecording()
	EndAudioRecording()

	# kill the crash check script
	command = "kill -9 `cat " + GetDumpArea() + "crash_check_script.process`"
	os.system(command)

	# end the per script running in background
	command = "touch " + GetDumpArea() + "end"
	os.system(command)


def KillPrevProcesses():
	OnClosing()

	#env the prev automata program
	command = "kill -9 `cat " + GetDumpArea() + "/.*pid`"
	os.system(command)

	activityLog = GetDumpArea() + "activity.log"
	# check if activity file exists
	if os.path.isfile(activityLog):
		# move activity file to home area
		prevActivityLog = "/home/pi/activity.log"
		shutil.move(activityLog, prevActivityLog)

	ExitThread(0)


# Restore previous settings from the settings.ini
def RestoreSettings():
	# check for settings file
	if (os.path.isfile(GetSettingsFile()) == 0):
		print color.cCyan.value + "No settings file" + color.cEnd.value
		return

	pSettingsFile = open(GetSettingsFile(), "r")
	lineNum = 0
	for line in pSettingsFile:
		lineNum += 1
		val = line[0:4]

		if (lineNum == 1):
			# Enable Motion Detection
			EnableMotionSensor(int(val))

		elif (lineNum == 2):
			# Disable Video
			SetDisableVideo(int(val))

		elif (lineNum == 3):
			# Disable Audio
			SetDisableAudio(int(val))

		elif (lineNum == 4):
			# Enable Bluetooth
			SetBluetooth(int(val))

		elif (lineNum == 5):
			# Switch on Fluorescent light
			gFluLight.SetPoweredOn(int(val))

		elif (lineNum == 6):
			# Switch on Plug0
			gPlug0.SetPoweredOn(int(val))

		elif (lineNum == 7):
			# Switch on Fan
			gFan.SetPoweredOn(int(val))

		elif (lineNum == 8):
			# Switch on balcony light
			gBalconyLight.SetPoweredOn(int(val))

		elif (lineNum == 9):
			# Switch on bulb0
			gBulb0.SetPoweredOn(int(val))

		elif (lineNum == 10):
			# Switch on Plug1
			gPlug1.SetPoweredOn(int(val))

		else:
			pSettingsFile.close()
			print color.cRed.value + "Invalid settings file" + color.cEnd.value
			return

	pSettingsFile.close()


# ============================== process arguments ============================
def ProcessArguments():
	argStr = ""

	argIdx = 0
	while (1):
		argIdx += 1
		if (argIdx >= len(sys.argv)):
			break

		arg = sys.argv[argIdx]
		argStr = argStr + " " + arg

		# add motion sensor
		if (arg == "-addMotionSensor"):
			AddMotionSensor()
			continue

		# add camera
		if (arg == "-addCamera"):
			AddCamera()
			continue

		# add lightings
		if (arg == "-addLightings"):
			argIdx += 1

			nextArg = sys.argv[argIdx]
			argStr = argStr + " " + nextArg

			if nextArg.isdigit():
				lightIdx = int(nextArg)
				AddLightings(lightIdx)

				# load previous power data
				if (GetAddedLightings() == 1):
					RestoreProfileOfAll()

				continue

		# add lirc
		if (arg == "-addLirc"):
			AddLirc()
			continue

		# set debug mode
		if (arg == "-debug"):
			SetDebugMode()
			continue

		# add senseHat
		if (arg == "-addSenseHat"):
			AddSenseHat()
			ClearSenseHat()
			continue

		# add touch sensor
		if (arg == "-addTouchSensor"):
			AddTouchSensor()
			continue

		# add gas sensor
		if (arg == "-addGasSensor"):
			AddGasSensor()
			continue

		# invalid argument
		print color.cRed.value + "Invalid argument : " + arg + color.cEnd.value
		return "-1"

	return argStr


# ===================================	run	======================================
argStr = ProcessArguments()
if (argStr == "-1"):
	OnClosing()
	sys.exit()


# Starting ... intialization
SetupGPIOs()


KillPrevProcesses()


# load previous settings
RestoreSettings()


# dump area setup
if (os.path.isdir(GetDumpArea())):
	shutil.rmtree(GetDumpArea())

os.makedirs(GetDumpArea())

# move the previous activity file
movedActivityLog = "/home/pi/activity.log"
if os.path.isfile(movedActivityLog):
	prevActivityLog = GetDumpArea() + "prevActivity.log"
	shutil.move(movedActivityLog, prevActivityLog)


SaveSettings()
DumpActivity("Arguments:" + argStr, color.cRed)


# dump process id
pProcessFile = open(GetDumpArea() + CurDateTimeStr() + ".pid", "w")
pProcessFile.write("%s" % os.getpid())
pProcessFile.close()


# launch bg scripts
if (IsDebugMode() != 1):
	command = "/home/pi/automation/crash_check.pl &"
	os.system(command)


# end streaming/video, audio recording
EndStreaming(1)
EndVideoRecording(1)
EndAudioRecording(1)


# enable touch sensor
EnableTouchSensor()


# start tcp monitor thread
gTcpMonitorThread.start()


# start 1 min timer thread
gTimer1MinThread.start()


# start tcp
StartTcpThread()


# closing
OnClosing()

DumpActivity("automata exited", color.cRed)
