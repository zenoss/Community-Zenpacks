##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 28th, 2011
# Revised:
#
# ApcUpsBattery object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""ApcUpsBattery

ApcUpsBattery is a component of a ApcUpsDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('ApcUpsBattery')

class ApcUpsBattery(DeviceComponent, ManagedEntity):
    """APC UPS Battery object"""

    portal_type = meta_type = 'ApcUpsBattery'
    

    #**************Custom data Variables here from modeling************************
    
    batteryStatus = 0
    batteryStatusText = ''
    timeOnBattery = 0
    batteryLastReplacementDate = ''
    batteryReplaceIndicator = 0
    batteryReplaceIndicatorText = ''
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'batteryStatus', 'type':'int', 'mode':''},
        {'id':'batteryStatusText', 'type':'string', 'mode':''},
        {'id':'timeOnBattery', 'type':'int', 'mode':''},
        {'id':'batteryLastReplacementDate', 'type':'string', 'mode':''},
        {'id':'batteryReplaceIndicator', 'type':'int', 'mode':''},
        {'id':'batteryReplaceIndicatorText', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("ApcUpsDevBat", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.ApcUps.ApcUpsDevice", "ApcUpsBat")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'ApcUpsBattery',
            'meta_type'      : 'ApcUpsBattery',
            'product'        : 'ApcUps',
            'immediate_view' : 'viewApcUpsBattery',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'APC UPS Battery Graphs'
                , 'action'        : 'viewApcUpsBattery'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'APC UPS Battery Template'
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

    def viewName(self):
        """Pretty version human readable version of this object"""
        return self.id


    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName


    def device(self):
        return self.ApcUpsDevBat()
    

InitializeClass(ApcUpsBattery)
