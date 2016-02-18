#!/usr/bin/python

# Print the system information from the plug
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

def print_sysinfo(plug):
  info = plug.getSysInfo()
  print "plug: %s" % plug.getUrl()
  for key in info.keys():
    print "  %s: %s" % (key,info[key])

if __name__ == "__main__":
  # setup parser
  parser = \
      argparse.ArgumentParser(description='print system info of the plug')
  parser.add_argument('-n', '--net', nargs='?', const='', \
                    default='', help='network to search')
  parser.add_argument('-p', '--password',  nargs='?',\
                      const= '1234', default='1234', help='Password of plug')
  args = vars(parser.parse_args())
  
  try:
    # find plugs in given network
    pf = PlugFinder(password=args['password'])
    if len(args['net']):
      plugs = pf.search(args['net'])
    else:
      plugs = pf.search()
    if len(plugs) == 0:
      print "no plugs found"
      sys.exit(3)

    # query system-information and print it
    for plug in plugs.values():
      print_sysinfo(plug)
      
  except Exception as e:
    print e
