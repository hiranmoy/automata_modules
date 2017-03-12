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



gDataPointsPerDay = 1024	# number of minutes in one day



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



# ============================ analog sensor class	============================
class AnalogSensor():
	def __init__(self, name):
		# set name
		self.mName = name

		# stores sensor data
		self.mReading = []
		for idx in range(gDataPointsPerDay):
			self.mReading.append(0.0)


	def GetReadings(self):
		profileStr = ""

		for idx in range(gDataPointsPerDay):
			if (idx > 0):
				profileStr = profileStr + ","

			profileStr = profileStr + str(self.mReading[idx])

		return profileStr


	def GetReading(self, minute):
		return self.mReading[minute]


	def SetReadings(self, minute, reading):
		self.mReading[minute] = reading


	def SaveReadings(self, pProfileFile):
		pProfileFile.write("%20s : %s\n" % (self.mName, self.GetReadings()))


	def RestoreReadings(self, lineInput):
		# remove first 23 characters
		data = lineInput[23:]

		profileArr = data.split(',')
		numMins = profileArr.__len__()

		if (numMins != gDataPointsPerDay):
			DumpActivity("Invalid sensor reading for " + self.mName, color.cRed)
			return

		for idx in range(gDataPointsPerDay):
			self.mReading[idx] = float(profileArr[idx])



# ================================== weather class	============================
class Weather():
	def __init__(self, name):
		# set name
		self.mName = name

		self.mTemperature = AnalogSensor("Temperature")
		self.mHumidity = AnalogSensor("Humidity")
		self.mPressure = AnalogSensor("Pressure")


	def GetTemperature(self):
		if (IsSenseHatAdded() != 1):
			return ""

		curMinute = datetime.datetime.now().minute
		curTemperature = self.mTemperature.GetReading(curMinute)

		# temperature already set
		if curTemperature:
			return curTemperature

		self.SetTemperature()
		return self.mTemperature.GetReading(curMinute)


	def SetTemperature(self):
		if (IsSenseHatAdded() != 1):
			return

		# calculate temperature
		sense = SenseHat()
		curTemperature = str(sense.get_temperature())

		# take only first 5 digits
		curTemperature = curTemperature[0:5]

		# update temperature
		self.mTemperature.SetReadings(datetime.datetime.now().minute, curTemperature)


	def GetHumidity(self):
		if (IsSenseHatAdded() != 1):
			return ""

		curMinute = datetime.datetime.now().minute
		curHumidity = self.mHumidity.GetReading(curMinute)

		# humidity already set
		if curHumidity:
			return curHumidity

		self.SetHumidity()
		return self.mHumidity.GetReading(curMinute)


	def SetHumidity(self):
		if (IsSenseHatAdded() != 1):
			return

		# calculate humidity
		sense = SenseHat()
		curHumidity = str(sense.get_humidity())

		# take only first 5 digits
		curHumidity = curHumidity[0:5]

		# update humidity
		self.mHumidity.SetReadings(datetime.datetime.now().minute, curHumidity)


	def GetPressure(self):
		if (IsSenseHatAdded() != 1):
			return ""

		curMinute = datetime.datetime.now().minute
		curPressure = self.mPressure.GetReading(curMinute)

		# pressure already set
		if curPressure:
			return curPressure

		self.SetPressure()
		return self.mPressure.GetReading(curMinute)


	def SetPressure(self):
		if (IsSenseHatAdded() != 1):
			return

		# calculate pressure
		sense = SenseHat()
		curPressure = str(sense.get_pressure())

		# take only first 6 digits
		curPressure = curPressure[0:6]

		# update pressure
		self.mPressure.SetReadings(datetime.datetime.now().minute, curPressure)


	def UpdateReadings(self):
		if (IsSenseHatAdded() != 1):
			return

		self.SetTemperature()
		self.SetHumidity()
		self.SetPressure()


	def SaveReadings(self, pProfileFile):
		if (IsSenseHatAdded() != 1):
			pProfileFile.write("\n\n\n")

		self.mTemperature.SaveReadings(pProfileFile)
		self.mHumidity.SaveReadings(pProfileFile)
		self.mPressure.SaveReadings(pProfileFile)


	def RestoreReadings(self, idx, lineInput):
		if (idx == 1):
			self.mTemperature.RestoreReadings(lineInput)
		if (idx == 2):
			self.mHumidity.RestoreReadings(lineInput)
		if (idx == 3):
			self.mPressure.RestoreReadings(lineInput)



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
