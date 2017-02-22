#!/usr/bin/python

import thread

from sense_hat import SenseHat

#Read a value from analogue input 0
#in A/D in the PCF8591P @ address 0x48
from smbus import SMBus

from utils2 import *



gTouchButtonPressed = 0
gMonitorStatus = "-"



# =============================	touch sensor	==================================
def SetTouchButtonPressed(pressed=1):
	if (IsTouchSensorAdded() != 1):
		return

	global gTouchButtonPressed
	gTouchButtonPressed = pressed


def IsTouchButtonPressed():
	if (IsTouchSensorAdded() != 1):
		return 0

	return gTouchButtonPressed


def button_pressed(channel):
	if (IsTouchSensorAdded() != 1):
		return

	if CheckForGlitch(channel, 1):
		return

	status = "Touch button pressed at " + GetTime()
	DumpActivity(status, color.cGreen)

	SetTouchButtonPressed()


def EnableTouchSensor():
	if (IsTouchSensorAdded() != 1):
		return

	GPIO.add_event_detect(touchGPIO, GPIO.RISING, callback=button_pressed)
	DumpActivity("Touch button enabled at " + GetTime(), color.cYellow)



# =============================	motion sensor	==================================
def SetMonitorStatus(status):
	if (IsMotionSensorAdded() != 1):
		return

	global gMonitorStatus
	gMonitorStatus = status


def PopMonitorStatus():
	if (IsMotionSensorAdded() != 1):
		return ""

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



# ==================== temperature, humidity, air pressure sensor	==============
def ClearSenseHat():
	if (IsSenseHatAdded() != 1):
		return

	sense = SenseHat()
	sense.clear()


def GetTemperature():
	if (IsSenseHatAdded() != 1):
		return ""

	sense = SenseHat()
	temperature = str(sense.get_temperature())
	return temperature[0:5]


def GetHumidity():
	if (IsSenseHatAdded() != 1):
		return ""

	sense = SenseHat()
	humidity = str(sense.get_humidity())
	return humidity[0:5]


def GetPressure():
	if (IsSenseHatAdded() != 1):
		return ""

	sense = SenseHat()
	pressure = str(sense.get_pressure())
	return pressure[0:6]



# ==============================	gas sensor	==================================
def GetAlcoholReading():
	bus = SMBus(1)
	bus.write_byte(0x48, 0) # set control register to read channel 0
	reading = bus.read_byte(0x48) # read A/D
	return str(reading)


def GetCOReading():
	bus = SMBus(1)
	bus.write_byte(0x48, 1) # set control register to read channel 1
	reading = bus.read_byte(0x48) # read A/D
	return str(reading)
