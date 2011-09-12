#!/usr/bin/env python
        
import os
import sys
import os.path
from stat import *

import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit
dmd = ZenScriptBase(connect=True).dmd

for dev in dmd.Devices.Power.Olson.getSubDevices():
  dev.os.addIpInterface('eth0', dev.manageIp)
  i=dev.os.interfaces._getOb('eth0')
  i.description = 'Manually kludged'
  i.setIpAddresses(dev.manageIp)
  i.macaddress=dev.getHWTag()
  i.monitor = False
  i.type = 'manual'
  i.adminStatus = 1
  i.operStatus = 1
  i.speed = 10000000
  i.MTU = 1500
  i.lockFromDeletion()
  i.lockFromUpdates()
commit()
