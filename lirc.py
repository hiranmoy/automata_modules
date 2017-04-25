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
	def __init__(self, lircIdx, gpio, name, config):
		# initalize Appliance class
		Appliance.__init__(self, -1, gpio, name)

		# lirc id
		self.mLircId = lircIdx

		# Lirc name
		self.mIRName = name

		# config file
		self.mConfig = GetAutomataDir() + config + ".conf"


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
		if (GetAddedLirc() != self.mLircId):
			return

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
		if (GetAddedLirc() != self.mLircId):
			return

		command = "irsend SEND_ONCE " + self.mIRName + " " + signalEnum
		os.system(command)
		DumpActivity(self.mIRName + " key " + signalEnum + " pressed", color.cWhite)



# ===========================	LED Flood Light class	===========================
class LEDFloodLight(Lirc):
	def __init__(self, lircIdx, gpio, name, config):
		# initalize Lirc class
		Lirc.__init__(self, lircIdx, gpio, name, config)
		

	def SetupLEDFloodLight(self, on=1):
		if (GetAddedLirc() != self.mLircId):
			return

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



# ===========================	Speaker class	===========================
class Speaker(Lirc):
	def __init__(self, lircIdx, gpio, name, config):
		# initalize Lirc class
		Lirc.__init__(self, lircIdx, gpio, name, config)
		

	def SetupSpeaker(self, on=1):
		if (GetAddedLirc() != self.mLircId):
			return

		# basic setup
		self.Setup(on)

		DumpActivity("Speaker setup done", color.cGreen)


	# convert button index to button name
	def GetSpeakerKEYs(self, button):
		# default on (speakerButtons.cAux)
		speakerButton = speakerButtons.cAux

		if (button == 1):
			speakerButton = speakerButtons.cPw
		elif (button == 2):
			speakerButton = speakerButtons.cMute
		elif (button == 3):
			speakerButton = speakerButtons.c1
		elif (button == 4):
			speakerButton = speakerButtons.c2
		elif (button == 5):
			speakerButton = speakerButtons.c3
		elif (button == 6):
			speakerButton = speakerButtons.c4
		elif (button == 7):
			speakerButton = speakerButtons.c5
		elif (button == 8):
			speakerButton = speakerButtons.c6
		elif (button == 9):
			speakerButton = speakerButtons.c7
		elif (button == 10):
			speakerButton = speakerButtons.c8
		elif (button == 11):
			speakerButton = speakerButtons.c9
		elif (button == 12):
			speakerButton = speakerButtons.c0
		elif (button == 13):
			speakerButton = speakerButtons.cLight
		elif (button == 14):
			speakerButton = speakerButtons.cReset
		elif (button == 15):
			speakerButton = speakerButtons.cBt
		elif (button == 16):
			speakerButton = speakerButtons.cUsb
		elif (button == 17):
			speakerButton = speakerButtons.cUp
		elif (button == 18):
			speakerButton = speakerButtons.cDown
		elif (button == 19):
			speakerButton = speakerButtons.cVolUp
		elif (button == 20):
			speakerButton = speakerButtons.cVolDn
		elif (button == 21):
			speakerButton = speakerButtons.cEn
		elif (button == 22):
			speakerButton = speakerButtons.cAux
		elif (button == 23):
			speakerButton = speakerButtons.cRd
		elif (button == 24):
			speakerButton = speakerButtons.cBack
		elif (button == 25):
			speakerButton = speakerButtons.cFwd
		elif (button == 26):
			speakerButton = speakerButtons.cPlPs
		elif (button == 27):
			speakerButton = speakerButtons.cTnUp
		elif (button == 28):
			speakerButton = speakerButtons.cTnDn
		elif (button == 29):
			speakerButton = speakerButtons.cChUp
		elif (button == 30):
			speakerButton = speakerButtons.cChDn
		elif (button == 31):
			speakerButton = speakerButtons.cScan
		elif (button == 32):
			speakerButton = speakerButtons.cMem
		else:
			DumpActivity("incorrect speaker button number, assuming default value", color.cRed)

		return speakerButton.value
