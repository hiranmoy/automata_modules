#!/usr/bin/python

import thread

from utils2 import *



gMonitorStatus = "-"



#def EnableTouchSensor():
#	GPIO.add_event_detect(touchGPIO, GPIO.RISING, callback=button_pressed)
#	DumpActivity("Touch button enabled at " + GetTime(), color.cWhite)



# =============================	motion sensor	==================================
def SetMonitorStatus(status):
	if (IsMotionSensorAdded() != 1):
		return

	global gMonitorStatus
	gMonitorStatus = status


def PopMonitorStatus():
	if (IsMotionSensorAdded() != 1):
		return

	status = gMonitorStatus
	SetMonitorStatus("-")

	return status


def motion_detected(channel):
	if (IsMotionSensorAdded() != 1):
		return

	if CheckForGlitch(channel, 1):
		return

	status = "Motion Detected at " + GetTime()
	SetMonitorStatus(status)
	DumpActivity(status, color.cRed)

	MotionDetectionEffects()


def EnableMotionSensor(enable=1):
	if (IsMotionSensorAdded() != 1):
		return

	if (enable == 1):
		GPIO.add_event_detect(motionGPIO, GPIO.RISING, callback=motion_detected)
		DumpActivity("Motion detection enabled at " + GetTime(), color.cCyan)
	else:
		GPIO.remove_event_detect(motionGPIO)
		DumpActivity("Motion detection disabled at " + GetTime(), color.cPink)
		print ""

	SetEnableMotionSensor(enable)


def MotionDetectionEffects():
	if (IsMotionSensorAdded() != 1):
		return

	curDateTime = datetime.datetime.now()
	curSurvDir = GetSurvDir() + str(curDateTime.date())

	# create current date directory if doesn't exist
	if (os.path.isdir(curSurvDir) == 0):
		os.makedirs(curSurvDir)

	#thread.start_new_thread(TakeSnapshot, ())	# 6 sec
	thread.start_new_thread(TakeShortClip, ())	# 3 sec
	thread.start_new_thread(RecordAudio, ())	# 3 sec

	time.sleep(17)
