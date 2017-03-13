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


# code hierarchy:
#
# automata
#		tcp
#			utils2
#				lirc
#					appliance
#						gpio
#				sensor
#						gpio
#							util
#								enums


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
		DumpActivity("No settings file", color.cCyan)
		return

	pSettingsFile = open(GetSettingsFile(), "r")
	lineNum = 0
	for line in pSettingsFile:
		lineNum += 1
		val = line[0:4]

		if (lineNum == 1):
			# Enable Motion Detection
			gMotionSensor.EnableSensor(int(val))

		elif (lineNum == 2):
			# Disable Video
			SetDisableVideo(int(val))

		elif (lineNum == 3):
			# Disable Audio
			SetDisableAudio(int(val))

		#elif (lineNum == 4):
		#	Enable Bluetooth
		#	SetBluetooth(int(val))

		else:
			pSettingsFile.close()
			DumpActivity("Invalid settings file", color.cRed)
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

			continue

		# add lirc
		if (arg == "-addLirc"):
			argIdx += 1

			nextArg = sys.argv[argIdx]
			argStr = argStr + " " + nextArg

			if nextArg.isdigit():
				lircIdx = int(nextArg)
				AddLirc(lircIdx)

			continue

		# set debug mode
		if (arg == "-debug"):
			SetDebugMode()
			continue

		# add senseHat
		if (arg == "-addSenseHat"):
			AddSenseHat()

			# clear senseHat
			sense = SenseHat()
			sense.clear()

			continue

		# add touch sensor
		if (arg == "-addTouchSensor"):
			argIdx += 1

			nextArg = sys.argv[argIdx]
			argStr = argStr + " " + nextArg

			if nextArg.isdigit():
				touchIdx = int(nextArg)
				AddTouchSensor(touchIdx)

			continue

		# add gas sensor
		if (arg == "-addGasSensor"):
			AddGasSensor()
			continue

		# invalid argument
		DumpActivity("Invalid argument : " + arg, color.cRed)
		return "-1"

	return argStr


# ===================================	run	======================================
argStr = ProcessArguments()
if (argStr == "-1"):
	OnClosing()
	sys.exit()


KillPrevProcesses()


# dump area setup
if (os.path.isdir(GetDumpArea())):
	shutil.rmtree(GetDumpArea())

os.makedirs(GetDumpArea())


# Starting ... intialization
# GPIO setup
SetupGPIOs()
DumpActivity("GPIO setup done", color.cGreen)


# enable touch sensor
gTouchSensor.EnableSensor()


# load previous settings
RestoreSettings()


# load previous profile
RestoreProfileOfAll()


# create settings area if it doesn't exist
if (os.path.isdir(GetSettingsArea()) == 0):
	os.makedirs(GetSettingsArea())


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


# start tcp monitor thread
gTcpMonitorThread.start()


# start 1 min timer thread
gTimer1MinThread.start()


# start tcp
StartTcpThread()


# closing
OnClosing()

DumpActivity("automata exited", color.cRed)
