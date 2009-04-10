################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqNicIfPhysAdapter

cpqNicIfPhysAdapter is an abstraction of a HP NIC.

$Id: cpqNicIfPhysAdapter.py,v 1.0 2008/12/05 15:14:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from HPExpansionCard import HPExpansionCard

class cpqNicIfPhysAdapter(HPExpansionCard):
    """NIC object"""

    portal_type = meta_type = 'cpqNicIfPhysAdapter'

    model = ""
    role = ""
    macaddress = ""
    duplex = ""
    speed = 0
    port = 0
    
    # we monitor RAID Controllers
    monitor = True

    statusmap = [(4, 3, 'other'),
	        (4, 3, 'other'),
	        (0, 0, 'Ok'),
		(3, 5, 'General Failure'),
		(2, 4, 'Link Failure'),
		]

    _properties = HPExpansionCard._properties + (
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'role', 'type':'string', 'mode':'w'},
        {'id':'macaddress', 'type':'string', 'mode':'w'},
        {'id':'duplex', 'type':'string', 'mode':'w'},
        {'id':'speed', 'type':'int', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'cpqNicIfPhysAdapter',
            'meta_type'      : 'cpqNicIfPhysAdapter',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addCpqNicIfPhysAdapter',
            'immediate_view' : 'viewCpqNicIfPhysAdapter',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqNicIfPhysAdapter'
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

InitializeClass(cpqNicIfPhysAdapter)
