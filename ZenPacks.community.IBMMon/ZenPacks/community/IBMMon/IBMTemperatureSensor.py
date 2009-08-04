################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMTemperatureSensor

IBMTemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: IBMTemperatureSensor.py,v 1.0 2009/07/13 00:10:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.TemperatureSensor import *
from IBMComponent import *

class IBMTemperatureSensor(TemperatureSensor, IBMComponent):
    """TemperatureSensor object"""

    portal_type = meta_type = 'IBMTemperatureSensor'

    threshold = 0
    status = 1

    _properties = TemperatureSensor._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
                )    

    def temperatureCelsius(self, default=None):
        """
        Return the current temperature in degrees celsius
        """
        tempC = self.cacheRRDValue('temperature_celsius', default)
        if tempC is not None:
            return long(tempC)
        return None
    temperature = temperatureCelsius

    def setState(self, value):
        self.status = 0
        for intvalue, status in self.statusmap.iteritems():
            if status[2].upper() != value.upper(): continue 
            self.status = value
            break
        
    state = property(fget=lambda self: self.statusString(),
                     fset=lambda self, v: self.setState(v)
		     )        

InitializeClass(IBMTemperatureSensor)
