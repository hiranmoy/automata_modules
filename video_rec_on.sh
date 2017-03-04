#!/bin/bash


# -*- Visual basic -*-

#*****************************************************************
#
#        Copyright 2017 Hiranmoy Basak
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
