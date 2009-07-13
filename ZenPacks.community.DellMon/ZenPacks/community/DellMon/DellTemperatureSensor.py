################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellTemperatureSensor

DellTemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: DellTemperatureSensor.py,v 1.0 2009/06/22 22:39:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.TemperatureSensor import *
from DellComponent import *

class DellTemperatureSensor(TemperatureSensor, DellComponent):
    """TemperatureSensor object"""

    portal_type = meta_type = 'DellTemperatureSensor'

    threshold = 0
    status = 1

    _properties = TemperatureSensor._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
                )    

    def state(self):
         return self.statusString()

    def temperatureCelsius(self, default=None):
        """
        Return the current temperature in degrees celsius
        """
        tempC = self.cacheRRDValue('temperature_celsius', default)
        if tempC is not None:
            return long(tempC) / 10
        return None
    temperature = temperatureCelsius


InitializeClass(DellTemperatureSensor)
