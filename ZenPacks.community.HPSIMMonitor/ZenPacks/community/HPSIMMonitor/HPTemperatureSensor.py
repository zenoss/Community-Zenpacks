###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__="""HPTemperatureSensor

HPTemperatureSensor is a variation of the standard temperature sensor class.
It allows HP specific temperature sensors not to clash with other vendors.

$Id: HPTemperatureSensor.py,v 1.00 2008/11/03 16:56:00 mikea Exp $"""

__version__="Revision: 1.00 $"[11:-2]

from Products.ZenModel.TemperatureSensor import *

class HPTemperatureSensor(TemperatureSensor):
    """
    HP Systems Insight Manager Temperature Sensor
    """
    
InitializeClass(HPTemperatureSensor)
