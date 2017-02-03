#!/bin/bash

	onlineDate=$(wget http://www.timeapi.org/utc/in+five+hours?format=%25d%20%25b%20%25Y%20%25H:%25M:%25S -q -O -)

	echo "UTC+5hrs : "
	sudo date -s "$onlineDate"

	echo ""

	curDate=`date --date='1800 seconds'`

	echo "Time set to : ";
	sudo date -s "$curDate"
