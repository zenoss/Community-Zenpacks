# ==============================================================================
# IMMFwVpd object class
#
# Zenoss community Zenpack for IBM SystemX Integrated Management Module
# version: 1.0
#
# (C) Copyright IBM Corp. 2011. All Rights Reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ==============================================================================

__doc__="""IMMFwVpd is the object class for the IMM System firmware VPD"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "1.0.0"

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('IMMFwVpd')

class IMMFwVpd(DeviceComponent, ManagedEntity):
    """IMM VPD object"""

    # When 3.0 style Javascript is not used, this is the name that will appear in the UI under Components heading.
    # When Javascript bits are used, this name must match the value of the 1st field in ZC.registerName() in the *.js;
    # the name that appears in the UI is then determined be the remaining fields of ZC.registerName().
#   event_key = portal_type = meta_type = 'IMM Firmware VPD'
    portal_type = meta_type = 'IMMFwVpd'
    
    # Data retrieved from modeling
    immVpdIndex = '0'
    immVpdType = 'VPD'
    immVpdVersionString = 'ABCDEFG' 
    immVpdReleaseDate = '01/01/2000'

    _properties = (
        {'id':'immVpdIndex', 'type':'int', 'mode':''},
        {'id':'immVpdType', 'type':'string', 'mode':''},
        {'id':'immVpdVersionString', 'type':'string', 'mode':''},
        {'id':'immVpdReleaseDate', 'type':'string', 'mode':''}
        )
    
    _relations = (
        ("IMMDev", ToOne(ToManyCont,
            "ZenPacks.community.IBMSystemxIMM.IMMDevice", "IMMFWVPD")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'IMMFwVpd',
            'meta_type'      : 'IMMFwVpd',
#           'description'    : """VPD entry info""",
            'product'        : 'IBMSystemxIMM',
            'immediate_view' : 'IMMFwVpd',
            'actions'        :
            ( 
#               { 'id'            : 'status'
#               , 'name'          : 'Another Graphs tab'
#               , 'action'        : 'viewDevicePerformance'
#               , 'permissions'   : (ZEN_VIEW, )
#               },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Monitoring Templates'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                },                
            )
          },
        ) 

    isUserCreatedFlag = True

    def isUserCreated(self):
        """
        Returns the value of isUserCreated. True adds SAVE & CANCEL buttons to Details menu
        """
        return self.isUserCreatedFlag

    def viewName(self):
        """ The component name as it will appear in the UI... assuming you display the attribute 'name'... """
        if self.immVpdType.__len__() == 0:
            return "Unknown"
        else:
            return str( self.immVpdIndex ) + " - " + self.immVpdType

    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName

    def primarySortKey(self):
        """Sort by VPD index number then VPD type"""
        return "%s%s" % (self.immVpdIndex, self.immVpdType)

    ## -- I think the idea here is, this method returns the containing device via the relation defined above...
    def device(self):
        return self.IMMDev()
    
    def monitored(self):
        return True

InitializeClass(IMMFwVpd)
