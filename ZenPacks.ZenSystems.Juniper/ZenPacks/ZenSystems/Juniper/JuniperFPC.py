##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 28th, 2011
# Revised:
#
# JuniperFPC object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperFPC

JuniperFPC is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity


import logging
log = logging.getLogger('JuniperFPC')

class JuniperFPC(DeviceComponent, ManagedEntity):
    """Juniper FPC object"""

    portal_type = meta_type = 'JuniperFPC'
    
    #**************Custom data Variables here from modeling************************
    
    containerIndex = 1
    containerDescr = ''
    containerParentIndex = 1
    containerParentDescr = ''
    FPCType = ''
    FPCDescr = ''
    FPCSerialNo = ''
    FPCRevision = '' 
    FPCPartNo = '' 
    FPCChassisId = 0
    FPCChassisDescr = '' 
    FPCChassisCLEI = '' 
    FPCCPU = 0
    FPCTemp = 0
    FPCState = 0
    FPCUpTime = ''
    FPCMemory = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'containerIndex', 'type':'int', 'mode':''},
        {'id':'containerDescr', 'type':'string', 'mode':''},
        {'id':'containerParentIndex', 'type':'int', 'mode':''},
        {'id':'containerParentDescr', 'type':'string', 'mode':''},
        {'id':'FPCType', 'type':'string', 'mode':''},
        {'id':'FPCDescr', 'type':'string', 'mode':''},
        {'id':'FPCSerialNo', 'type':'string', 'mode':''},
        {'id':'FPCRevision', 'type':'string', 'mode':''},
        {'id':'FPCPartNo', 'type':'string', 'mode':''},
        {'id':'FPCChassisId', 'type':'int', 'mode':''},
        {'id':'FPCChassisDescr', 'type':'string', 'mode':''},
        {'id':'FPCChassisCLEI', 'type':'string', 'mode':''},
        {'id':'FPCCPU', 'type':'int', 'mode':''},
        {'id':'FPCTemp', 'type':'int', 'mode':''},
        {'id':'FPCState', 'type':'int', 'mode':''},
        {'id':'FPCUpTime', 'type':'string', 'mode':''},
        {'id':'FPCMemory', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevFP", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperFP")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperFPC',
            'meta_type'      : 'JuniperFPC',
            'description'    : """Juniper FPC info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperFPC',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper FPC Graphs'
                , 'action'        : 'viewJuniperFPC'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper FPC Template'
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
        return self.JuniperDevFP()
    
InitializeClass(JuniperFPC)
