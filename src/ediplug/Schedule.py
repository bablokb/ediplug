#!/usr/bin/python

# Class definition of Schedule
#
# Schedule holds the low-level datastructure of a weekly schedule.
# It is implemented as a list of 1 or 0
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

from TPoint import TPoint as TPoint

class Schedule(object):
  """Schedule data-object"""

  # Constructor. If argument is true, it is initialized with 1, else 0 -------
  
  def __init__(self,active=True):
    self.init(active)

  # Re-initialize structure   ------------------------------------------------

  def init(self,active=True):
    val = '1' if active else '0'
    self.__sched = list(10080*val)

  # get list of switch-points   ----------------------------------------------

  def getSwitchList(self,day):
    resultList = []
    startIndex = day*1440
    endIndex   = startIndex + 1439
    dayList = self.__sched[startIndex:endIndex]
    if self.__sched[startIndex-1] <> self.__sched[startIndex]:
      resultList.append((TPoint.create(startIndex),dayList[0]))
    val = dayList[0]
    try:
      index = dayList.index('1' if val=='0' else '0',1)
      while index > 0:
        val = dayList[index]
        resultList.append((TPoint.create(startIndex+index),val))
        index = dayList.index('1' if val=='0' else '0',index+1)
    except ValueError:
      pass
    return resultList

  # get the switch-points in transport-format   ------------------------------
  
  def getTransportSwitchList(self,day):
    tplist = ""
    list = self.getSwitchList(day)
    i = 0
    while i < len(list):
      (tpstart,valstart) = list[i]
      if valstart == '1':
        if i < len(list)-1:
          (tpend,valend) = list[i+1]
          i = i+1
        else:
          (tpend,valend) = (TPoint(day,23,59),'0')
        if len(tplist):
          tplist += "-" + tpstart.toTransport() + tpend.toTransport() + "1"
        else:
          tplist = tpstart.toTransport() + tpend.toTransport() + "1"
      i = i + 1
    return tplist
  
  # convert to transport format   --------------------------------------------

  def toTransport(self,day):
    # pack four values together
    startIndex = day*360
    endIndex   = startIndex + 360
    out = [''.join(self.__sched[4*i:4*(i+1)]) \
                                          for i in range(startIndex,endIndex)]
    # convert to hex ...
    out = [hex(int(i,2))[2:] for i in out]
    # ... and return result
    return ''.join(out).upper()

  # convert from transport format   -----------------------------------------

  def fromTransport(self,value,day):
    sched = int('F'+value,16)        # the F is to preserve the length
    startIndex = day*360             # it will be removed in the last line
    endIndex   = startIndex + 360
    # convert to list and assign
    self.__sched[4*startIndex:4*endIndex] = list(bin(sched)[6:])

  # get state for timepoint-range   -----------------------------------------

  def getState(self,start,end=None):
    # TODO: handle start > end
    return self.__sched[start.getIndex():end.getIndex()]

  # set state for given timepoint-range   -----------------------------------

  def setState(self,start,end,active=True):
    # end itself is not included!
    val = '1' if active else '0'
    startIndex = start.getIndex()
    endIndex   = end.getIndex()
    if endIndex >= startIndex:
      self.__sched[startIndex:endIndex] = list((endIndex-startIndex)*val)
    else:
      self.__sched[startIndex:10080] = list((10080-startIndex)*val)
      self.__sched[0:endIndex] = list(endIndex*val)

  # string representation ---------------------------------------------------

  def __str__(self):
    str = ''
    for i in range(7):
      str += TPoint.DAYS[i] + ":"
      tf = self.toTransport(i)
      for j in range(6):
        part = tf[60*j:60*(j+1)]
        str += part[0:14] + " " + part[15:29] + " " + \
               part[30:44] + " " + part[45:59]
      
  # repr function   ---------------------------------------------------------
  
  def __repr__(self):
    repr = "<Schedule: \n"
    for i in range(7):
      tf = self.toTransport(i)
      repr += str(i) + ':\n'
      for j in range(6):
        repr += '    ' + tf[60*j:60*(j+1)] + '\n'
    return  repr +  ">"
                                  
# test   ---------------------------------------------------------------------

if __name__ == "__main__":
    s = Schedule(False)
    s.setState(TPoint(TPoint.MON,0,0),TPoint(TPoint.TUE,0,0),True)
    s.setState(TPoint(TPoint.WED,10,0),TPoint(TPoint.WED,11,0),True)
    s.setState(TPoint(TPoint.WED,20,0),TPoint(TPoint.WED,22,0),True)
    print s
    
    for (tp,val) in  s.getSwitchList(TPoint.MON) +  s.getSwitchList(TPoint.WED) :
      print "%s: %s" % (tp, 'ON' if val=='1' else 'OFF')
    for d in range(7):
      print "%d:" % d, s.getTransportSwitchList(d)
