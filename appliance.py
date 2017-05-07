#!/usr/bin/python


# -*- Python -*-

#*****************************************************************
#
#        			 Copyright 2017 Hiranmoy Basak
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


from sensors import *



gDataPointsPerDay = 24	# number of hours in one day



# ================================	Appliance class	===============================
class Appliance(AnalogSensor):
	def __init__(self, idx, gpio, name, watt):
		# initalize AnalogSensor class
		AnalogSensor.__init__(self, name)

		# appliane id, for now multiple appliance can have same id
		# -1 indicates special appliance like LIRC
		self.mId = idx

		# GPIO pin corresponding to this appliance
		self.mGPIO = gpio

		# switched on status
		self.mPoweredOn = 0

		# watt
		self.mWatt = watt


	def SetPoweredOnOnly(self, on=1):
		self.mPoweredOn = on

		# some devices are not controlled by GPIO
		if (self.mGPIO < 0):
			return

		if (self.mPoweredOn):
			GPIO.output(self.mGPIO, True)
		else:
			GPIO.output(self.mGPIO, False)


	# virtual
	def SetPoweredOn(self, on=1):
		if (GetAddedLightings() != self.mId):
			return

		self.SetPoweredOnOnly(on)


	def CheckIfOn(self):
		return self.mPoweredOn


	def SavePowerSettings(self, pPowerFile):
		pPowerFile.write("%20s : %s\n" % (self.mName, str(self.mPoweredOn)))


	# virtual
	def SaveProfile(self, pPowerFile, pSensorFile):
		if (GetAddedLightings() != self.mId):
			pPowerFile.write("\n")
			pSensorFile.write("\n")
			return

		self.SavePowerSettings(pPowerFile)
		self.SaveReadings(pSensorFile)


	def RestorePowerProfileOnly(self, lineInput):
		# remove first 23 characters
		data = lineInput[23:]

		# set power on status
		self.mPoweredOn = int(data[0:1])
		self.SetPoweredOn(self.mPoweredOn)


	# virtual
	def RestorePowerProfile(self, lineInput):
		if (GetAddedLightings() != self.mId):
			return

		self.RestorePowerProfileOnly(lineInput)


	# virtual
	def RestoreReadings(self, lineInput, month, day):
		if (GetAddedLightings() != self.mId):
			return

		AnalogSensor.RestoreReadings(self, lineInput, month, day)


	def SetApplianceReading(self):
		if (GetAddedLightings() != self.mId):
			return

		self.SetApplianceReadingOnly()


	def SetApplianceReadingOnly(self):
		curPowerUsage = 0.0
		if self.mPoweredOn:
			curPowerUsage = round(self.mWatt / 60.0, 2)

		# update alcohol reading
		curMinute = (datetime.datetime.now().hour * 60) + datetime.datetime.now().minute
		AnalogSensor.SetReadings(self, curMinute, curPowerUsage)
