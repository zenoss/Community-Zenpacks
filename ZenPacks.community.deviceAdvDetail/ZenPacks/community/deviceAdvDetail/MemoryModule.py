################################################################################
#
# This program is part of the deviceAdvDetail Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MemoryModule

MemoryModule is an abstraction of a memorymodule.

$Id: MemoryModule.py,v 1.0 2009/04/23 14:57:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass

from Products.ZenUtils.Utils import convToUnits

from Products.ZenRelations.RelSchema import *

from Products.ZenModel.HWComponent import HWComponent
from Products.ZenModel.ZenossSecurity import *

class MemoryModule(HWComponent):

    """MemoryModule object"""

    portal_type = meta_type = 'MemoryModule'

    slot = 0
    size = 0
    moduletype = ""
    status = 1
    
    _properties = HWComponent._properties + (
        {'id':'slot', 'type':'int', 'mode':'w'},
        {'id':'size', 'type':'int', 'mode':'w'},
        {'id':'moduletype', 'type':'string', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW", "memorymodules")),
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

InitializeClass(MemoryModule)
