################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellFan

DellFan is an abstraction of a fan or probe.

$Id: DellFan.py,v 1.0 2009/06/22 22:35:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.Fan import *
from DellComponent import *

class DellFan(Fan, DellComponent):
    """Fan object"""

    portal_type = meta_type = 'DellFan'

    status = 1
    threshold = 0

    _properties = Fan._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
		 )

    def state(self):
        return self.statusString()

InitializeClass(DellFan)
