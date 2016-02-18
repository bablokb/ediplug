#!/usr/bin/python

# Class definition of SP1101W
#
# This class implements the behaviour for the Edimax SP1101W plug.
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

__author__ = "Bernhard Bablok, https://github.com/bablokb"

from Plug import Plug as Plug

class SP1101W(Plug):
  """Implement behaviour of the  Edimax SP1101W Plug"""

  # initialize Plug object   -------------------------------------------------

  def __init__(self,ip,port=10000,user='admin',password='1234'):
    super(SP1101W,self).__init__(ip,port,user,password)

