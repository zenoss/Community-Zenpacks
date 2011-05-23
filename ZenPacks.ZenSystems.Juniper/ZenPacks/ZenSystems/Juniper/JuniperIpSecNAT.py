##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 7th, 2011
# Revised:
#
# JuniperIpSecNAT object class
# NATs will only be populated on SRX devices
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperIpSecNAT

JuniperIpSecNAT is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperIpSecNAT')

class JuniperIpSecNAT(DeviceComponent, ManagedEntity):
    """Juniper IpSecNAT object"""

    portal_type = meta_type = 'JuniperIpSecNAT'
    
    #**************Custom data Variables here from modeling************************
    
    natId = ''
    natNumPorts = 0
    natNumSess = 0
    natPoolType = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'natId', 'type':'string', 'mode':''},
        {'id':'natNumPorts', 'type':'int', 'mode':''},
        {'id':'natNumSess', 'type':'int', 'mode':''},
        {'id':'natPoolType', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevIpSecN", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperIpSecN")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperIpSecNAT',
            'meta_type'      : 'JuniperIpSecNAT',
            'description'    : """Juniper IpSecNAT info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperIpSecNAT',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper IpSecNAT Graphs'
                , 'action'        : 'viewJuniperIpSecNAT'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper IpSecNAT Template'
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
        return self.JuniperDevIpSecN()
    
InitializeClass(JuniperIpSecNAT)
