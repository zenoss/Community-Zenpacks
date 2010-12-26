################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellStorageCntlr

DellStorageCntlr is an abstraction of a Dell Storage Controller.

$Id: DellStorageCntlr.py,v 1.2 2010/10/17 19:13:22 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits
from DellExpansionCard import *

class DellStorageCntlr(DellExpansionCard):
    """Delll Storage Controller object"""

    FWRev = ""
    SWVer = ""
    role = 1
    cacheSize = 0
    controllerType = ""

    # we monitor RAID Controllers
    monitor = True

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Other'),
                2: (DOT_GREY, SEV_WARNING, 'Unknown'),
                3: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                4: (DOT_YELLOW, SEV_WARNING, 'Non-critical'),
                5: (DOT_ORANGE, SEV_ERROR, 'Critical'),
                6: (DOT_RED, SEV_CRITICAL, 'Non-recoverable'),
                }

    _properties = DellExpansionCard._properties + (
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'SWVer', 'type':'string', 'mode':'w'},
        {'id':'role', 'type':'int', 'mode':'w'},
        {'id':'cacheSize', 'type':'int', 'mode':'w'},
        {'id':'controllerType', 'type':'string', 'mode':'w'},
    )


    factory_type_information = (
        {
            'id'             : 'DellStorageCntlr',
            'meta_type'      : 'DellStorageCntlr',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addDellStorageCntlr',
            'immediate_view' : 'viewDellStorageCntlr',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellStorageCntlr'
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

    def roleString(self):
        """
        Return the controller current role in human readable form
        """
        roles = {1: 'Enables',
                2: 'Disabled',
                3: 'Active',
                99: 'Not Applicable',
                }
        return roles.get(self.role, roles[99])

    def cacheSizeString(self):
        """
        Return the cache size in human readable form ie 10MB
        """
        return convToUnits(self.cacheSize)

InitializeClass(DellStorageCntlr)
