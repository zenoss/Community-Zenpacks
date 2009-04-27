################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPTemperatureSensor

HPTemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: HPTemperatureSensor.py,v 1.0 2008/11/24 12:52:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.TemperatureSensor import *
from HPComponent import *

class HPTemperatureSensor(TemperatureSensor, HPComponent):
    """TemperatureSensor object"""

    portal_type = meta_type = 'HPTemperatureSensor'

    threshold = 0
    status = 1

    _properties = HWComponent._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
                )    

    def state(self):
         return self.statusString()

InitializeClass(HPTemperatureSensor)
