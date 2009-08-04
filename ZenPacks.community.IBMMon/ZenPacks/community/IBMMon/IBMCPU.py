################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMCPU

IBMCPU is an abstraction of a CPU.

$Id: IBMCPU.py,v 1.0 2009/07/12 23:08:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.CPU import *

class IBMCPU(CPU):
    """CPU object"""

    core = 1
    socket = 0
    clockspeed = 0
    extspeed = 0
    voltage = 0
    cacheSizeL1 = 0
    cacheSizeL2 = 0
    cacheSizeL3 = 0

    _properties = (
         {'id':'core', 'type':'int', 'mode':'w'},
         {'id':'socket', 'type':'int', 'mode':'w'},
         {'id':'clockspeed', 'type':'int', 'mode':'w'},     #MHz
         {'id':'extspeed', 'type':'int', 'mode':'w'},       #MHz
         {'id':'voltage', 'type':'int', 'mode':'w'},        #Millivolts
         {'id':'cacheSizeL1', 'type':'int', 'mode':'w'},    #KBytes
         {'id':'cacheSizeL2', 'type':'int', 'mode':'w'},    #KBytes
         {'id':'cacheSizeL3', 'type':'int', 'mode':'w'},    #KBytes
    )    

InitializeClass(IBMCPU)
