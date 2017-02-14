#!/usr/bin/python

gAddMotionSensor = 0
gAddCamera = 0
gAddLightings = 0
gAddLirc = 0
gDebugMode = 0
gAddSenseHat = 0



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
