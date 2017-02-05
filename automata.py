#!/usr/bin/python

import shutil
import sys

from tcp import *



gTcpMonitorThread = threading.Thread(target=MonitorTcpConnection)



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
			SwitchOnFluLight(int(val))

		elif (lineNum == 6):
			# Switch on Plug0
			SwitchOnPlug0(int(val))

		elif (lineNum == 7):
			# Switch on Fan
			SwitchOnFan(int(val))

		elif (lineNum == 8):
			# Switch on balcony light
			SwitchOnBalconyLight(int(val))

		elif (lineNum == 9):
			# Switch on bulb0
			SwitchOnBulb0(int(val))

		elif (lineNum == 10):
			# Switch on Plug1
			SwitchOnPlug1(int(val))

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
			argStr = argStr + " " + arg

			if nextArg.isdigit():
				lightIdx = int(nextArg)
				AddLightings(lightIdx)
				continue

		# add lirc
		if (arg == "-addLirc"):
			AddLirc()
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
SaveSettings()
DumpActivity("Arguments:" + argStr, color.cRed)


# dump process id
pProcessFile = open(GetDumpArea() + CurDateTimeStr() + ".pid", "w")
pProcessFile.write("%s" % os.getpid())
pProcessFile.close()


# launch bg scripts
command = "/home/pi/automation/crash_check.pl &"
os.system(command)


# end streaming/video, audio recording
EndStreaming(1)
EndVideoRecording(1)
EndAudioRecording(1)


# start tcp monitor thread
gTcpMonitorThread.start()


# start tcp
StartTcpThread()


# closing
OnClosing()

DumpActivity("automata exited", color.cRed)
