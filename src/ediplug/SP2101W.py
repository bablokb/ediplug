#!/usr/bin/python

# Class definition of SP2101W
#
# This class implements the behaviour for the Edimax SP2101W plug.
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

__author__ = "Bernhard Bablok, https://github.com/bablokb"

from Plug import Plug as Plug

class SP2101W(Plug):
  """Implement behaviour of the  Edimax SP2101W Plug"""

  # initialize Plug object   -------------------------------------------------

  def __init__(self,ip,port=10000,user='admin',password='1234'):
    super(SP2101W,self).__init__(ip,port,user,password)

  # query power-info   ------------------------------------------------------

  def getPowerInfo(self):
    
    dom = self._execCommand('get',"NOW_POWER")
    info = {}
    tags = dom.getElementsByTagName("NOW_POWER")[0].childNodes
    for tag in tags:
      if tag.hasChildNodes():
        info[tag.tagName] = tag.firstChild.nodeValue
    return info
