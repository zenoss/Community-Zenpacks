################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqNicIfPhysAdapter

cpqNicIfPhysAdapter is an abstraction of a HP NIC.

$Id: cpqNicIfPhysAdapter.py,v 1.1 2010/06/30 16:25:15 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from HPExpansionCard import *

class cpqNicIfPhysAdapter(HPExpansionCard):
    """NIC object"""

    model = ""
    role = ""
    macaddress = ""
    duplex = ""
    speed = 0
    port = 0

    # we monitor RAID Controllers
    monitor = True

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
                2: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                3: (DOT_RED, SEV_CRITICAL, 'General Failure'),
                4: (DOT_ORANGE, SEV_ERROR, 'Link Failure'),
                }

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
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
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
