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


gAddMotionSensor = 0
gAddCamera = 0
gAddLightings = 0
gAddLirc = 0
gDebugMode = 0
gAddSenseHat = 0
gAddTouchSensor = 0
gAddGasSensor = 0



# ===================================	functions	================================
def AddMotionSensor(add=1):
	global gAddMotionSensor
	gAddMotionSensor = add


def IsMotionSensorAdded():
	return gAddMotionSensor


def AddCamera(add=1):
	global gAddCamera
	gAddCamera = add


def IsCameraAdded():
	return gAddCamera


def AddLightings(add):
	global gAddLightings
	gAddLightings = add


def GetAddedLightings():
	return gAddLightings


def AddLirc(add=1):
	global gAddLirc
	gAddLirc = add


def IsLircAdded():
	return gAddLirc


def IsDebugMode():
	return gDebugMode


def SetDebugMode(on=1):
	global gDebugMode
	gDebugMode = on


def AddSenseHat(add=1):
	global gAddSenseHat
	gAddSenseHat = add


def IsSenseHatAdded():
	return gAddSenseHat


def AddTouchSensor(add=1):
	global gAddTouchSensor
	gAddTouchSensor = add


def IsTouchSensorAdded():
	return gAddTouchSensor


def AddGasSensor(add=1):
	global gAddGasSensor
	gAddGasSensor = add


def IsGasSensorAdded():
	return gAddGasSensor
