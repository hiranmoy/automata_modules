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



import os
import time
import datetime

from gpioSetup import *



# ===================================	class	===================================
class Appliance:

	def __init__(self, gpio, name):
		# GPIO pin corresponding to this appliance
		self.mGPIO = gpio

		# set name
		self.mName = name

		# switched on status
		self.mPoweredOn = 0

		# initialize switched on info
		self.mProfile = []
		for idx in range(24):
			self.mProfile.append(0)


	def SetPoweredOn(self, on=1):
		if (GetAddedLightings() != 1):
			return

		self.mPoweredOn = on

		if (self.mPoweredOn):
			GPIO.output(self.mGPIO, True)
		else:
			GPIO.output(self.mGPIO, False)


	def CheckIfOn(self):
		return self.mPoweredOn


	def GetSwitchedOnProfile(self):
		profileStr = ""

		for idx in range(24):
			if (idx > 0):
				profileStr = profileStr + ","

			profileStr = profileStr + str(self.mProfile[idx])

		return profileStr


	def UpdateSwitchedProfile(self):
		if (GetAddedLightings() != 1):
			return

		if self.mPoweredOn:
			self.mProfile[datetime.datetime.now().hour] += 1


	def SaveProfle(self, pProfileFile):
		pProfileFile.write("%20s : %s\n" % (self.mName, self.GetSwitchedOnProfile()))


	def RestoreProfle(self, lineInput):
		if (GetAddedLightings() != 1):
			return

		data = lineInput[23:]

		profileArr = data.split(',')
		numHrs = profileArr.__len__()

		if (numHrs != 24):
			print color.cCyan.value + "Invalid power info for " + self.mName + color.cEnd.value
			return

		for idx in range(24):
			self.mProfile[idx] = int(profileArr[idx])
