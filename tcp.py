#!/usr/bin/python


# -*- Python -*-

#*****************************************************************
#
#        			 Copyright 2016 Hiranmoy Basak
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



import commands
import socket
import threading

from utils2 import *



Timer1sec = None



gHost = commands.getstatusoutput('hostname -I')[1]		# Server IP or Hostname, like 192.168.1.100 
gPort = 10001		# Pick an open Port (1000+ recommended), must match the client sport
gConnected = 0
gDataReceived = 0
gConnection = None



# ===================================	functions	================================
# forcefully kills the tcp connection/port
# resulting killing the whole program as well
def KillTcp():
	DumpActivity("Killed tcp at " + CurDateTimeStr(), color.cRed)
	command = "sudo fuser -k " + str(gPort) + "/tcp"
	os.system(command)


def StartTcp():
	global gDataReceived, gConnection

	bindFailed = 1
	while bindFailed:
		bindFailed = StartSocket()

		gConnection = None
		gDataReceived = 0

		# wait for 10 sec before trying a socket connection
		time.sleep(10)
		DumpActivity("Killing tcp connection after 10 sec of probable bind failed", color.cCyan)
		KillTcp()


def StartSocket():
	global gConnected, gDataReceived, gConnection
	gConnected = 0
	gConnection = None


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
	(gConnection, addr) = s.accept()
	DumpActivity("Connected", color.cWhite)
	gConnected = 1


	# start 1 sec timer thread
	timer1secThread = threading.Thread(target=Timer1sec)
	timer1secThread.start()


	# awaiting for message
	while True:
		try:
			tcpData = gConnection.recv(64)
		except:
			DumpActivity("Connection interrupted", color.cRed)
			CloseTcpConnection()
			return 1

		# split tcpData into key and data based '#' char
		# tcpData = <key>#<data>
		dataArr = tcpData.split('#')
		numData = dataArr.__len__()
		key = ""
		data = ""
		if (((numData % 2) != 1) or (numData < 3)):
			DumpActivity("Incorrect tcp data format : " + tcpData, color.cRed)
			CloseTcpConnection()
			return 1
		else:
			for idx in range(0, (numData - 2), 2):
				key = dataArr[idx]
				data = dataArr[idx + 1]

				# quit
				if (data == "quit"):
					gConnection.send("#" + key + "=Terminating~")
					CloseTcpConnection()
					return 0

				reply = GetTcpReply(data)

				if (len(reply) > 64):
					profileArr = reply.split(',')
					numReplies = profileArr.__len__()

					DumpActivity(str(numReplies) + " Messages are being sent back in response to: " + tcpData, color.cWhite)
					for idx in range(numReplies):
						partReply = profileArr[idx]
						success = SendTcpMessage(key, partReply, idx)
						if (success == 0):
							return 1

					DumpActivity(str(numReplies) + " Messages sent back in response to: " + tcpData, color.cWhite)
				else:
					success = SendTcpMessage(key, reply)
					if (success == 0):
							return 1

					DumpActivity("Message: " + reply + " sent back in response to: " + tcpData + " at " + CurDateTimeStr(), color.cCyan)

	return 1


def SendTcpMessage(key, reply, idx=-1):
	global gDataReceived

	# tcp reply	= #<key>=<reply>~
	# 			 or = #<key>=<packet index>|<part reply>~

	tcpReply = "#" + key + "="

	if (idx > 0):
		tcpReply = tcpReply + str(idx) + "|"

	tcpReply = tcpReply + reply + "~"

	try:
		gConnection.send(tcpReply)
		gDataReceived = 1

		if (key[0] == "-"):
			DumpActivity("Message: " + reply + " sent back (key):" + str(key) + " at " + CurDateTimeStr(), color.cWhite)
		return 1
	except:
		DumpActivity("Connection interrupted", color.cRed)
		CloseTcpConnection()
		return 0


def CloseTcpConnection():
	global gDataReceived, gConnected
	
	# Close connections
	gConnection.close()
	DumpActivity("Tcp connection terminated", color.cWhite)

	gConnected = 0
	gDataReceived = 0


def ConnectAndCloseConnection():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((gHost, gPort))
		s.close()
	except:
		DumpActivity("Unable to connect and close tcp", color.cRed)
		KillTcp()


