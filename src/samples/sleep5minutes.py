#!/usr/bin/python

# This script is for a computer (e.g. Raspberry Pi) attached to the
# smartplug. Running this script will shutdown the system, turn off the power
# in five minutes and turn it on again in another five minutes.
# This will reboot the system again. The programable plug therefore
# allows a sort of "Wake-on-RTC" for the Raspberry Pi.
#
# Note that you actually have to uncomment the line
#     #os.system("sudo shutdown now")
# which does the shutdown.
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

import os, sys
import argparse

sys.path.insert(0,os.path.join(os.path.dirname(__file__), ".."))
from ediplug import *

POWEROFF_DELAY     = 5  # delay in minutes from initiating shutdown to power off
POWEROFF_DURATION  = 5  # duration in minutes the system is shutdown

if __name__ == "__main__":
  # setup parser
  parser = \
      argparse.ArgumentParser(description='shutdown and sleep for 5 minutes')
  parser.add_argument('-n', '--net', nargs='?', const='', \
                    default='', help='network to search')
  parser.add_argument('-p', '--password',  nargs='?',\
                      const= '1234', default='1234', help='Password of plug')
  args = vars(parser.parse_args())
  
  try:
    # find plug in given network
    pf = PlugFinder(password=args['password'])
    if len(args['net']):
      plugs = pf.search(args['net'],maxCount=1)
    else:
      plugs = pf.search(maxCount=1)
    if len(plugs):
      plug = plugs.values()[0]
    else:
      print "no plugs found"
      sys.exit(3)
      
    # now define schedule
    now = TPoint.now()
    shutdownTime = now.createAfter(0,0,POWEROFF_DELAY)
    bootTime     = shutdownTime.createAfter(0,0,POWEROFF_DURATION)
    # bootTime = TPoint(TPoint.MON,8,0)   # reboot Monday 08:00

    # configure the plug (active==False between shutdownTime and bootTime)
    plug.setExclusiveState(shutdownTime,bootTime,False)

    # shutdown the system: uncomment to activate!
    #os.system("sudo shutdown now")

    # after reboot, don't forget to clear the schedule:
    # plug.clearSchedule()

  except Exception as e:
    print e
