#!/usr/bin/python

# Class definition of TPoint
#
# TPoint represents a timepoint (minute) in the weekly schedule
#
# This file is part of the project https://github.com/bablokb/ediplug
#
# Copyright: Bernhard Bablok
# License: GPL v3
#

from datetime import datetime

class TPoint(object):
  """Timepoint data-object"""

  # symbolic names for weekdays   --------------------------------------------
  
  SUN = 0
  MON = 1
  TUE = 2
  WED = 3
  THU = 4
  FRI = 5
  SAT = 6

  # names of days (should be localized)   ------------------------------------
  
  DAYS = [ 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' ]

  # translation-code for TPoint to transport-format   ------------------------
  
  TCODE="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  #      012345678901234567890123456789012345678901234567890123456789
  #                1         2         3         4         5

  # normalize index to valid range   -----------------------------------------

  @staticmethod
  def _normalizeIndex(index):
    day = (index) // 1440
    hour = (index - day*1440) // 60
    minute = (index - day*1440 - hour*60)
    return (day,hour,minute)
      
  # create day,hour,min for arbitrary input   --------------------------------

  @staticmethod
  def _normalize(day,hour,minute):
    index = (1440*day + 60*hour + minute ) % 10080
    return TPoint._normalizeIndex(index)

  # return TPoint for a given index   ----------------------------------------

  @staticmethod
  def create(index):
    day,hour,minute = TPoint._normalizeIndex(index)
    return TPoint(day,hour,minute)
  
  # return TPoint for "now"   ------------------------------------------------

  @staticmethod
  def now():
    now = datetime.today()
    return TPoint(now.isoweekday() % 7,now.hour,now.minute)

  # Constructor passing day, hour, minute   ----------------------------------
  
  def __init__(self,day,hour,minute):
    self.__Day, self.__Hour, self.__Minute = TPoint._normalize(day,hour,minute)

  # repr function   ---------------------------------------------------------
  
  def __repr__(self):
    return "<TPoint day:%s, hour:%s, minute:%s>" % \
           (self.__Day,self.__Hour,self.__Minute)

  # pretty print as string   ------------------------------------------------

  def __str__(self):
    return "%s %02d:%02d" % (TPoint.DAYS[self.__Day],self.__Hour,self.__Minute)

  # getter for day   --------------------------------------------------------

  @property
  def day(self):
    return self.__Day

  # setter for day   --------------------------------------------------------

  @day.setter
  def day(self,day):
    self.__Day = day
  
  # getter for hour   -------------------------------------------------------

  @property
  def hour(self):
    return self.__Hour

  # setter for hour   -------------------------------------------------------

  @hour.setter
  def hour(self,hour):
    self.__Hour = hour
  
  # getter for minute   -----------------------------------------------------

  @property
  def minute(self):
    return self.__Minute

  # setter for minute   -----------------------------------------------------

  @minute.setter
  def minute(self,minute):
    self.__Minute = minute
  
  # convert to transport   --------------------------------------------------

  def toTransport(self):
    return TPoint.TCODE[self.__Hour] + TPoint.TCODE[self.__Minute]
  
  # return flat index of TPoint in weekly schedule   ------------------------
  
  def getIndex(self):
    return self.__Day*1440 + self.__Hour*60 + self.__Minute

  # return TPoint after given duration   ------------------------------------
  
  def createAfter(self,days,hours,minutes):
    newIndex = (self.getIndex() + 1440*days + 60*hours + minutes) % 10080
    return TPoint.create(newIndex)

  # add duration to TPoint   ------------------------------------------------
  
  def add(self,days,hours,minutes):
    self.__init__(self.__Day+days,self.__Hour+hours,self.__Minute+minutes)
    return self

# test   ---------------------------------------------------------------------

if __name__ == "__main__":
  tp = TPoint(0,0,0)
  print "tp: %s" % tp
  print "tp.getIndex(): %d" % tp.getIndex()

  tp = TPoint(0,10,02)
  print "tp: %s" % tp
  print "tp.getIndex(): %d" % tp.getIndex()

  tp2 = tp.createAfter(-1,-1,-5)
  #tp2 = tp.createAfter(0,0,0)
  print "tp2 = tp.createAfter(-1,-1,-5): %s" % tp2
  print "tp2.toTransport(): %s" % tp2.toTransport()
  
  now = TPoint.now()
  print "now: %s" % now
  print "now.toTransport(): %s" % now.toTransport()
  print "now (day number): %d" % now.day
  
  now.day = TPoint.TUE
  print "now on Tuesday: %s" % now
  
