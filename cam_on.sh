#!/bin/bash

scriptProcessIdFile="/home/pi/automation/dump/cam_on_script.process"

mkdir -p "/tmp/stream"

raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0 &

#get raspistill process id
pid=$!

echo -n "raspistill process id: "
echo $pid
echo ""

# dump process id in a file
rm -f $scriptProcessIdFile
echo -n $pid > $scriptProcessIdFile
