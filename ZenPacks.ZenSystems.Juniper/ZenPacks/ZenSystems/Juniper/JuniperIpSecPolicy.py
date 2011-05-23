##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 7th, 2011
# Revised:
#
# JuniperIpSecPolicy object class
# Policys will only be populated on SRX devices
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperIpSecPolicy

JuniperIpSecPolicy is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperIpSecPolicy')

class JuniperIpSecPolicy(DeviceComponent, ManagedEntity):
    """Juniper IpSecPolicy object"""

    portal_type = meta_type = 'JuniperIpSecPolicy'
    
    #**************Custom data Variables here from modeling************************
    
    policyId = ''
    policyAction = ''
    policyState = ''
    policyFromZone = ''
    policyToZone = ''
    policyName = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'policyId', 'type':'string', 'mode':''},
        {'id':'policyAction', 'type':'string', 'mode':''},
        {'id':'policyState', 'type':'string', 'mode':''},
        {'id':'policyFromZone', 'type':'string', 'mode':''},
        {'id':'policyToZone', 'type':'string', 'mode':''},
        {'id':'policyName', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevIpSecP", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperIpSecP")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperIpSecPolicy',
            'meta_type'      : 'JuniperIpSecPolicy',
            'description'    : """Juniper IpSecPolicy info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperIpSecPolicy',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper IpSecPolicy Graphs'
                , 'action'        : 'viewJuniperIpSecPolicy'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper IpSecPolicy Template'
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
        return self.JuniperDevIpSecP()
    
InitializeClass(JuniperIpSecPolicy)
