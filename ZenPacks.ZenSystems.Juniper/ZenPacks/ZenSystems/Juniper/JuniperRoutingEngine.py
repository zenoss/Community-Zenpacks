##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 1st, 2011
# Revised:
#
# JuniperRoutingEngine object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperRoutingEngine

JuniperRoutingEngine is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity


import logging
log = logging.getLogger('JuniperRoutingEngine')

class JuniperRoutingEngine(DeviceComponent, ManagedEntity):
    """Juniper RoutingEngine object"""

    portal_type = meta_type = 'JuniperRoutingEngine'
    
    #**************Custom data Variables here from modeling************************
    
    containerIndex = 1
    containerDescr = ''
    containerParentIndex = 1
    containerParentDescr = ''
    RoutingEngineType = ''
    RoutingEngineDescr = ''
    RoutingEngineSerialNo = ''
    RoutingEngineRevision = '' 
    RoutingEnginePartNo = '' 
    RoutingEngineChassisId = 0
    RoutingEngineChassisDescr = '' 
    RoutingEngineChassisCLEI = '' 
    RoutingEngineCPU = 0
    RoutingEngineTemp = 0
    RoutingEngineState = 0
    RoutingEngineUpTime = ''
    RoutingEngineMemory = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'containerIndex', 'type':'int', 'mode':''},
        {'id':'containerDescr', 'type':'string', 'mode':''},
        {'id':'containerParentIndex', 'type':'int', 'mode':''},
        {'id':'containerParentDescr', 'type':'string', 'mode':''},
        {'id':'RoutingEngineType', 'type':'string', 'mode':''},
        {'id':'RoutingEngineDescr', 'type':'string', 'mode':''},
        {'id':'RoutingEngineSerialNo', 'type':'string', 'mode':''},
        {'id':'RoutingEngineRevision', 'type':'string', 'mode':''},
        {'id':'RoutingEnginePartNo', 'type':'string', 'mode':''},
        {'id':'RoutingEngineChassisId', 'type':'int', 'mode':''},
        {'id':'RoutingEngineChassisDescr', 'type':'string', 'mode':''},
        {'id':'RoutingEngineChassisCLEI', 'type':'string', 'mode':''},
        {'id':'RoutingEngineCPU', 'type':'int', 'mode':''},
        {'id':'RoutingEngineTemp', 'type':'int', 'mode':''},
        {'id':'RoutingEngineState', 'type':'int', 'mode':''},
        {'id':'RoutingEngineUpTime', 'type':'string', 'mode':''},
        {'id':'RoutingEngineMemory', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevRE", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperRE")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperRoutingEngine',
            'meta_type'      : 'JuniperRoutingEngine',
            'description'    : """Juniper RoutingEngine info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperRoutingEngine',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper RoutingEngine Graphs'
                , 'action'        : 'viewJuniperRoutingEngine'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper RoutingEngine Template'
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
        return self.JuniperDevRE()
    
InitializeClass(JuniperRoutingEngine)
