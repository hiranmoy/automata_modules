#!/usr/bin/python

import commands
import socket
import threading

from sensors import *



gExit = 0
gHost = commands.getstatusoutput('hostname -I')[1]		# Server IP or Hostname, like 192.168.1.100 
gPort = 10001		# Pick an open Port (1000+ recommended), must match the client sport
gConnected = 0
gDataReceived = 0



# ===================================	functions	================================
def ExitThread(exit=1):
	global gExit
	gExit = exit


# forcefully kills the tcp connection/port
# resulting killing the whole program as well
def KillTcp():
	DumpActivity("Killed tcp", color.cRed)
	command = "sudo fuser -k " + str(gPort) + "/tcp"
	os.system(command)


def StartTcpThread():
	global gDataReceived

	bindFailed = 1
	while bindFailed:
		bindFailed = StartSocket()
		gDataReceived = 0

		# wait for 10 sec before trying a socket connection
		time.sleep(10)
		KillTcp()


def StartSocket():
	global gConnected, gDataReceived
	gConnected = 0

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	DumpActivity("Socket created", color.cWhite)

	# managing error exception
	try:
		s.bind((gHost, gPort))
	except socket.error:
		DumpActivity("Bind failed", color.cRed)
		return 1

	# wait for connections
	s.listen(5)
	DumpActivity("Socket awaiting messages", color.cWhite)
	(conn, addr) = s.accept()
	DumpActivity("Connected", color.cWhite)

	gConnected = 1
	quit = 0

	# awaiting for message
	while True:
		try:
			data = conn.recv(1024)
		except:
			DumpActivity("Connection interrupted", color.cRed)
			break
 
		gDataReceived = 1
		reply = "Unknown command"

		# return some data w.r.t a message
		if (data == "Handshake"):
			reply = "ok"

		elif (data == "ExtractMonitorStatus"):
			temp = PopMonitorStatus()
			reply = temp

		elif (data == "ToggleLED"):
			ToggleLED()
			reply = str(GetPowerOnLED())

		elif (data == "StartLiveFeed"):
			StartStreaming()
			reply = "on"

		elif (data == "StopLiveFeed"):
			EndStreaming()
			reply = "off"

		elif (data == "StartVideoRec"):
			StartVideoRecording()
			reply = "on"

		elif (data == "StopVideoRec"):
			EndVideoRecording()
			reply = "off"

		elif (data == "StartAudioRec"):
			StartAudioRecording()
			reply = "on"

		elif (data == "StopAudioRec"):
			EndAudioRecording()
			reply = "off"


		elif (data == "GetIsEnableMotionDetect"):
			reply = str(GetIsEnableMotionSensor())

		elif (data == "GetIsDisableVideo"):
			reply = str(GetIsDisableVideo())

		elif (data == "GetIsDisableAudio"):
			reply = str(GetIsDisableAudio())

		elif (data == "CheckIfOnFluLight"):
			reply = str(CheckIfOnFluLight())

		elif (data == "CheckIfOnPlug0"):
			reply = str(CheckIfOnPlug0())

		elif (data == "CheckIfOnFan"):
			reply = str(CheckIfOnFan())

		elif (data == "CheckIfOnBalconyLight"):
			reply = str(CheckIfOnBalconyLight())

		elif (data == "CheckIfOnBulb0"):
			reply = str(CheckIfOnBulb0())

		elif (data == "CheckIfOnPlug1"):
			reply = str(CheckIfOnPlug1())


		elif (data[0:18] == "EnableMotionDetect"):
			EnableMotionSensor(int(data[19:20]))
			reply = str(GetIsEnableMotionSensor())

		elif (data[0:12] == "DisableVideo"):
			SetDisableVideo(int(data[13:14]))
			reply = str(GetIsDisableVideo())

		elif (data[0:12] == "DisableAudio"):
			SetDisableAudio(int(data[13:14]))
			reply = str(GetIsDisableAudio())

		elif (data[0:10] == "PowerOnFan"):
			SwitchOnFan(int(data[11:12]))
			reply = str(CheckIfOnFan())

		elif (data[0:15] == "PowerOnFluLight"):
			SwitchOnFluLight(int(data[16:17]))
			reply = str(CheckIfOnFluLight())

		elif (data[0:12] == "PowerOnPlug0"):
			SwitchOnPlug0(int(data[13:14]))
			reply = str(CheckIfOnPlug0())

		elif (data[0:19] == "PowerOnBalconyLight"):
			SwitchOnBalconyLight(int(data[20:21]))
			reply = str(CheckIfOnBalconyLight())

		elif (data[0:12] == "PowerOnBulb0"):
			SwitchOnBulb0(int(data[13:14]))
			reply = str(CheckIfOnBulb0())

		elif (data[0:12] == "PowerOnPlug1"):
			SwitchOnPlug1(int(data[13:14]))
			reply = str(CheckIfOnPlug1())

		# quit
		elif (data == "quit"):
			conn.send("Terminating")
			quit = 1
			break


		try:
			conn.send(reply)
			DumpActivity("Message: " + reply + " sent back in response to: " + data, color.cCyan)
		except:
			DumpActivity("Connection interrupted", color.cRed)
			break


	# Close connections
	conn.close()
	DumpActivity("Tcp connection terminated", color.cWhite)

	gConnected = 0
	if quit:
		return 0

	return 1


def MonitorTcpConnection():
	global gDataReceived

	timeInSec = 0

	while(1):
		if gExit:
			break

		time.sleep(1)
		timeInSec += 1

		if (timeInSec == 30):
			timeInSec = 0

			if gConnected:
				if (gDataReceived == 0):
					KillTcp()

				gDataReceived = 0
