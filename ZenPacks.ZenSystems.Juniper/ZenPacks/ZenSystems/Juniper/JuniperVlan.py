##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 7th, 2011
# Revised:
#
# JuniperVlan object class
# VPNs will only be populated on SRX devices
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperVlan

JuniperVlan is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperVlan')

class JuniperVlan(DeviceComponent, ManagedEntity):
    """Juniper Vlan object"""

    portal_type = meta_type = 'JuniperVlan'
    
    #**************Custom data Variables here from modeling************************
    
    vlanName = ''
    vlanType = ''
    vlanTag = 0
    vlanPortGroup = 0
    vlanInterfaceInfo = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'vlanName', 'type':'string', 'mode':''},
        {'id':'vlanType', 'type':'string', 'mode':''},
        {'id':'vlanTag', 'type':'int', 'mode':''},
        {'id':'vlanPortGroup', 'type':'int', 'mode':''},
        {'id':'vlanInterfaceInfo', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevVl", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperVl")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperVlan',
            'meta_type'      : 'JuniperVlan',
            'description'    : """Juniper Vlan info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperVlan',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper Vlan Graphs'
                , 'action'        : 'viewJuniperVlan'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper Vlan Template'
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
        return self.JuniperDevVl()
    
InitializeClass(JuniperVlan)
