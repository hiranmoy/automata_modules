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


from gpioSetup import *



gDataPointsPerDay = 24	# number of hours in one day



# ================================	Appliance class	===============================
class Appliance():
	def __init__(self, idx, gpio, name):
		# appliane id, for now multiple appliance can have same id
		# -1 indicates special appliance like LIRC
		self.mId = idx

		# GPIO pin corresponding to this appliance
		self.mGPIO = gpio

		# set name
		self.mName = name

		# switched on status
		self.mPoweredOn = 0

		# initialize switched on info
		self.mPower = []
		for idx in range(gDataPointsPerDay):
			self.mPower.append(0)


	def SetPoweredOnOnly(self, on=1):
		self.mPoweredOn = on

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


	def GetSwitchedOnProfile(self):
		profileStr = ""

		for idx in range(gDataPointsPerDay):
			if (idx > 0):
				profileStr = profileStr + ","

			profileStr = profileStr + str(self.mPower[idx])

		return profileStr


	def UpdateSwitchedProfile(self):
		if (GetAddedLightings() != self.mId and -1):
			return

		if self.mPoweredOn:
			self.mPower[datetime.datetime.now().hour] += 1


	def SaveProfileOnly(self, pProfileFile):
		pProfileFile.write("%20s : %s : %s\n" % (self.mName, str(self.mPoweredOn), self.GetSwitchedOnProfile()))


	# virtual
	def SaveProfile(self, pProfileFile):
		if (GetAddedLightings() != self.mId):
			pProfileFile.write("\n")
			return

		self.SaveProfileOnly(pProfileFile)


	def RestoreProfileOnly(self, lineInput):
		# remove first 23 characters
		data = lineInput[23:]

		# set power on status
		self.mPoweredOn = int(data[0:1])
		self.SetPoweredOn(self.mPoweredOn)

		# remove 3 more characters
		data = data[3:]

		profileArr = data.split(',')
		numHrs = profileArr.__len__()

		if (numHrs != gDataPointsPerDay):
			DumpActivity("Invalid power info for " + self.mName, color.cRed)
			return

		for idx in range(gDataPointsPerDay):
			self.mPower[idx] = int(profileArr[idx])


	# virtual
	def RestoreProfile(self, lineInput):
		if (GetAddedLightings() != self.mId):
			return

		self.RestoreProfileOnly(lineInput)
