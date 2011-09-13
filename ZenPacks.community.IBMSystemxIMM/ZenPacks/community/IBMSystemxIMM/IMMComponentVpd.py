# ==============================================================================
# IMMComponentVpd object class
#
# Zenoss community Zenpack for IBM SystemX Integrated Management Module
# version: 0.3
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

__doc__="""IMMComponentVpd is the object class for the IMM Chassis Component VPD"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "0.3.0"

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('IMMComponentVpd')

class IMMComponentVpd(DeviceComponent, ManagedEntity):
    """IMM VPD object"""

    # When Javascript bits are used, this name must match the value of the 1st field in ZC.registerName() in the *.js
    portal_type = meta_type = 'IMMComponentVpd'
    
    # Data retrieved from modeling
    componentLevelVpdIndex = '0'
    componentLevelVpdFruNumber = ''
    componentLevelVpdFruName = ''
    componentLevelVpdSerialNumber = ''
    componentLevelVpdManufacturingId = ''

    _properties = (
        {'id':'componentLevelVpdIndex', 'type':'int', 'mode':''},
        {'id':'componentLevelVpdFruNumber', 'type':'string', 'mode':''},
        {'id':'componentLevelVpdFruName', 'type':'string', 'mode':''},
        {'id':'componentLevelVpdSerialNumber', 'type':'string', 'mode':''},
        {'id':'componentLevelVpdManufacturingId', 'type':'string', 'mode':''},
        )
    
    _relations = (
        ("IMMDev", ToOne(ToManyCont,
            "ZenPacks.community.IBMSystemxIMM.IMMDevice", "IMMCOMPVPD")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'IMMComponentVpd',
            'meta_type'      : 'IMMComponentVpd',
            'product'        : 'IBMSystemxIMM',
            'immediate_view' : 'viewDevicePerformance',
            'actions'        :
            ( 
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
        """ The component name as it will appear in the UI """
        if self.componentLevelVpdFruName.__len__() == 0:
            return "Unknown"
        else:
            return str( self.componentLevelVpdIndex ) + " - " + self.componentLevelVpdFruName

    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName

    def primarySortKey(self):
        """Sort by VPD index number then VPD type"""
        return "%s%s" % (self.componentLevelVpdIndex, self.componentLevelVpdFruName)

    def device(self):
        return self.IMMDev()
    
    def monitored(self):
        return True

InitializeClass(IMMComponentVpd)
