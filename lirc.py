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


# id of the enabled lirc
gLircsEnabled = -1



# =================================	Lirc class	=================================
class Lirc(Appliance):
	def __init__(self, lircIdx, lircModuleIdx, gpio, name, config):
		# initalize Appliance class
		Appliance.__init__(self, -1, gpio, name)

		# lirc id
		self.mLircId = lircIdx

		# lirc module id
		self.mLircModuleId = lircModuleIdx

		# Lirc name
		self.mIRName = name

		# config file
		self.mConfig = GetAutomataDir() + config + ".conf"


	# virtual
	def SetPoweredOn(self, on=1):
		if (GetAddedLirc() != self.mLircModuleId):
			return

		self.SetPoweredOnOnly(on)


	# virtual
	def SaveProfile(self, pProfileFile):
		if (GetAddedLirc() != self.mLircModuleId):
			pProfileFile.write("\n")
			return

		self.SaveProfileOnly(pProfileFile)


	# virtual
	def RestoreProfile(self, lineInput):
		if (GetAddedLirc() != self.mLircModuleId):
			return

		self.RestoreProfileOnly(lineInput)


	def Setup(self, on):
		global gLircsEnabled

		if (GetAddedLirc() != self.mLircModuleId):
			return

		self.SetPoweredOn(on)

		if (on == 0):
			return


		if (self.mLircId != gLircsEnabled):
			command = "sudo cp " + self.mConfig + " /etc/lirc/lircd.conf; " + \
								"sudo /etc/init.d/lirc stop; " + \
								"sudo /etc/init.d/lirc start; " + \
								"sudo lircd -d /dev/lirc0"
			os.system(command)

			# wait for 1 sec
			#time.sleep(1)

			gLircsEnabled = self.mLircId


	def SendIRSignal(self, signalEnum):
		if (GetAddedLirc() != self.mLircModuleId):
			return

		# basic setup
		self.Setup(1)

		command = "irsend SEND_ONCE " + self.mIRName + " " + signalEnum
		os.system(command)
		DumpActivity(self.mIRName + " key " + signalEnum + " pressed", color.cWhite)



# ===========================	LED Flood Light class	===========================
class LEDFloodLight(Lirc):
	def __init__(self, lircIdx, lircModuleIdx, gpio, name, config):
		# initalize Lirc class
		Lirc.__init__(self, lircIdx, lircModuleIdx, gpio, name, config)

		# ir keys for LED buttons
		self.mArr = ["KEY_A", "KEY_B", "KEY_C", "KEY_D", \
		             "KEY_E", "KEY_F", "KEY_G", "KEY_H", \
		             "KEY_I", "KEY_J", "KEY_K", "KEY_L", \
		             "KEY_M", "KEY_N", "KEY_O", "KEY_P", \
		             "KEY_Q", "KEY_R", "KEY_S", "KEY_T", \
		             "KEY_U", "KEY_V", "KEY_W", "KEY_X"]


	# virtual
	def RestoreProfile(self, lineInput):
		if (GetAddedLirc() != self.mLircModuleId):
			return

		self.RestoreProfileOnly(lineInput)

		if self.CheckIfOn():
			# press on "off" button (3) if switched on
			self.SendIRSignal(self.GetLEDKEYs(3))
	

	# convert button index to button name
	def GetLEDKEYs(self, button):
		# default: off (KEY_C)
		ledButton = self.mArr[2]

		if (button < 24):
			ledButton = self.mArr[button - 1]
		else:
			DumpActivity("incorrect LED button number, assuming default value", color.cRed)

		return ledButton



# ===========================	Speaker class	===========================
class Speaker(Lirc):
	def __init__(self, lircIdx, lircModuleIdx, gpio, name, config):
		# initalize Lirc class
		Lirc.__init__(self, lircIdx, lircModuleIdx, gpio, name, config)

		# ir keys for speaker buttons
		self.mArr = ["KEY_POWER", "KEY_MUTE", \
		             "KEY_1", "KEY_2", "KEY_3", "KEY_4", "KEY_5", "KEY_6", "KEY_7", "KEY_8", "KEY_9", "KEY_0", \
		             "KEY_L", "KEY_R", "KEY_BLUETOOTH", "KEY_U", \
		             "KEY_UP", "KEY_DOWN", "KEY_VOLUMEUP", "KEY_VOLUMEDOWN", "KEY_ENTER", \
		             "KEY_AUX", "KEY_RADIO", \
		             "KEY_BACK", "KEY_FORWARD", "KEY_PLAYPAUSE", \
		             "BTN_TL", "BTN_TL2", \
		             "KEY_CHANNELUP", "KEY_CHANNELDOWN" \
		             "KEY_S", "KEY_M"]
		

	def SetupSpeaker(self, on=1):
		if (GetAddedLirc() != self.mLircModuleId):
			return

		# basic setup
		self.Setup(on)

		DumpActivity("Speaker setup done", color.cGreen)


	# convert button index to button name
	def GetSpeakerKEYs(self, button):
		# default: aux (KEY_AUX)
		speakerButton = self.mArr[21]

		if (button < 32):
			speakerButton = self.mArr[button - 1]
		else:
			DumpActivity("incorrect speaker button number, assuming default value", color.cRed)

		return speakerButton



# ===========================	AC class	===========================
class AC(Lirc):
	def __init__(self, lircIdx, lircModuleIdx, gpio, name, config):
		# initalize Lirc class
		Lirc.__init__(self, lircIdx, lircModuleIdx, gpio, name, config)

		# ir keys for ac buttons
		self.mArr = ["ON", "OFF" \
		             "FAN_1_SWOFF", "FAN_2_SWOFF", "FAN_3_SWOFF", \
		             "FAN_1_SWON", "FAN_2_SWON", "FAN_3_SWON", \
		             "DRY_16_SWOFF", "DRY_17_SWOFF", "DRY_18_SWOFF", "DRY_19_SWOFF", "DRY_20_SWOFF", \
		             "DRY_21_SWOFF", "DRY_22_SWOFF", "DRY_23_SWOFF", "DRY_24_SWOFF", "DRY_25_SWOFF", \
		             "DRY_26_SWOFF", "DRY_27_SWOFF", "DRY_28_SWOFF", "DRY_29_SWOFF", "DRY_30_SWOFF", \
		             "DRY_16_SWON", "DRY_17_SWON", "DRY_18_SWON", "DRY_19_SWON", "DRY_20_SWON", \
		             "DRY_21_SWON", "DRY_22_SWON", "DRY_23_SWON", "DRY_24_SWON", "DRY_25_SWON", \
		             "DRY_26_SWON", "DRY_27_SWON", "DRY_28_SWON", "DRY_29_SWON", "DRY_30_SWON"]


	def SetupAC(self, on=1):
		if (GetAddedLirc() != self.mLircModuleId):
			return

		# basic setup
		self.Setup(on)

		DumpActivity("AC setup done", color.cGreen)


	# convert button index to button name
	def GetACKEYs(self, button):
		# default: on (ON)
		acButton = self.mArr[0]

		if (button < 38):
			acButton = self.mArr[button - 1]
		else:
			DumpActivity("incorrect ac button number, assuming default value", color.cRed)

		return acButton
