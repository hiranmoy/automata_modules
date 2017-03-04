#!/usr/bin/perl


# -*- Visual basic -*-

#*****************************************************************
#
#        Copyright 2017 Hiranmoy Basak
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


# global variables
$dumpArea = "/home/pi/automation/dump/";
$endFile = $dumpArea."end";
$scriptProcessIdFile = $dumpArea."crash_check_script.process";


# returns process id of the automata python program
sub GetProcessId()
{
	my $processFile = `ls $dumpArea*.pid`;
	chomp $processFile;

	my $processId = "1";
	if (-e $processFile)
	{
		$processId = `cat $processFile`;
		chomp $processId;
	}

	return $processId;
}


sub main
{
	# dump process id in a file
	my $scriptProcessId = "$$";
	print "\nCrash check script process id: ".$scriptProcessId."\n\n";
	if (-f $scriptProcessIdFile)
	{
		unlink $scriptProcessIdFile;
	}
	`echo -n $scriptProcessId > $scriptProcessIdFile`;


	# get automata python program
	my $processId = GetProcessId();


	while (1)
	{
		# exit if end file exists
		if (-e $endFile)
		{
			print "Exited";
			exit(0);
		}

		# check if the python program is running
		my $checkIfRunning = `ps $processId | grep -c "automata\.py"`;
		chomp $checkIfRunning;
		if ($checkIfRunning ne "1")
		{
			# sleep for 1 sec
			Time::HiRes::sleep(1);

			print "process $processId may not be running\n";

			# exit if end file exists
			if (-e $endFile)
			{
				print "Exited";
				exit(0);
			}

			print "\nRestarting ...\n\n";

			my $args = `cat "/home/pi/automation/arg.txt"`;
			chomp $args;
			print "/home/pi/automation/automata.py $args &\n";

			`/home/pi/automation/automata.py $args &`;

			print "Restarted and exited";
			exit(0);
		}

		#print ".1 sec timer\n";
		Time::HiRes::sleep(.1);
	}
}

main;
