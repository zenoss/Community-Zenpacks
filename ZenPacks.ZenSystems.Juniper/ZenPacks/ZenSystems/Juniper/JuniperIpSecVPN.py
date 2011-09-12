##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 3rd, 2011
# Revised:
#
# JuniperIpSecVPN object class
# VPNs will only be populated on SRX devices
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperIpSecVPN

JuniperIpSecVPN is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperIpSecVPN')

class JuniperIpSecVPN(DeviceComponent, ManagedEntity):
    """Juniper IpSecVPN object"""

    portal_type = meta_type = 'JuniperIpSecVPN'
    
    #**************Custom data Variables here from modeling************************
    
    vpnPhase1LocalGwAddr = ''
    vpnPhase1LocalIdValue = ''
    vpnPhase1RemoteIdValue = ''
    vpnPhase1State = ''
    vpnPhase2LocalGwAddr = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'vpnPhase1LocalGwAddr', 'type':'string', 'mode':''},
        {'id':'vpnPhase1LocalIdValue', 'type':'string', 'mode':''},
        {'id':'vpnPhase1RemoteIdValue', 'type':'string', 'mode':''},
        {'id':'vpnPhase1State', 'type':'string', 'mode':''},
        {'id':'vpnPhase2LocalGwAddr', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevIpSecV", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperIpSecV")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperIpSecVPN',
            'meta_type'      : 'JuniperIpSecVPN',
            'description'    : """Juniper IpSecVPN info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperIpSecVPN',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper IpSecVPN Graphs'
                , 'action'        : 'viewJuniperIpSecVPN'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper IpSecVPN Template'
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
        return self.JuniperDevIpSecV()
    
InitializeClass(JuniperIpSecVPN)
