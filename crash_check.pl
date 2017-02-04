#!/usr/bin/perl

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
			`/home/pi/automation/automata.py -addMotionSensor -addCamera -addLightings 1 &`;
			print "Restarted and exited";
			exit(0);
		}

		#print ".1 sec timer\n";
		Time::HiRes::sleep(.1);
	}
}

main;
