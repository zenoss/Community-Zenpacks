##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 15th, 2011
# Revised:
#
# JuniperPS object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperPS

JuniperPS is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

from Products.ZenModel.PowerSupply import *

import logging
log = logging.getLogger('JuniperPS')

class JuniperPS(PowerSupply, JuniperComponent):
    """Juniper Power Supply object"""

    
    #**************Custom data Variables here from modeling************************
    
    psuAvailable = 1
    outletName = ''
    outletDesc = ''
    outletCurrent = 0
    outletPower = 0
    outletVoltage = 0
    outletStatus = 0
    thermalValue = 0
    humidityValue = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'psuAvailable', 'type':'int', 'mode':''},
        {'id':'outletName', 'type':'string', 'mode':''},
        {'id':'outletDesc', 'type':'string', 'mode':''},
        {'id':'outletCurrent', 'type':'int', 'mode':''},
        {'id':'outletPower', 'type':'int', 'mode':''},
        {'id':'outletVoltage', 'type':'int', 'mode':''},
        {'id':'outletStatus', 'type':'int', 'mode':''},
        {'id':'thermalValue', 'type':'int', 'mode':''},
        {'id':'humidityValue', 'type':'int', 'mode':''},
        )
    #****************
    

    factory_type_information = ( 
        { 
            'id'             : 'PowerSupply',
            'meta_type'      : 'PowerSupply',
            'description'    : """Juniper Power Supply info""",
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPowerSupply',
            'immediate_view' : 'viewJuniperPS',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper Power Supply Graphs'
                , 'action'        : 'viewJuniperPS'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper Power Supply Template'
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


InitializeClass(JuniperPS)
