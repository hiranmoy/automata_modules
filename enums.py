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
