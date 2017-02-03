#!/usr/bin/python

from sense_hat import SenseHat

from utils import *



gPowerOnLED = 0
gCameraOn = 0
gMicOn = 0
gSurvDir = "/home/backups/surveillance/motion_detection/"
gRecDir = "/home/backups/surveillance/recordings/"



# ===================================	functions	================================
def GetSurvDir():
	return gSurvDir


def GetPowerOnLED():
	return gPowerOnLED


def SetPowerLED(on=1):
	global gPowerOnLED
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
	if (GetIsDisableVideo() == 1):
		return

	if (gCameraOn == 1):
		return

	# snapshot command
	command = "raspistill -o " + gSurvDir + CurDateStr() + "/" + CurTimeStr() + ".jpg"
	os.system(command)

	print color.cYellow.value + "Snapshot taken" + color.cEnd.value


def TakeShortClip():
	if (GetIsDisableVideo() == 1):
		return

	if (gCameraOn == 1):
		return

	# command of taking 3 sec video clip
	command = "raspivid -o " + gSurvDir + CurDateStr() + "/"  + CurTimeStr() + ".h264 -t 3000"
	os.system(command)

	print color.cYellow.value + "Short clip captured" + color.cEnd.value


def RecordAudio():
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
