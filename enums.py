#!/usr/bin/python

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
