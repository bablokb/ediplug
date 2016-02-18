#!/usr/bin/python

# Class definition of PlugFinder
#
# PlugFinder is a factory-method and creates instances of subclasses of Plug.
# It's methods either try to find a specific plug, or plugs within the
# given network.
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

__author__ = "Bernhard Bablok, https://github.com/bablokb"

import sys
import socket
import netifaces
import netaddr
from Plug import Plug as Plug
from SP1101W import SP1101W as SP1101W
from SP2101W import SP2101W as SP2101W

class PlugFinder(object):
  """Search for Plugs in the network"""

  # get IP range of current network   ----------------------------------------

  @staticmethod
  def _getcidr():
    for iface in netifaces.interfaces():
      try:
        val = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
        if val['addr'] == '127.0.0.1':
          continue
        cidr = "%s/%s" % (val['addr'],val['netmask'])
        return netaddr.IPNetwork(cidr)
      except Exception as e:
        pass
    
  # initialize PlugFinder object   -------------------------------------------

  def __init__(self,user='admin',password='1234',port=10000):
    self.__user     = user
    self.__password = password
    self.__port     = port
    
  # check a given address/port combination if is available   -----------------

  def __check(self,host):
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(0.05)
      s.connect((host,self.__port))
      s.close()
      return True
    except Exception as e:
      #print e
      return False

  # add a plug to to the dictionary of all available plugs   -----------------

  def __add(self,plugs,plugnames,ip):
    # query the name of the plug
    plug = Plug(ip,self.__port,self.__user,self.__password)
    name, type = plug.getNameAndType()
    if plugnames is None or name in plugnames:
      constructor = globals()[type]
      plugs[name] = constructor(ip,self.__port,self.__user,self.__password)

  # Create a Plug-instance for a specific address (Host or IP)   -------------
  
  def create(self,host):
    plugs = {}
    plugnames = None
    if self.__check(host):
      self.__add(plugs,plugnames,host)
    return plugs.values()[0]

  # Search for all Plugs within the given network   --------------------------

  def search(self,network=None,plugnames=None,maxCount=254):
    plugs = {}
    # resolv network argument to a netaddr.IPNetwork
    if network is None:
      # autodetect network
      iplist = [ip for ip in PlugFinder._getcidr().iter_hosts() ]
    elif network.find('-') > -1:
      network = network.split('-')
      iplist = [ ip for ip in netaddr.IPRange(network[0],network[1]) ]
    else:
      try:
        iplist = [ ip for ip in netaddr.IPNetwork(network).iter_hosts() ]
      except netaddr.AddrFormatError as afe:
        # assume network is a single hostname
        iplist = [ network ]
      
    for ip in iplist:
      if self.__check(str(ip)):
        self.__add(plugs,plugnames,str(ip))
        if (plugnames is not None and len(plugnames) == len(plugs)) \
                                                   or len(plugs) == maxCount:
          # all requested plugs are already found, so return
          return plugs
    # ok, all IPs have been checked, so return all plugs found
    return plugs

# test   ---------------------------------------------------------------------

if __name__ == "__main__":
  """pass network and password as arguments"""
  if len(sys.argv) < 3:
    print "pass network and password as arguments"
  else:
    pf = PlugFinder(password=sys.argv[2])
    plug = pf.search(sys.argv[1],maxCount=1).values()[0]
    name, type = plug.getNameAndType()
    print "Name: %s\nType: %s\nURL:  %s\n" % (name, type, plug.getUrl())
    plugInfo = plug.getSysInfo()
    for key in plugInfo.keys():
      print "%s: %s" % (key,plugInfo[key])
