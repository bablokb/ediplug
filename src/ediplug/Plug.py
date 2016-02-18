#!/usr/bin/python

# Class definition of Plug
#
# Plug is the base class of SP1101W or SP2101W (the plugs currently supported
# by this library). It contains some common methods
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

__author__ = "Bernhard Bablok, https://github.com/bablokb"

import sys
import os
import requests as req
from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parseString

from Schedule import Schedule as Schedule
from TPoint import TPoint as TPoint

class Plug(object):
  """Base class of supported Edimax Plugs"""

  # initialize Plug object   -------------------------------------------------

  def __init__(self,ip,port=10000,user='admin',password='1234'):
    self.__url = 'http://%s:%s/smartplug.cgi' % (ip,port)
    self.__cred = (user,password)
    self.__info = None
    self.__debug = True if os.getenv('DEBUG') is not None else False

    if self.__debug:
      sys.stderr.write("url: %s\n" % self.__url)

  # string representation of plug   -------------------------------------------
  
  def __str__(self):
    return "Plugtype: %s" % type(self)

  # technical representation of plug   ----------------------------------------
  
  def __repr__(self):
    return "Type: %s\nURL: %s" % (type(self),self.__url)
    
  # create XML command document   --------------------------------------------
  
  def _getXML(self,cmdType):
    doc = getDOMImplementation().createDocument(None, "SMARTPLUG", None)
    doc.documentElement.setAttribute("id", "edimax")
    
    cmdElem = doc.createElement("CMD")
    cmdElem.setAttribute("id", cmdType)
    doc.documentElement.appendChild(cmdElem)
    return (doc,cmdElem)

  # post request and return DOM   ---------------------------------------------
  
  def _postCmd(self,doc):
    if self.__debug:
      sys.stderr.write(doc.toprettyxml())
      
    res = req.post(self.__url, auth=self.__cred, files={'file': doc.toxml()})
    if self.__debug:
      print res
    if res.status_code == req.codes.ok:
      result = parseString(res.text)
      if self.__debug:
        sys.stderr.write(result.toprettyxml())
      return result
    else:
      # TODO: throw some exception??
      pass

  # execute generic command   ------------------------------------------------

  def _execCommand(self,cmdType,tag,value=None):
    doc, cmdElem = self._getXML(cmdType)
    childElem = doc.createElement(tag)
    cmdElem.appendChild(childElem)
    if value is not None:
      childElem.appendChild(doc.createTextNode(value))
    return self._postCmd(doc)

  # return url of plug   ------------------------------------------------------

  def getUrl(self):
    return self.__url
  
  # parse result of command   -------------------------------------------------

  def _parseResult(self,dom):
    value = dom.getElementsByTagName("CMD")[0].firstChild.nodeValue
    return True if value == 'OK' else False
    
  # query name and type of plug   --------------------------------------------

  def getNameAndType(self):
    info = self.getSysInfo()
    return (info['Device.System.Name'],info['Run.Model'])

  # query system-info   ------------------------------------------------------

  def getSysInfo(self):
    if self.__info is not None:
      return self.__info
    
    dom = self._execCommand('get',"SYSTEM_INFO")
    info = {}
    tags = dom.getElementsByTagName("SYSTEM_INFO")[0].childNodes
    for tag in tags:
      if tag.tagName == "SUPPORT":
        for supportTag in tag.childNodes:
          info[supportTag.tagName] = supportTag.firstChild.nodeValue
      else:
        if tag.hasChildNodes():
          info[tag.tagName] = tag.firstChild.nodeValue
    self.__info = info
    return info

  # query power-state   ------------------------------------------------------

  def getPowerState(self):
    dom = self._execCommand('get',"Device.System.Power.State")
    value = dom.getElementsByTagName("Device.System.Power.State")[0].\
                                                          firstChild.nodeValue
    return True if value == 'ON' else False

  # set power-state   ---------------------------------------------------------

  def setPowerState(self,active=True):
    value = 'ON' if active else 'OFF'
    dom = self._execCommand('setup',"Device.System.Power.State",value)
    return self._parseResult(dom)

  # query schedule   ----------------------------------------------------------

  def getSchedule(self,schedule=None,getDom=False):
    if schedule is None:
      schedule = Schedule()
    days = [ i for i in range(7) ]

    # build command-xml ...
    doc, cmdElem = self._getXML('get')
    schedElem = doc.createElement("SCHEDULE")
    cmdElem.appendChild(schedElem)
    
    if not getDom:      # return full information
      for d in days:
        dayElem = doc.createElement("Device.System.Power.Schedule."+str(d))
        schedElem.appendChild(dayElem)

    # ... post and parse the result
    dom = self._postCmd(doc)
    if getDom:
      return dom
    
    tags = dom.getElementsByTagName("SCHEDULE")[0].childNodes
    for tag in tags:
      name = tag.tagName
      if name.find('List') > 0:
        continue
      day = name.split('.')[-1]
      value = tag.firstChild.nodeValue
      schedule.fromTransport(value,int(day))
    return schedule

  # set schedule (for a given day)   ------------------------------------------

  def setSchedule(self,schedule,day=None):
    doc, cmdElem = self._getXML('setup')
    schedElem = doc.createElement("SCHEDULE")
    cmdElem.appendChild(schedElem)

    # iterate over all days (either given day or all days)
    # and add XML-node to command-document
    
    days = [day] if day is not None else [ i for i in range(7) ]
    for d in days:
      dayElem = doc.createElement("Device.System.Power.Schedule."+str(d))
      dayElem.setAttribute("value","ON")
      dayElem.appendChild(doc.createTextNode(schedule.toTransport(d)))
      schedElem.appendChild(dayElem)

      listElem = doc.createElement("Device.System.Power.Schedule."+str(d)+".List")
      listElem.appendChild(doc.createTextNode(schedule.getTransportSwitchList(d)))
      schedElem.appendChild(listElem)

    return self._parseResult(self._postCmd(doc))

  # set state for a given time-range   ----------------------------------------
  # (this only changes the schedule in the given range)

  def setState(self,start,end,active=True):
    sched = self.getSchedule()          # query current schedule
    sched.setState(start,end,active)    # set value in given range
    return self.setSchedule(sched)      # write schedule back to plug

  # configure (exclusive) time in status ON/OFF   -----------------------------

  def setExclusiveState(self,start,end,active=True):
    sched = Schedule(not active)            # all ON or OFF schedule
    sched.setState(start,end,active)        # time range in status OFF/ON
    return self.setSchedule(sched)          # write schedule to plug
  
  # clear schedule   ----------------------------------------------------------

  def clear(self,active=True):
    sched = Schedule(active)
    self.setSchedule(sched)

  
