#!/bin/bash

scriptProcessIdFile="/home/pi/automation/dump/stream_script.process"

LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www" &

#get raspistill process id
pid=$!

echo -n "mjpg streamer process id: "
echo $pid
echo ""

# dump process id in a file
rm -f $scriptProcessIdFile
echo -n $pid > $scriptProcessIdFile
