##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 28th, 2011
# Revised:
#
# JuniperBGP object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperBGP

JuniperBGP is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperBGP')

class JuniperBGP(DeviceComponent, ManagedEntity):
    """Juniper BGP object"""

    portal_type = meta_type = 'JuniperBGP'
    
    #**************Custom data Variables here from modeling************************
    
    bgpLocalAddress = ''
    bgpRemoteAddress = ''
    bgpRemoteASN = ''
    bgpStateInt = 0
    bgpStateText = ''
    bgpLastUpDown = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'bgpLocalAddress', 'type':'string', 'mode':''},
        {'id':'bgpRemoteAddress', 'type':'string', 'mode':''},
        {'id':'bgpRemoteASN', 'type':'string', 'mode':''},
        {'id':'bgpStateInt', 'type':'int', 'mode':''},
        {'id':'bgpStateText', 'type':'string', 'mode':''},
        {'id':'bgpLastUpDown', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevBG", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperBG")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperBGP',
            'meta_type'      : 'JuniperBGP',
            'description'    : """Juniper BGP info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperBGP',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper BGP Graphs'
                , 'action'        : 'viewJuniperBGP'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper BGP Template'
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
        return self.JuniperDevBG()
    
InitializeClass(JuniperBGP)
