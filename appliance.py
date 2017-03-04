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

from gpioSetup import *


gPowerLogFile = "/home/pi/automation/power.log"



# ===================================	class	===================================
class Appliance:

	def __init__(self, gpio):
		# GPIO pin corresponding to this appliance
		self.mGPIO = gpio

		# switched on status
		self.mPoweredOn = 0


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



# ===================================	functions	================================
