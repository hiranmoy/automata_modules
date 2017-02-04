#!/usr/bin/python

import RPi.GPIO as GPIO

from utils import *



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

motionGPIO = 5
#touchGPIO = 25
bluetoothGPIO = 16
lightGPIO = 20
fluLightGPIO = 19
plug0GPIO = 13
fanGPIO = 12
balconyLightGPIO = 26
bulb0GPIO = 6
plug1GPIO = 21



# ===================================	functions	================================
def SetupGPIOs():
	if IsMotionSensorAdded():
		# Motion sensor input (active high)
		GPIO.setup(motionGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


	# Touch sensor input (active high)
	#GPIO.setup(touchGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


	# Bluetooth enable control (active high)
	#GPIO.setup(bluetoothGPIO, GPIO.OUT)


	if (GetAddedLightings() == 1):
		# LED light control (active high)
		GPIO.setup(lightGPIO, GPIO.OUT)


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



# clear all GPIOs
def ClearGPIO():
	#GPIO.output(bluetoothGPIO, False)

	if (GetAddedLightings() == 1):
		GPIO.output(lightGPIO, False)
		GPIO.output(fluLightGPIO, False)
		GPIO.output(plug0GPIO, False)
		GPIO.output(fanGPIO, False)
		GPIO.output(balconyLightGPIO, False)
		GPIO.output(bulb0GPIO, False)
		GPIO.output(plug1GPIO, False)
