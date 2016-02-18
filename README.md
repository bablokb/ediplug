Python Library for Edimax Smartplugs
====================================

Introduction
------------

This library allows to control all aspects of the Edimax Smartplugs
SP1101W and SP2101W using Python and without access to the cloud of
the manufacturer.


Prerequisites
-------------

The code was developed for Python2. You need the following additional
packages:

  - minidom
  - netifaces
  - netaddr
  - requests
  - socket

Either install the packages using `pip` or the package-management of your
distribution.


Installation
------------

Copy the directory `src/ediplug` to a directory which is on your python search
path for packages (something like `/usr/local/lib/python2.7/site-packages`).
In your code, use

    from ediplug import *

You can find some annotated samples in the directory `src/samples`.


Usage
-----

Since the plugs use DHCP to get their own IP-address, you would typically
use the class `PlugFinder` to search for the plug on your network. As an
alternative, you could also instantiate and object of the class `SP1101W`
or `SP2101W` directly.

PlugFinder supports various methods to optimize the search:

    pf = PlugFinder(password='1234')
    plugs = pf.search()
    plugs = pf.search(network='192.168.1.0/24',maxCount=1)
    plugs = pf.search(network='192.168.1.100-192.168.1.120',\
                      plugnames=['plug1','plug2'])

The first line instantiates the `PlugFinder`. Note that all your plugs
need the same password. The second line searches the whole local network
for all plugs. The version in the third line specifies a subnet and
stops the search after a single plug is found. The last version
specifies an IP-range (e.g. the range of your DHCP-server) and a list
of plugs (identified by their names) to be found. Here, the search
stops when all specified plugs were found. Of course you can combine
the various options (e.g. if you specify `plugnames` and `maxCount` the
search will only find plugs with the given name up to the given count).

PlugFinder returns a map, keyed by plugname. You can access a plug by
name, e.g.

    plug = plugs['plug1']

or value:

    plug = plugs.values()[0]    # use the "first" plug

Once you have the plug-object, you use it to control the plug, e.g.
to query or set the powerstate:

    print plug.getPowerState()
    plug.setPowerState(True)                # turn the power on
    plug.setPowerState(False)               # and off again

or to query and set the schedule:

    onTime = TPoint.now()
    offTime = TPoint(onTime.day,24,00)
    plug.setState(onTime,offTime)


PlugFinder
----------

This class searches for plugs within the net. It provides the following
methods:

  - `PlugFinder(user='admin',password='1234',port=10000)`: constructor
  - `create(host)`: returns a `Plug`-object for the given host or IP
  - `search(network=None,plugnames=None,maxCount=254)`: returns a map of plugs


TPoint
------

This class implements a point in time within the weekly schedule. This is
a triple of (day,hour,minute). The day is encoded in ISO-weekday format, i.e.
Sunday is 0, Monday is 1 and so on.

Methods:

  - `TPoint(day,hour,minute)`: constructor
  - `TPoint.now()`: static method, returns a TPoint for "now"
  - `day`, `hour`, 'minute': getter and setters for day, hour, minute
  - `createAfter(days,hours,minutes)`: create a TPoint which is the given
    days, hours, minutes later than this object 
  - `add(day,hour,minute)`: adds the given days, hours, minutes to the
    current object. The method returns `self` to allow method chaining.


Schedule
--------

This is a list with a value of `1` or `0` for every minute within the
weekly schedule. Note that this is an internal data-structure which
you typically don't manipulate directly.


Plug
----

Base class of the model-specific classes `SP1101W` and `SP2101W`. The class
implements all common methods. This is the main interface for the
communikcation with the physical plug.

Methods:

  - `Plug(ip,port=10000,user='admin',password='1234')`: constructor
  - `getUrl()`: returns the URL of this plug
  - `getNameAndType()`: returns the tuple (name,type)
  - `getSysInfo()`: returns a map with system-information
  - `getPowerState()`: returns the current power state (True if "on")
  - `setPowerState(active=True)`: set the current power state (pass True for "on")
  - `getSchedule(schedule=None)`: returns low-level data-structure
  - `setSchedule(schedule,day=None)`: set schedule (only for the given day)
  - `setState(start,end,active=True)`: set state from `start` to `end`
  - `setExclusiveState(start,end,active=True)`: set state from `start` to `end`
    to `active` and the rest of the time to `not active`.
  - `clear(active=True)`: clear the schedule in the plug (to "on" or "off")


SP1101W
-------

This is a subclass of `Plug` without any additional methods.


SP2101W
-------

This subclass of `Plug` for the Edimax SP2101W implements the additional
method

  - `getPowerInfo()`: return a map with infos regarding power-consumption.