def GetTcpReply(data):
	reply = "Unknown command"

	# return some data w.r.t a message

	if (data == "Handshake"):
		reply = "ok"

	elif (data == "IsConnected"):
		reply = "connected"

	elif (data == "Weather"):
		if IsSenseHatAdded():
			reply = str(gWeather.GetTemperature()) + "," + \
							str(gWeather.GetHumidity()) + "," + \
							str(gWeather.GetPressure())

	elif (data == "AirQuality"):
		if IsGasSensorAdded():
			reply = str(gAlcoholSensor.GetAlcoholReading()) + "," + \
							str(gCOSensor.GetCOReading()) + "," + \
							str(gSmokeSensor.GetSmokeReading())

	elif (data[0:21] == "GetTemperatureProfile"):
		if IsSenseHatAdded():
			reply = gWeather.GetTemperatureReadings(3, data[22:])

	elif (data[0:18] == "GetHumidityProfile"):
		if IsSenseHatAdded():
			reply = gWeather.GetHumidityReadings(3, data[19:])

	elif (data[0:18] == "GetPressureProfile"):
		if IsSenseHatAdded():
			reply = gWeather.GetPressureReadings(3, data[19:])

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
			reply = str(gMotionSensor.IsEnabled())

	elif (data == "GetIsDisableVideo"):
		if IsCameraAdded():
			reply = str(GetIsDisableVideo())

	elif (data == "GetIsDisableAudio"):
		if IsCameraAdded():
			reply = str(GetIsDisableAudio())

	elif (data == "CheckIfOnFluLight"):
		if (GetAddedLightings() == 2):
			reply = str(gFluLight.CheckIfOn())

	elif (data == "CheckIfOnPlug0"):
		if (GetAddedLightings() == 2):
			reply = str(gPlug0.CheckIfOn())

	elif (data == "CheckIfOnFan"):
		if (GetAddedLightings() == 1):
			reply = str(gFan.CheckIfOn())

	elif (data == "CheckIfOnBalconyLight"):
		if (GetAddedLightings() == 1):
			reply = str(gBalconyLight.CheckIfOn())

	elif (data == "CheckIfOnBulb0"):
		if (GetAddedLightings() == 1):
			reply = str(gBulb0.CheckIfOn())

	elif (data == "CheckIfOnPlug1"):
		if (GetAddedLightings() == 1):
			reply = str(gPlug1.CheckIfOn())

	elif (data == "SetupLEDFloodLight"):
		if (GetAddedLirc() == 1):
			gLEDFlood.SetupLEDFloodLight()
			reply = "on"

	elif (data == "SwitchOffLEDFloodLight"):
		if (GetAddedLirc() == 1):
			gLEDFlood.SetupLEDFloodLight(0)
			reply = "off"

	elif (data[0:13] == "ClickOnButton"):
		if (GetAddedLirc() == 1):
			ledKey = gLEDFlood.GetLEDKEYs(int(data[14:16]))
			gLEDFlood.SendIRSignal(ledKey)
			reply = "button " + data[14:16] + " pressed"

	elif (data[0:18] == "EnableMotionDetect"):
		if IsMotionSensorAdded():
			gMotionSensor.EnableSensor(int(data[19:20]))
			reply = str(gMotionSensor.IsEnabled())
			SaveSettings()

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
			gFan.SetPoweredOn(int(data[11:12]))
			reply = str(gFan.CheckIfOn())
			SaveSettings()

	elif (data[0:15] == "PowerOnFluLight"):
		if (GetAddedLightings() == 2):
			gFluLight.SetPoweredOn(int(data[16:17]))
			reply = str(gFluLight.CheckIfOn())
			SaveSettings()

	elif (data[0:12] == "PowerOnPlug0"):
		if (GetAddedLightings() == 2):
			gPlug0.SetPoweredOn(int(data[13:14]))
			reply = str(gPlug0.CheckIfOn())
			SaveSettings()

	elif (data[0:19] == "PowerOnBalconyLight"):
		if (GetAddedLightings() == 1):
			gBalconyLight.SetPoweredOn(int(data[20:21]))
			reply = str(gBalconyLight.CheckIfOn())
			SaveSettings()

	elif (data[0:12] == "PowerOnBulb0"):
		if (GetAddedLightings() == 1):
			gBulb0.SetPoweredOn(int(data[13:14]))
			reply = str(gBulb0.CheckIfOn())
			SaveSettings()

	elif (data[0:12] == "PowerOnPlug1"):
		if (GetAddedLightings() == 1):
			gPlug1.SetPoweredOn(int(data[13:14]))
			reply = str(gPlug1.CheckIfOn())
			SaveSettings()

	elif (data == "GetFluLightProfile"):
		if (GetAddedLightings() == 2):
			reply = gFluLight.GetSwitchedOnProfile()

	elif (data == "GetPlug0Profile"):
		if (GetAddedLightings() == 2):
			reply = gPlug0.GetSwitchedOnProfile()

	elif (data == "GetBalconyLightProfile"):
		if (GetAddedLightings() == 1):
			reply = gBalconyLight.GetSwitchedOnProfile()

	elif (data == "GetFanProfile"):
		if (GetAddedLightings() == 1):
			reply = gFan.GetSwitchedOnProfile()

	elif (data == "GetPlug1Profile"):
		if (GetAddedLightings() == 1):
			reply = gPlug1.GetSwitchedOnProfile()

	elif (data == "GetBulb0Profile"):
		if (GetAddedLightings() == 1):
			reply = gBulb0.GetSwitchedOnProfile()

	SaveSettings()
	SaveProfileOfAllAppliances()
	SaveProfileOfAllSensors()

	return reply


# ===================================	timer	===================================
def MonitorTcpConnection():
	global gDataReceived

	timeInSec = 0
	timeInMin = 0.0

	while(1):
		if IsExitTread():
			break

		time.sleep(1)
		timeInSec += 1

		if (timeInSec == 60):
			timeInSec = 0
			timeInMin += 1

			if IsDebugMode():
				# debug mode
				continue

			if gConnected:
				if (gDataReceived == 0) and (gConnection != None):
					DumpActivity("Killing tcp connection after not received any response from client for 2 min", color.cPink)
					KillTcp()

				gDataReceived = 0

			elif (timeInMin >= 10):
				DumpActivity("Starting new tcp connection after not connecting to any client for 10 min", color.cPink)
				ConnectAndCloseConnection()
				timeInMin = 0.0


def Timer1sec():
	while(1):
		if gExit:
			break

		if gConnected:
			if IsMotionSensorAdded():
				reply = gMotionSensor.GetLastTriggeredTime()

				if (reply != "-"):
					# motion sensor status key = -1
					success = SendTcpMessage("-1", reply)
					if (success == 0):
						return
					gMotionSensor.ClearTriggeredStatus()

			if (GetAddedTouchSensor() == gTouchSensor.GetId()):
				reply = gTouchSensor.GetLastTriggeredTime()

				if (reply != "-"):
					# touch sensor status key = -2
					success = SendTcpMessage("-2", reply)
					if (success == 0):
						return
					gTouchSensor.ClearTriggeredStatus()
		else:
			return

		time.sleep(1)
