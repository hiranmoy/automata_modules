#!/usr/bin/python

import commands
import socket
import threading

from sensors import *
from lirc import *



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
	DumpActivity("Killed tcp at " + CurDateTimeStr(), color.cRed)
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
		DumpActivity("Killing tcp connection after 10 sec of probable bind failed", color.cCyan)
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
 
		reply = "Unknown command"

		gDataReceived = 1

		# return some data w.r.t a message
		if (data == "Handshake"):
			reply = "ok"

		if (data == "IsConnected"):
			reply = "connected"

		elif (data == "Weather"):
			if IsSenseHatAdded():
				reply = GetTemperature() + "," + GetHumidity() + "," + GetPressure()

		elif (data == "AirQuality"):
			if IsGasSensorAdded():
				reply = GetAlcoholReading() + "," + GetCOReading() + "," + GetSmokeReading()

		elif (data == "ExtractMonitorStatus"):
			if IsMotionSensorAdded():
				temp = PopMonitorStatus()
				reply = temp

		elif (data == "ExtractTouchSensorStatus"):
			if IsTouchSensorAdded():
				reply = str(IsTouchButtonPressed())
				SetTouchButtonPressed(0)
				
		elif (data == "ToggleLED"):
			if (GetAddedLightings() == 2):
				ToggleLED()
				reply = str(GetPowerOnLED())

		elif (data == "StartLiveFeed"):
			if IsCameraAdded():
				StartStreaming()
				reply = "on"

		elif (data == "StopLiveFeed"):
			if IsCameraAdded():
				EndStreaming()
				reply = "off"

		elif (data == "StartVideoRec"):
			if IsCameraAdded():
				StartVideoRecording()
				reply = "on"

		elif (data == "StopVideoRec"):
			if IsCameraAdded():
				EndVideoRecording()
				reply = "off"

		elif (data == "StartAudioRec"):
			if IsCameraAdded():
				StartAudioRecording()
				reply = "on"

		elif (data == "StopAudioRec"):
			if IsCameraAdded():
				EndAudioRecording()
				reply = "off"

		elif (data == "GetIsEnableMotionDetect"):
			if IsMotionSensorAdded():
				reply = str(GetIsEnableMotionSensor())

		elif (data == "GetIsDisableVideo"):
			if IsCameraAdded():
				reply = str(GetIsDisableVideo())

		elif (data == "GetIsDisableAudio"):
			if IsCameraAdded():
				reply = str(GetIsDisableAudio())

		elif (data == "CheckIfOnFluLight"):
			if (GetAddedLightings() == 1):
				reply = str(CheckIfOnFluLight())

		elif (data == "CheckIfOnPlug0"):
			if (GetAddedLightings() == 1):
				reply = str(CheckIfOnPlug0())

		elif (data == "CheckIfOnFan"):
			if (GetAddedLightings() == 1):
				reply = str(CheckIfOnFan())

		elif (data == "CheckIfOnBalconyLight"):
			if (GetAddedLightings() == 1):
				reply = str(CheckIfOnBalconyLight())

		elif (data == "CheckIfOnBulb0"):
			if (GetAddedLightings() == 1):
				reply = str(CheckIfOnBulb0())

		elif (data == "CheckIfOnPlug1"):
			if (GetAddedLightings() == 1):
				reply = str(CheckIfOnPlug1())

		elif (data == "SetupLEDFloodLight"):
			if IsLircAdded():
				SetupLEDLight()
				reply = "on"

		elif (data == "SwitchOffLEDFloodLight"):
			if IsLircAdded():
				SetPowerLEDFloodLight(0)
				reply = "off"

		elif (data[0:13] == "ClickOnButton"):
			if IsLircAdded():
				reply = ClickOnButton(int(data[14:16]))

		elif (data[0:18] == "EnableMotionDetect"):
			if IsMotionSensorAdded():
				EnableMotionSensor(int(data[19:20]))
				reply = str(GetIsEnableMotionSensor())

		elif (data[0:12] == "DisableVideo"):
			if IsCameraAdded():
				SetDisableVideo(int(data[13:14]))
				reply = str(GetIsDisableVideo())

		elif (data[0:12] == "DisableAudio"):
			if IsCameraAdded():
				SetDisableAudio(int(data[13:14]))
				reply = str(GetIsDisableAudio())

		elif (data[0:10] == "PowerOnFan"):
			if (GetAddedLightings() == 1):
				SwitchOnFan(int(data[11:12]))
				reply = str(CheckIfOnFan())

		elif (data[0:15] == "PowerOnFluLight"):
			if (GetAddedLightings() == 1):
				SwitchOnFluLight(int(data[16:17]))
				reply = str(CheckIfOnFluLight())

		elif (data[0:12] == "PowerOnPlug0"):
			if (GetAddedLightings() == 1):
				SwitchOnPlug0(int(data[13:14]))
				reply = str(CheckIfOnPlug0())

		elif (data[0:19] == "PowerOnBalconyLight"):
			if (GetAddedLightings() == 1):
				SwitchOnBalconyLight(int(data[20:21]))
				reply = str(CheckIfOnBalconyLight())

		elif (data[0:12] == "PowerOnBulb0"):
			if (GetAddedLightings() == 1):
				SwitchOnBulb0(int(data[13:14]))
				reply = str(CheckIfOnBulb0())

		elif (data[0:12] == "PowerOnPlug1"):
			if (GetAddedLightings() == 1):
				SwitchOnPlug1(int(data[13:14]))
				reply = str(CheckIfOnPlug1())


		# quit
		elif (data == "quit"):
			conn.send("Terminating")
			quit = 1
			break


		try:
			conn.send(reply)
			DumpActivity("Message: " + reply + " sent back in response to: " + data + " at " + CurDateTimeStr(), color.cCyan)
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

			# unset touch button pressed status
			SetTouchButtonPressed(0)

			if (IsDebugMode() == 0):
			# debug mode
				continue

			if gConnected:
				if (gDataReceived == 0):
					DumpActivity("Killing tcp connection after not received any response from client for 1 min", color.cCyan)
					KillTcp()

				gDataReceived = 0
