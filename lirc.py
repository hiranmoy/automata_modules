#!/usr/bin/python


# -*- Visual basic -*-

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



from utils2 import *



gPowerOnLEDFloodLight = 0
gLEDLightCfg = "/home/pi/automation/LED_flood_light.conf"



# ===================================	functions	================================
def SetPowerLEDFloodLight(on=1):
	global gPowerOnLEDFloodLight

	if (IsLircAdded() != 1):
		return

	gPowerOnLEDFloodLight = on

	if on:
		GPIO.output(ledFloodGPIO, True)
	else:
		GPIO.output(ledFloodGPIO, False)


def SetupLEDLight():
	command = "sudo cp " + gLEDLightCfg + " /etc/lirc/lircd.conf; " + \
						"sudo /etc/init.d/lirc restart; " + \
						"sudo lircd -d /dev/lirc0"
	os.system(command)

	SetPowerLEDFloodLight()

	# wait for 1 sec
	time.sleep(1)

	# click on off button (3)
	ClickOnButton(3)

	DumpActivity("LED flood light setup done", color.cGreen)


def ClickOnButton(button):
	command = "irsend SEND_ONCE LED " + GetLEDKEYs(button)
	os.system(command)
	DumpActivity("LED key " + GetLEDKEYs(button) + " pressed", color.cWhite)

	return "button " + str(button) + " pressed"


# convert button index to button name
def GetLEDKEYs(button):
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