# -----------------------------------------------------------------------------
# test program   --------------------------------------------------------------

if __name__ == "__main__":
  try:
    if len(sys.argv) > 2:
      plug = Plug(sys.argv[1],password=sys.argv[2])

      # query power state
      state = plug.getPowerState()
      print "Power state is active: %s" % state

      # set power state
      result = plug.setPowerState(len(sys.argv) > 3)
      print "Setting power state... success?:", result

      # query current schedule
      print "Current schedule:"
      print plug.getSchedule()

      sched = Schedule(False)
      sched.setState(TPoint(TPoint.MON,0,0),TPoint(TPoint.TUE,0,0),True)
      print "input schedule:"
      print sched
      print "Setting schedule... success:", plug.setSchedule(sched)
      print "Output schedule from plug:"
      #print plug.getSchedule(getDom=True).toprettyxml()
      print plug.getSchedule()

      #print \
      #  plug.setState(TPoint(TPoint.FRI,0,0),TPoint(TPoint.SAT,0,0),False).\
      #  toprettyxml()

      #now = TPoint.now()
      #now = now.createAfter(1,0,0)
      #then = now.createAfter(0,3,0)
      #print plug.setExclusiveState(now,then,False).toprettyxml()
    else:
      print "please pass host/ip and password as argument"
  except Exception as e:
    print e
