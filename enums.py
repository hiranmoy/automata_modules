#!/usr/bin/python


# -*- Python -*-

#*****************************************************************
#
#        Copyright 2016 Hiranmoy Basak
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



from enum import Enum



# ASCII escape char
class color(Enum):
	cRed = '\x1b[6;30;41m'
	cGreen = '\x1b[6;30;42m'
	cYellow = '\x1b[6;30;43m'
	cBlue = '\x1b[6;30;44m'
	cPink = '\x1b[6;30;45m'
	cCyan = '\x1b[6;30;46m'
	cWhite = '\x1b[6;30;47m'
	cEnd = '\x1b[0m'


# LED flood light buttons
class ledButtons(Enum):
	c1 = "KEY_A"
	c2 = "KEY_B"
	c3 = "KEY_C"
	c4 = "KEY_D"

	c5 = "KEY_E"
	c6 = "KEY_F"
	c7 = "KEY_G"
	c8 = "KEY_H"

	c9 = "KEY_I"
	c10 = "KEY_J"
	c11 = "KEY_K"
	c12 = "KEY_L"

	c13 = "KEY_M"
	c14 = "KEY_N"
	c15 = "KEY_O"
	c16 = "KEY_P"

	c17 = "KEY_Q"
	c18 = "KEY_R"
	c19 = "KEY_S"
	c20 = "KEY_T"

	c21 = "KEY_U"
	c22 = "KEY_V"
	c23 = "KEY_W"
	c24 = "KEY_X"


# Speaker buttons
class speakerButtons(Enum):
	cPw = "KEY_POWER"
	cMute = "KEY_MUTE"

 	c1 = "KEY_1"
	c2 = "KEY_2"
	c3 = "KEY_3"
	c4 = "KEY_4"
	c5 = "KEY_5"
	c6 = "KEY_6"
	c7 = "KEY_7"
	c8 = "KEY_8"
	c9 = "KEY_9"
	c0 = "KEY_0"

	cLight = "KEY_L"
 	cReset = "KEY_R"
 	cBt = "KEY_BLUETOOTH"
 	cUsb = "KEY_U"

 	cUp = "KEY_UP"
	cDown = "KEY_DOWN"
 	cVolUp = "KEY_VOLUMEUP"
	cVolDn = "KEY_VOLUMEDOWN"
	cEn = "KEY_ENTER"

	cAux = "KEY_AUX"
	cRd = "KEY_RADIO"

	cBack = "KEY_BACK"
	cFwd = "KEY_FORWARD"
	cPlPs = "KEY_PLAYPAUSE"

	cTnUp = "BTN_TL"
	cTnDn = "BTN_TL2"

	cChUp = "KEY_CHANNELUP"
	cChDn = "KEY_CHANNELDOWN"

	cScan = "KEY_S"
	cMem = "KEY_M"
