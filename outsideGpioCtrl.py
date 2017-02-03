#!/usr/bin/python

import RPi.GPIO as GPIO
import sys


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


channel = sys.argv[1]
state = sys.argv[2]

GPIO.setup(int(channel), GPIO.OUT)

if state == "1":
	GPIO.output(int(channel), True)
else:
	GPIO.output(int(channel), False)
