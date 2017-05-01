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


	# virtual
	def SendIRSignal(self, signalStr):
		if (GetAddedLirc() != self.mLircModuleId):
			return

		# basic setup
		self.Setup(1)

		command = "irsend SEND_ONCE " + self.mIRName + " " + signalStr
		os.system(command)
		DumpActivity(self.mIRName + " key " + signalStr + " pressed", color.cWhite)



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
		             "KEY_CHANNELUP", "KEY_CHANNELDOWN", \
		             "KEY_S", "KEY_M"]


	# convert button index to button name
	def GetSpeakerKEYs(self, button):
		# default: aux (KEY_AUX)
		speakerButton = self.mArr[21]

		if (button < 33):
			speakerButton = self.mArr[button - 1]
		else:
			DumpActivity("incorrect speaker button number, assuming default value", color.cRed)

		return speakerButton



# ===========================	AC class	===========================
class AC(Lirc):
	def __init__(self, lircIdx, lircModuleIdx, gpio, name, config):
		# initalize Lirc class
		Lirc.__init__(self, lircIdx, lircModuleIdx, gpio, name, config)

		# ac setting
		self.mSetting = ""

		# ac on/off
		self.mPw = ["OFF", "ON"]

		# ac mode
		self.mMode = ["COOL", "DRY", "FAN"]

		# ac swing
		self.mSw = ["SWOFF", "SWON"]

		# ac turbo
		self.mTurbo = ["TURBOOFF", "TURBOON"]

	# get setting
	def GetSetting(self):
		return self.mSetting


	# set setting
	def SetSetting(self, setting):
		if (setting[0] == " "):
			DumpActivity("no ac setting", color.cCyan)

		self.mSetting = setting
		irKey = self.GetACKEYs(setting)
		self.SendIRSignal(irKey)


	# convert button index to button name
	def GetACKEYs(self, settings):
		# default: off (OFF)
		acButton = self.mPw[1]

		if (settings == "0"):
			self.mSetting = settings
			return self.mPw[0]
		elif (settings == "1"):
			self.mSetting = settings
			return self.mPw[1]
		else:
			settingsArr = settings.split('-')

			# 0: mode
			# 1: temperature
			# 2: fan speed
			# 3: swing
			# 4: turbo

			if (settingsArr.__len__() != 5):
				DumpActivity("incorrect ac setting format, assuming default value", color.cRed)
				return acButton

			if (settingsArr[0] == "0"):
				self.mSetting = settings
				return (self.mMode[int(settingsArr[0])] + "_" + \
								settingsArr[1] + "_" + \
								settingsArr[2] + "_" + \
								self.mSw[int(settingsArr[3])] + "_" + \
								self.mTurbo[int(settingsArr[4])])
			elif (settingsArr[0] == "1"):
				self.mSetting = settings
				return (self.mMode[int(settingsArr[0])] + "_" + \
								settingsArr[1] + "_" + \
								self.mSw[int(settingsArr[3])])
			elif (settingsArr[0] == "2"):
				self.mSetting = settings
				return (self.mMode[int(settingsArr[0])] + "_" + \
								settingsArr[2] + "_" + \
								self.mSw[int(settingsArr[3])])
			else:
				DumpActivity("incorrect ac mode, assuming default value", color.cRed)
				return acButton


	# virtual
	def SendIRSignal(self, signalStr):
		Lirc.SendIRSignal(self, signalStr)

		if (signalStr == "OFF"):
			Lirc.SetPoweredOn(self, 0)
		else:
			Lirc.SetPoweredOn(self, 1)
