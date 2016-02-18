#!/usr/bin/python

# Clear the schedule of the plug and set state to on or off.
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

import os, sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from ediplug import *

if __name__ == "__main__":
  # setup parser
  parser = \
      argparse.ArgumentParser(description='clear the schedule of the plug')
  parser.add_argument('-n', '--net', nargs='?', const='', \
                    default='', help='network to search')
  parser.add_argument('-p', '--password',  nargs='?',\
                      const= '1234', default='1234', help='Password of plug')
  parser.add_argument('-s', '--state', nargs='?', const='', \
                    default='', help='target state (on/off)')
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

    # now clear the state of the plug
    if len(args['state']) == 0:
      args['state'] = 'on'
    plug.clear(True if args['state'].lower() == 'on' else False)

  except Exception as e:
    print e
