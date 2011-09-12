##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 24th, 2011
# Revised:
#
# JuniperComponents object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperComponents

JuniperComponents is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperComponents')

class JuniperComponents(DeviceComponent, ManagedEntity):
    """Juniper Components object"""

    portal_type = meta_type = 'JuniperComponents'
    
    #**************Custom data Variables here from modeling************************
    
    containerIndex = 1
    containerDescr = ''
    containerParentIndex = 1
    containerParentDescr = ''
    containerType = ''
    containerLevel = 0
    containerNextLevel = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'containerIndex', 'type':'int', 'mode':''},
        {'id':'containerDescr', 'type':'string', 'mode':''},
        {'id':'containerParentIndex', 'type':'int', 'mode':''},
        {'id':'containerParentDescr', 'type':'string', 'mode':''},
        {'id':'containerType', 'type':'string', 'mode':''},
        {'id':'containerLevel', 'type':'int', 'mode':''},
        {'id':'containerNextLevel', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevComp", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperComp")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperComponents',
            'meta_type'      : 'JuniperComponents',
            'description'    : """Juniper Components info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperComponents',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper Components Graphs'
                , 'action'        : 'viewJuniperComponents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper Components Template'
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
        return self.JuniperDevComp()
    
InitializeClass(JuniperComponents)
