##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 8th, 2011
# Revised:
#
# DellUpsBattery object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""DellUpsBattery

DellUpsBattery is a component of a DellUpsDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('DellUpsBattery')

class DellUpsBattery(DeviceComponent, ManagedEntity):
    """Dell UPS Battery object"""

    portal_type = meta_type = 'DellUpsBattery'
    

    #**************Custom data Variables here from modeling************************
    
    batteryABMStatus = 0
    batteryABMStatusText = ''
    batteryTestStatus = 0
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'batteryABMStatus', 'type':'int', 'mode':''},
        {'id':'batteryABMStatusText', 'type':'string', 'mode':''},
        {'id':'batteryTestStatus', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("DellUpsDevBat", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.DellUps.DellUpsDevice", "DellUpsBat")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'DellUpsBattery',
            'meta_type'      : 'DellUpsBattery',
            'description'    : """Dell UPS Battery info""",
            'product'        : 'DellUps',
            'immediate_view' : 'viewDellUpsBattery',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Dell UPS Battery Graphs'
                , 'action'        : 'viewDellUpsBattery'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Dell UPS Battery Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW, )
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
        """Pretty version human readable version of this object"""
        return self.id


    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName


    def device(self):
        return self.DellUpsDevBat()
    
    def monitored(self):
        """
        Dummy
        """
        return True
        

InitializeClass(DellUpsBattery)
