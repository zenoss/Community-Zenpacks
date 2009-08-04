################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMFan

IBMFan is an abstraction of a fan or probe.

$Id: IBMFan.py,v 1.0 2009/06/22 22:35:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.Fan import *
from IBMComponent import *

class IBMFan(Fan, IBMComponent):
    """Fan object"""

    portal_type = meta_type = 'IBMFan'

    status = 3
    threshold = 0

    _properties = Fan._properties + (
                 {'id':'status', 'type':'int', 'mode':'w'},
                 {'id':'threshold', 'type':'int', 'mode':'w'},
		 )

    def setState(self, value):
        self.status = 0
        for intvalue, status in self.statusmap.iteritems():
            if status[2].upper() != value.upper(): continue 
            self.status = value
            break
        
    state = property(fget=lambda self: self.statusString(),
                     fset=lambda self, v: self.setState(v)
		     )        

InitializeClass(IBMFan)
