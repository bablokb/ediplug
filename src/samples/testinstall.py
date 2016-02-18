#!/usr/bin/python

# Test correct installation of ediplug. This program just instantiates
# various obects of the classes provided by ediplug.
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

try:
    from ediplug import *

    # define some timepoints
    on = TPoint.now()
    off = on.createAfter(0,2,0)
    print "on: %s" % on
    print "off: %s" % off

    # define a schedule and print it
    sched = Schedule(active=False)
    sched.setState(on,off,active=True)
    sched.setState(on.add(0,3,0),off.add(0,3,0),active=True)

    for (tp,val) in  sched.getSwitchList(on.day):
        print "%s: %s" % (tp, 'ON' if val=='1' else 'OFF')

    # create a PlugFinder
    finder = PlugFinder(password='1234')

    # create a Plug
    plug = SP1101W('foo')
    print plug

    # print OK
    print "installation seems to be fine!"
except Exception as e:
    print e
    print "Oops, something is wrong!"

