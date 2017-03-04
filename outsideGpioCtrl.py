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
