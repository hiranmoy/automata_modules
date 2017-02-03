#!/usr/bin/python

import RPi.GPIO as GPIO



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# Motion sensor input (active high)
motionGPIO = 5
GPIO.setup(motionGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Touch sensor input (active high)
touchGPIO = 25
GPIO.setup(touchGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Bluetooth enable control (active high)
bluetoothGPIO = 16
GPIO.setup(bluetoothGPIO, GPIO.OUT)


# LED light control (active high)
lightGPIO = 20
GPIO.setup(lightGPIO, GPIO.OUT)


# Fluorescent light control (active high)
fluLightGPIO = 19
GPIO.setup(fluLightGPIO, GPIO.OUT)


# Plug0 control (active high)
plug0GPIO = 13
GPIO.setup(plug0GPIO, GPIO.OUT)


# Fan control (active high)
fanGPIO = 12
GPIO.setup(fanGPIO, GPIO.OUT)


# Balcony light control (active high)
balconyLightGPIO = 26
GPIO.setup(balconyLightGPIO, GPIO.OUT)


# Light bulb0 control (active high)
bulb0GPIO = 6
GPIO.setup(bulb0GPIO, GPIO.OUT)


# Plug1 control (active high)
plug1GPIO = 21
GPIO.setup(plug1GPIO, GPIO.OUT)



# clear all GPIOs
def ClearGPIO():
	GPIO.output(bluetoothGPIO, False)
	GPIO.output(lightGPIO, False)
	GPIO.output(fluLightGPIO, False)
	GPIO.output(plug0GPIO, False)
	GPIO.output(fanGPIO, False)
	GPIO.output(balconyLightGPIO, False)
	GPIO.output(bulb0GPIO, False)
	GPIO.output(plug1GPIO, False)
