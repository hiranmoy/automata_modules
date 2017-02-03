#!/bin/bash

# clear gpio outputs
`/home/pi/automation/outsideGpioCtrl.py 16 0`
`/home/pi/automation/outsideGpioCtrl.py 20 0`
`/home/pi/automation/outsideGpioCtrl.py 19 0`
`/home/pi/automation/outsideGpioCtrl.py 13 0`
`/home/pi/automation/outsideGpioCtrl.py 6 0`

sleep 60


# set up IST
/home/pi/automation/setDateTime.sh

createVNC="0"

if [ ! -f "$HOME/.vnc/raspberrypi:1.pid" ]
then
	createVNC="1"
	echo "vnc pid file doesn't exist"
else
	vncPid=`cat $HOME/.vnc/raspberrypi:1.pid`
	vncrunning=`ps $vncPid | grep vnc | grep -c geometry`

	if [ $vncrunning -ne "1" ]
	then
		echo "vnc process is not running"
		createVNC="1"
	fi
fi

if [ $createVNC -eq "1" ]
then
	echo "creating vnc"

	rm -rf $HOME/.vnc
	rm -rf /tmp/.X1-lock
	rm -rf /tmp/.X11-unix/X1

	mkdir -p $HOME/.vnc
	cp $HOME/automation/vnc_passwd $HOME/.vnc/passwd

	vncserver -geometry 1900x1000 :1
fi

export DISPLAY=':1'
echo "Display = "$DISPLAY
/home/pi/automation/automata.py
