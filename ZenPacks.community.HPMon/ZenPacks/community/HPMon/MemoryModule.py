################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MemoryModule

MemoryModule is an abstraction of a  Memory Module.

$Id: MemoryModule.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits

from Products.ZenModel.ExpansionCard import *

class MemoryModule(ExpansionCard):

    """MemoryModule object"""

    portal_type = meta_type = 'MemoryModule'

    size = 0
    moduletype = ""
    speed = 0
    frequency = 0
    
    _properties = ExpansionCard._properties + (
        {'id':'size', 'type':'int', 'mode':'w'},
        {'id':'moduletype', 'type':'string', 'mode':'w'},
        {'id':'speed', 'type':'int', 'mode':'w'},
        {'id':'frequency', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'MemoryModule',
            'meta_type'      : 'MemoryModule',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'MemoryModule_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addMemoryModule',
            'immediate_view' : 'viewMemoryModule',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewMemoryModule'
                , 'permissions'   : ('View',)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : ("Change Device", )
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
	if self.size > 0:
            return convToUnits(self.size)
	else:
	    return ''

    def speedString(self):
        """
        Return the speed in human readable form
        """
	if self.size > 0:
            return "%dns" % self.speed
	else:
	    return ''

    def frequencyString(self):
        """
        Return the memory module frequency in MHz
        """
	if self.size > 0:
            return "%dMHz" % self.frequency
	else:
	    return ''

InitializeClass(MemoryModule)
