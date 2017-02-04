#!/usr/bin/python

gAddMotionSensor = 0
gAddCamera = 0
gAddLightings = 0



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
