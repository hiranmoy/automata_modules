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



import RPi.GPIO as GPIO

from utils import *



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

motionGPIO = 5
touchGPIO = 25
#bluetoothGPIO = 16
lightGPIO = 20
fluLightGPIO = 19
plug0GPIO = 13
fanGPIO = 12
balconyLightGPIO = 26
bulb0GPIO = 6
plug1GPIO = 21
ledFloodGPIO = 24



# ===================================	functions	================================
def SetupGPIOs():
	if IsMotionSensorAdded():
		# Motion sensor input (active high)
		GPIO.setup(motionGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


	if IsTouchSensorAdded():
		# Touch sensor input (active high)
		GPIO.setup(touchGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


	# Bluetooth enable control (active high)
	#GPIO.setup(bluetoothGPIO, GPIO.OUT)


	if (GetAddedLightings() == 1):
		# Fluorescent light control (active high)
		GPIO.setup(fluLightGPIO, GPIO.OUT)


		# Plug0 control (active high)
		GPIO.setup(plug0GPIO, GPIO.OUT)


		# Fan control (active high)
		GPIO.setup(fanGPIO, GPIO.OUT)


		# Balcony light control (active high)
		GPIO.setup(balconyLightGPIO, GPIO.OUT)


		# Light bulb0 control (active high)
		GPIO.setup(bulb0GPIO, GPIO.OUT)


		# Plug1 control (active high)
		GPIO.setup(plug1GPIO, GPIO.OUT)


	if (GetAddedLightings() == 2):
		# LED light control (active high)
		GPIO.setup(lightGPIO, GPIO.OUT)


	if IsLircAdded():
		# LED flood light
		GPIO.setup(ledFloodGPIO, GPIO.OUT)


# clear all GPIOs
def ClearGPIO():
	#GPIO.output(bluetoothGPIO, False)

	if (GetAddedLightings() == 1):
		GPIO.output(fluLightGPIO, False)
		GPIO.output(plug0GPIO, False)
		GPIO.output(fanGPIO, False)
		GPIO.output(balconyLightGPIO, False)
		GPIO.output(bulb0GPIO, False)
		GPIO.output(plug1GPIO, False)

	if (GetAddedLightings() == 2):
		GPIO.output(lightGPIO, False)

	if IsLircAdded():
		GPIO.output(ledFloodGPIO, False)
