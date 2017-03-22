#!/usr/bin/perl


# -*- Perl -*-

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



#use strict;
#use warnings;
use Time::HiRes;
use File::Copy;


sub main
{
	`touch /home/pi/automation/dump/end`;

	# search for automata processes
	my $process = `ps aux | \\grep "automata.py -" | head -1`;
	chomp $process;

	my @processStr = split(' ', $process);
	my $processId = $processStr[1];

	print "Killing process id:".$processId."\n";
	`kill -9 $processId`;
}

main;
