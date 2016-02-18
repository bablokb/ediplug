#!/usr/bin/python

# Query and set powerstate of plug
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

import argparse
import os, sys

sys.path.insert(0,os.path.join(os.path.dirname(__file__), '..'))
from ediplug import *

if __name__ == '__main__':
  # setup parser
  parser = \
      argparse.ArgumentParser(description='Query and optionally set powerstate')
  parser.add_argument('-p', '--password',  nargs='?',\
                      const= '1234', default='1234', help='Password of plug')
  parser.add_argument('-s', '--state', nargs='?', const='', \
                    default='', help='target state (on/off)')
  args = vars(parser.parse_args())

  # process arguments
  try:
    pf = PlugFinder(password=args['password'])
    plug = pf.search(maxCount=1).values()[0]
    if args['state'] <> "":
      plug.setPowerState(True if args['state'].lower() == 'on' else False)
    print 'Currently active: %s' % plug.getPowerState()
  except Exception as e:
    print e
