################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPFan

HPFan is an abstraction of a fan or probe.

$Id: HPFan.py,v 1.0 2008/11/28 15:10:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.Fan import *
from HPComponent import *

class HPFan(Fan, HPComponent):
    """Fan object"""

    portal_type = meta_type = 'HPFan'

    status = 1

    _properties = HWComponent._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
		 )

    def state(self):
        return self.statusString()

InitializeClass(HPFan)
