#!/bin/bash

scriptProcessIdFile="/home/pi/automation/dump/audio_rec_on_script.process"
arecord -D hw:1,0 -r 48000 -d 99999 -c 1 -f S16_LE "$1" &

#get raspistill process id
pid=$!

echo -n "raspivid process id: "
echo $pid
echo ""

# dump process id in a file
rm -f $scriptProcessIdFile
echo -n $pid > $scriptProcessIdFile
