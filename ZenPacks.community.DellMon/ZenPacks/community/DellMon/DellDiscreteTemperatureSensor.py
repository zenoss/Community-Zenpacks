################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellDiscreteTemperatureSensor

DellDiscreteTemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: DellDiscreteTemperatureSensor.py,v 1.0 2009/06/22 22:39:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.TemperatureSensor import *
from DellComponent import *

class DellDiscreteTemperatureSensor(TemperatureSensor, DellComponent):
    """Discrete TemperatureSensor object"""

    portal_type = meta_type = 'DellDiscreteTemperatureSensor'

    threshold = 1
    status = 1

    _properties = TemperatureSensor._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
                )    

    def state(self):
         return self.statusString()

    tempC = self.cacheRRDValue('temperature_celsius', default)


    def temperatureCelsiusString(self):
        """
        Return the current discrete temperature as a string
        """
        tempC = self.temperatureCelsius()
        if tempC == 1: return "Good"
        if tempC == 2: return "Bad"
        return "unknown"

    def temperatureFahrenheitString(self):
        """
        Return the current discrete temperature as a string
        """
        return self.temperatureCelsiusString()

InitializeClass(DellDiscreteTemperatureSensor)
