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

$Id: HPFan.py,v 1.0 2009/03/12 13:34:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.Fan import *
from HPComponent import HPComponent

class HPsdFan(Fan, HPComponent):
    """Speed Detect Fan object"""

    portal_type = meta_type = 'HPsdFan'

    status = 1

    _properties = HWComponent._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
		 )

    def state(self):
        return self.statusString()

    def rpmString(self):
        """
        Return a string representation of the RPM
        """
        rpm = self.rpm()
	if rpm == 2: return "Normal"
	if rpm == 3: return "High"
	return "Unknown"

InitializeClass(HPsdFan)
