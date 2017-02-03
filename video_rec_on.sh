#!/bin/bash

scriptProcessIdFile="/home/pi/automation/dump/video_rec_on_script.process"
raspivid -o "$1" -t 99999999 &

#get raspistill process id
pid=$!

echo -n "raspivid process id: "
echo $pid
echo ""

# dump process id in a file
rm -f $scriptProcessIdFile
echo -n $pid > $scriptProcessIdFile
