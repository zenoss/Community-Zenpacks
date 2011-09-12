##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 2nd, 2011
# Revised:
#
# JuniperBaseComp object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperBaseComp

JuniperBaseComp is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperBaseComp')

class JuniperBaseComp(DeviceComponent, ManagedEntity):
    """Juniper BaseComp object"""

    portal_type = meta_type = 'JuniperBaseComp'
    
    #**************Custom data Variables here from modeling************************
    
    containerIndex = 1
    containerDescr = ''
    containerParentIndex = 1
    containerParentDescr = ''
    BaseCompType = ''
    BaseCompDescr = ''
    BaseCompSerialNo = ''
    BaseCompRevision = '' 
    BaseCompPartNo = '' 
    BaseCompChassisId = 0
    BaseCompChassisDescr = '' 
    BaseCompChassisCLEI = '' 
    BaseCompCPU = 0
    BaseCompTemp = 0
    BaseCompState = 0
    BaseCompUpTime = ''
    BaseCompMemory = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'containerIndex', 'type':'int', 'mode':''},
        {'id':'containerDescr', 'type':'string', 'mode':''},
        {'id':'containerParentIndex', 'type':'int', 'mode':''},
        {'id':'containerParentDescr', 'type':'string', 'mode':''},
        {'id':'BaseCompType', 'type':'string', 'mode':''},
        {'id':'BaseCompDescr', 'type':'string', 'mode':''},
        {'id':'BaseCompSerialNo', 'type':'string', 'mode':''},
        {'id':'BaseCompRevision', 'type':'string', 'mode':''},
        {'id':'BaseCompPartNo', 'type':'string', 'mode':''},
        {'id':'BaseCompChassisId', 'type':'int', 'mode':''},
        {'id':'BaseCompChassisDescr', 'type':'string', 'mode':''},
        {'id':'BaseCompChassisCLEI', 'type':'string', 'mode':''},
        {'id':'BaseCompCPU', 'type':'int', 'mode':''},
        {'id':'BaseCompTemp', 'type':'int', 'mode':''},
        {'id':'BaseCompState', 'type':'int', 'mode':''},
        {'id':'BaseCompUpTime', 'type':'string', 'mode':''},
        {'id':'BaseCompMemory', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevBC", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperBC")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperBaseComp',
            'meta_type'      : 'JuniperBaseComp',
            'description'    : """Juniper BaseComp info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperBaseComp',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper BaseComp Graphs'
                , 'action'        : 'viewJuniperBaseComp'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper BaseComp Template'
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
        return self.JuniperDevBC()
    
InitializeClass(JuniperBaseComp)
