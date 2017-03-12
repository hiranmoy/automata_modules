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


import thread

from sense_hat import SenseHat

#Read a value from analogue input 0
#in A/D in the PCF8591P @ address 0x48
from smbus import SMBus

from gpioSetup import *



# ================	digital GPIO rising edge triggered class	==================
class DigitalSensor():
	def __init__(self, gpio, name):
		# GPIO pin corresponding to this sensor
		self.mGPIO = gpio

		# set name
		self.mName = name

		# stores whether the sensor is enabled
		self.mEnabled = 0

		# stores when sensor was triggered last time
		self.mLastTriggeredTime = "-"


	def IsEnabled(self):
		return self.mEnabled


	def CheckForGlitch(self, channel, high):
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


	# virtual
	def ClearTriggeredStatus(self):
		self.mLastTriggeredTime = "-"


	#virtual
	def GetLastTriggeredTime(self):
		return self.mLastTriggeredTime


	#virtual
	def SensorTriggered(self, channel):
		if self.CheckForGlitch(channel, 1):
			return

		self.mLastTriggeredTime = GetTime()
		DumpActivity(self.mName + " sensor triggered ", color.cRed)


	#virtual
	def EnableSensor(self, enable=1):
		if (enable == 1):
			GPIO.add_event_detect(self.mGPIO, GPIO.RISING, callback=self.SensorTriggered)
			DumpActivity(self.mName + " enabled at " + GetTime(), color.cCyan)
		else:
			GPIO.remove_event_detect(self.mGPIO)
			DumpActivity(self.mName + " disabled at " + GetTime(), color.cPink)

		self.mEnabled = enable



# ===========================	touch sensor class	===============================
class TouchSensor(DigitalSensor):
	def __init__(self, idx, gpio, name):
		# initalize DigitalSensor class
		DigitalSensor.__init__(self, gpio, name)

		# touch sensor id
		self.mId = idx


	#virtual
	def EnableSensor(self, enable=1):
		if (GetAddedTouchSensor() != self.mId):
			return

		DigitalSensor.EnableSensor(self, enable)


	#virtual
	def SensorTriggered(self, channel):
		if (GetAddedTouchSensor() != self.mId):
			return

		DigitalSensor.SensorTriggered(self, channel)


	# virtual
	def ClearTriggeredStatus(self):
		if (GetAddedTouchSensor() != self.mId):
			return

		DigitalSensor.ClearTriggeredStatus(self)


	#virtual
	def GetLastTriggeredTime(self):
		if (GetAddedTouchSensor() != self.mId):
			return ""

		return DigitalSensor.GetLastTriggeredTime(self)




# ===========================	motion sensor class	==================================
class MotionSensor(DigitalSensor):
	def __init__(self, gpio, name):
		# initalize DigitalSensor class
		DigitalSensor.__init__(self, gpio, name)


	#virtual
	def EnableSensor(self, enable=1):
		if (IsMotionSensorAdded() != 1):
			return

		DigitalSensor.EnableSensor(self, enable)


	#virtual
	def SensorTriggered(self, channel):
		if (IsMotionSensorAdded() != 1):
			return

		DigitalSensor.SensorTriggered(self, channel)
		self.MotionDetectionEffects()


	# virtual
	def ClearTriggeredStatus(self):
		if (IsMotionSensorAdded() != 1):
			return

		DigitalSensor.ClearTriggeredStatus(self)


	#virtual
	def GetLastTriggeredTime(self):
		if (IsMotionSensorAdded() != 1):
			return ""

		return DigitalSensor.GetLastTriggeredTime(self)


	def MotionDetectionEffects(self):
		if (IsMotionSensorAdded() != 1):
			return

		curDateTime = datetime.datetime.now()
		curSurvDir = GetSurvDir() + str(curDateTime.date())

		# create current date directory if doesn't exist
		if (os.path.isdir(curSurvDir) == 0):
			os.makedirs(curSurvDir)

		#thread.start_new_thread(TakeSnapshot, ())						# 6 sec
		thread.start_new_thread(self.TakeShortClip, ())				# 3 sec
		thread.start_new_thread(self.RecordShortAudio, ())		# 3 sec

		time.sleep(17)


	def TakeShortClip(self):
		if (IsCameraAdded() != 1):
			return

		if (GetIsDisableVideo() == 1):
			return

		if IsCamBusy():
			return

		# command of taking 3 sec video clip
		command = "raspivid -o " + GetSurvDir() + CurDateStr() + "/"  + CurTimeStr() + ".h264 -t 3000"
		os.system(command)

		DumpActivity("Short clip captured", color.cYellow)


	def RecordShortAudio(self):
		if (IsCameraAdded() != 1):
			return

		if (GetIsDisableAudio() == 1):
			return

		if IsMicBusy():
			return

		# command of recording 3 sec audio clip
		command = "arecord -D hw:1,0 -r 48000 -d 3 -c 1 -f S16_LE " + \
							GetSurvDir() + CurDateStr() + "/"  + CurTimeStr() + ".wav"
		os.system(command)



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
	if (IsGasSensorAdded() != 1):
		return ""

	bus = SMBus(1)
	bus.write_byte(0x48, 3) # set control register to read channel 3
	reading = bus.read_byte(0x48) # read A/D
	return str(reading)


def GetCOReading():
	if (IsGasSensorAdded() != 1):
		return ""

	bus = SMBus(1)
	bus.write_byte(0x48, 2) # set control register to read channel 2
	reading = bus.read_byte(0x48) # read A/D
	return str(reading)


def GetSmokeReading():
	if (IsGasSensorAdded() != 1):
		return ""

	bus = SMBus(1)
	bus.write_byte(0x48, 1) # set control register to read channel 1
	reading = bus.read_byte(0x48) # read A/D
	return str(reading)
