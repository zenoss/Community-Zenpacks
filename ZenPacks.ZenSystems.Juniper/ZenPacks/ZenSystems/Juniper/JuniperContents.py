##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 16th, 2011
# Revised:
#
# JuniperContents object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperContents

JuniperContents is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperContents')

class JuniperContents(DeviceComponent, ManagedEntity):
    """Juniper Contents object"""

    portal_type = meta_type = 'JuniperContents'
    
    #**************Custom data Variables here from modeling************************
    
    containerIndex = 1
    containerDescr = ''
    containerParentIndex = 1
    containerParentDescr = ''
    contentsType = ''
    contentsDescr = ''
    contentsSerialNo = ''
    contentsRevision = '' 
    contentsPartNo = '' 
    contentsChassisId = 0
    contentsChassisDescr = '' 
    contentsChassisCLEI = '' 
    contentsCPU = 0
    contentsTemp = 0
    contentsState = 0
    contentsUpTime = ''
    contentsMemory = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'containerIndex', 'type':'int', 'mode':''},
        {'id':'containerDescr', 'type':'string', 'mode':''},
        {'id':'containerParentIndex', 'type':'int', 'mode':''},
        {'id':'containerParentDescr', 'type':'string', 'mode':''},
        {'id':'contentsType', 'type':'string', 'mode':''},
        {'id':'contentsDescr', 'type':'string', 'mode':''},
        {'id':'contentsSerialNo', 'type':'string', 'mode':''},
        {'id':'contentsRevision', 'type':'string', 'mode':''},
        {'id':'contentsPartNo', 'type':'string', 'mode':''},
        {'id':'contentsChassisId', 'type':'int', 'mode':''},
        {'id':'contentsChassisDescr', 'type':'string', 'mode':''},
        {'id':'contentsChassisCLEI', 'type':'string', 'mode':''},
        {'id':'contentsCPU', 'type':'int', 'mode':''},
        {'id':'contentsTemp', 'type':'int', 'mode':''},
        {'id':'contentsState', 'type':'int', 'mode':''},
        {'id':'contentsUpTime', 'type':'string', 'mode':''},
        {'id':'contentsMemory', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevConte", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperConte")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperContents',
            'meta_type'      : 'JuniperContents',
            'description'    : """Juniper Contents info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperContents',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper Contents Graphs'
                , 'action'        : 'viewJuniperContents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper Contents Template'
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
        return self.JuniperDevConte()
    
InitializeClass(JuniperContents)
