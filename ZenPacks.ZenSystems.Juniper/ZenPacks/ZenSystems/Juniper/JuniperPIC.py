##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 1st, 2011
# Revised:
#
# JuniperPIC object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperPIC

JuniperPIC is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperPIC')

class JuniperPIC(DeviceComponent, ManagedEntity):
    """Juniper PIC object"""

    portal_type = meta_type = 'JuniperPIC'
    
    #**************Custom data Variables here from modeling************************
    
    containerIndex = 1
    containerDescr = ''
    containerParentIndex = 1
    containerParentDescr = ''
    PICType = ''
    PICDescr = ''
    PICSerialNo = ''
    PICRevision = '' 
    PICPartNo = '' 
    PICChassisId = 0
    PICChassisDescr = '' 
    PICChassisCLEI = '' 
    PICCPU = 0
    PICTemp = 0
    PICState = 0
    PICUpTime = ''
    PICMemory = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'containerIndex', 'type':'int', 'mode':''},
        {'id':'containerDescr', 'type':'string', 'mode':''},
        {'id':'containerParentIndex', 'type':'int', 'mode':''},
        {'id':'containerParentDescr', 'type':'string', 'mode':''},
        {'id':'PICType', 'type':'string', 'mode':''},
        {'id':'PICDescr', 'type':'string', 'mode':''},
        {'id':'PICSerialNo', 'type':'string', 'mode':''},
        {'id':'PICRevision', 'type':'string', 'mode':''},
        {'id':'PICPartNo', 'type':'string', 'mode':''},
        {'id':'PICChassisId', 'type':'int', 'mode':''},
        {'id':'PICChassisDescr', 'type':'string', 'mode':''},
        {'id':'PICChassisCLEI', 'type':'string', 'mode':''},
        {'id':'PICCPU', 'type':'int', 'mode':''},
        {'id':'PICTemp', 'type':'int', 'mode':''},
        {'id':'PICState', 'type':'int', 'mode':''},
        {'id':'PICUpTime', 'type':'string', 'mode':''},
        {'id':'PICMemory', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevPI", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperPI")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperPIC',
            'meta_type'      : 'JuniperPIC',
            'description'    : """Juniper PIC info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperPIC',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper PIC Graphs'
                , 'action'        : 'viewJuniperPIC'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper PIC Template'
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
        return self.JuniperDevPI()
    
InitializeClass(JuniperPIC)
