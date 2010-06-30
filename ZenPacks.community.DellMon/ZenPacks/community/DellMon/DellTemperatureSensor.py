################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellTemperatureSensor

DellTemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: DellTemperatureSensor.py,v 1.1 2010/06/30 22:09:04 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.TemperatureSensor import *
from DellComponent import *

class DellTemperatureSensor(TemperatureSensor, DellComponent):
    """TemperatureSensor object"""

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
            return long(tempC) / 10
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

    def getRRDTemplates(self):
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(DellTemperatureSensor)
