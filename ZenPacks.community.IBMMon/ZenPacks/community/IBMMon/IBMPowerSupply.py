################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMPowerSupply

IBMPowerSupply is an abstraction of a PowerSupply.

$Id: IBMPowerSupply.py,v 1.0 2009/07/15 21:36:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

import inspect
from Products.ZenModel.PowerSupply import *
from IBMComponent import *

class IBMPowerSupply(PowerSupply, IBMComponent):
    """PowerSupply object"""

    portal_type = meta_type = 'IBMPowerSupply'

    status = 1
            
    _properties = PowerSupply._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'PowerSupply',
            'meta_type'      : 'PowerSupply',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'PowerSupply_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPowerSupply',
            'immediate_view' : 'viewIBMPowerSupply',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBMPowerSupply'
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

    def setState(self, value):
        self.status = 0
        for intvalue, status in self.statusmap.iteritems():
            if status[2].upper() != value.upper(): continue 
            self.status = value
            break
        
    state = property(fget=lambda self: self.statusString(),
                     fset=lambda self, v: self.setState(v)
		     )        


InitializeClass(IBMPowerSupply)
