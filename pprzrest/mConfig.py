# -*- coding: utf8 -*-

#Configuration File

import os

SERVER_PATH = "/sw/ground_segment/tmtc/server "
LINK_PATH = "/sw/ground_segment/tmtc/link "
APP_SERVER_PATH = "/sw/ground_segment/tmtc/app_server "
# Full path for anthenna tracker..   /home/pprz/DEV/BeagleBone/ant_TR/ant_TR_pwm_cleaning
# TRACKER_PATH = "<full_path_to_tracker_backend>/ant_tr -v "
TRACKER_PATH = "/home/pprz/DEV/BeagleBone/ant_TR/ant_TR_pwm_cleaning/ant_tr_pwm -v "

#Get PAPARAZZI_HOME path
PAPARAZZI_PATH = os.getenv('PAPARAZZI_HOME')
if PAPARAZZI_PATH is None:
	#if no environment variable 
	PAPARAZZI_PATH = "/home/pprz/DEV/paparazzi"

#Get PAPARAZZI_SRC path
PAPARAZZI_SRC = os.getenv('PAPARAZZI_SRC')
if PAPARAZZI_SRC is None:
	os.environ["PAPARAZZI_SRC"] = PAPARAZZI_PATH

IVY_BUS = "192.168.4.255"
#IVY_BUS = ""

#Default parameters to run agents
DEF_LINK_PARAM = "-d /dev/ttyO2 -transport xbee -s 57600"
DEF_SERVER_PARAM = ""
DEF_APP_SERVER_PARAM = "-v -utcp"
DEF_TRACKER_PARAM =" -v -b " + IVY_BUS

#Run agents on app start
RUN_AGENTS = True
#Run process monitor on app start
RUN_PROCESS_MONITOR = True
RUN_LINK = True
RUN_APP_SERVER = True
RUN_SERVER = True
RUN_TRACKER = True





