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



from appliance import *



# =================================	Lirc class	=================================
class Lirc(Appliance):
	def __init__(self, lircIdx, gpio, name):
		# initalize Appliance class
		Appliance.__init__(self, -1, gpio, name)

		# lirc id
		self.mLircId = lircIdx

		# config file
		self.mConfig = GetAutomataDir() + self.mName + ".conf"


	# virtual
	def SetPoweredOn(self, on=1):
		if (GetAddedLirc() != self.mLircId):
			return

		self.SetPoweredOnOnly(on)


	# virtual
	def SaveProfile(self, pProfileFile):
		if (GetAddedLirc() != self.mLircId):
			pProfileFile.write("\n")
			return

		self.SaveProfileOnly(pProfileFile)


	# virtual
	def RestoreProfile(self, lineInput):
		if (GetAddedLirc() != self.mLircId):
			return

		self.RestoreProfileOnly(lineInput)


	def Setup(self, on):
		self.SetPoweredOn(on)

		if (on == 0):
			return

		command = "sudo cp " + self.mConfig + " /etc/lirc/lircd.conf; " + \
							"sudo /etc/init.d/lirc restart; " + \
							"sudo lircd -d /dev/lirc0"
		os.system(command)

		# wait for 1 sec
		time.sleep(1)


	def SendIRSignal(self, signalEnum):
		command = "irsend SEND_ONCE LED " + signalEnum
		os.system(command)
		DumpActivity("LED key " + signalEnum + " pressed", color.cWhite)




# ===========================	LED Flood Light class	===========================
class LEDFloodLight(Lirc):
	def __init__(self, lircIdx, gpio, name):
		# initalize Lirc class
		Lirc.__init__(self, lircIdx, gpio, name)
		

	def SetupLEDFloodLight(self, on=1):
		# basic setup
		self.Setup(on)

		# press on "off" button (3)
		self.SendIRSignal(self.GetLEDKEYs(3))

		DumpActivity("LED flood light setup done", color.cGreen)


	# convert button index to button name
	def GetLEDKEYs(self, button):
		# default on (ledButtons.c4)
		ledButton = ledButtons.c4

		if (button == 1):
			ledButton = ledButtons.c1
		elif (button == 2):
			ledButton = ledButtons.c2
		elif (button == 3):
			ledButton = ledButtons.c3
		elif (button == 4):
			ledButton = ledButtons.c4
		elif (button == 5):
			ledButton = ledButtons.c5
		elif (button == 6):
			ledButton = ledButtons.c6
		elif (button == 7):
			ledButton = ledButtons.c7
		elif (button == 8):
			ledButton = ledButtons.c8
		elif (button == 9):
			ledButton = ledButtons.c9
		elif (button == 10):
			ledButton = ledButtons.c10
		elif (button == 11):
			ledButton = ledButtons.c11
		elif (button == 12):
			ledButton = ledButtons.c12
		elif (button == 13):
			ledButton = ledButtons.c13
		elif (button == 14):
			ledButton = ledButtons.c14
		elif (button == 15):
			ledButton = ledButtons.c15
		elif (button == 16):
			ledButton = ledButtons.c16
		elif (button == 17):
			ledButton = ledButtons.c17
		elif (button == 18):
			ledButton = ledButtons.c18
		elif (button == 19):
			ledButton = ledButtons.c19
		elif (button == 20):
			ledButton = ledButtons.c20
		elif (button == 21):
			ledButton = ledButtons.c21
		elif (button == 22):
			ledButton = ledButtons.c22
		elif (button == 23):
			ledButton = ledButtons.c23
		elif (button == 24):
			ledButton = ledButtons.c24
		else:
			DumpActivity("incorrect LED button number, assuming default value", color.cRed)

		return ledButton.value
