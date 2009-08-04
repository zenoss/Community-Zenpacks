################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMNetworkAdapter

IBMNetworkAdapter is an abstraction of a IBM NetworkAdapter.

$Id: IBMNetworkAdapter.py,v 1.0 2009/07/21 23:45:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.ExpansionCard import *
from IBMComponent import *

class IBMNetworkAdapter(ExpansionCard, IBMComponent):
    """NetworkAdapter object"""

    portal_type = meta_type = 'IBMNetworkAdapter'

    model = ""
    macaddress = ""
    speed = 0
    status = 0
    
    # we monitor Network Adapters
    monitor = True

    _properties = ExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'macaddress', 'type':'string', 'mode':'w'},
        {'id':'speed', 'type':'int', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'IBMNetworkAdapter',
            'meta_type'      : 'IBMNetworkAdapter',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'IBMMon',
            'factory'        : 'manage_addIBMNetworkAdapter',
            'immediate_view' : 'viewIBMNetworkAdapter',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewIBMNetworkAdapter'
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

    def speedString(self):
        """
        Return the speed in human readable form
        """
        if not self.speed:
            return 'Unknown'
        speed = self.speed
        for unit in ('bps', 'Kbps', 'Mbps', 'Gbps'):
            if speed < 1000: break
            speed /= 1000.0
        return "%.0f%s" % (speed, unit)

InitializeClass(IBMNetworkAdapter)
