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
