##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 2nd, 2011
# Revised:
#
# JuniperMIC object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperMIC

JuniperMIC is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('JuniperMIC')

class JuniperMIC(DeviceComponent, ManagedEntity):
    """Juniper MIC object"""

    portal_type = meta_type = 'JuniperMIC'
    
    #**************Custom data Variables here from modeling************************
    
    containerIndex = 1
    containerDescr = ''
    containerParentIndex = 1
    containerParentDescr = ''
    MICType = ''
    MICDescr = ''
    MICSerialNo = ''
    MICRevision = '' 
    MICPartNo = '' 
    MICChassisId = 0
    MICChassisDescr = '' 
    MICChassisCLEI = '' 
    MICCPU = 0
    MICTemp = 0
    MICState = 0
    MICUpTime = ''
    MICMemory = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'containerIndex', 'type':'int', 'mode':''},
        {'id':'containerDescr', 'type':'string', 'mode':''},
        {'id':'containerParentIndex', 'type':'int', 'mode':''},
        {'id':'containerParentDescr', 'type':'string', 'mode':''},
        {'id':'MICType', 'type':'string', 'mode':''},
        {'id':'MICDescr', 'type':'string', 'mode':''},
        {'id':'MICSerialNo', 'type':'string', 'mode':''},
        {'id':'MICRevision', 'type':'string', 'mode':''},
        {'id':'MICPartNo', 'type':'string', 'mode':''},
        {'id':'MICChassisId', 'type':'int', 'mode':''},
        {'id':'MICChassisDescr', 'type':'string', 'mode':''},
        {'id':'MICChassisCLEI', 'type':'string', 'mode':''},
        {'id':'MICCPU', 'type':'int', 'mode':''},
        {'id':'MICTemp', 'type':'int', 'mode':''},
        {'id':'MICState', 'type':'int', 'mode':''},
        {'id':'MICUpTime', 'type':'string', 'mode':''},
        {'id':'MICMemory', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("JuniperDevMI", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.Juniper.JuniperDevice", "JuniperMI")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'JuniperMIC',
            'meta_type'      : 'JuniperMIC',
            'description'    : """Juniper MIC info""",
            'product'        : 'Juniper',
            'immediate_view' : 'viewJuniperMIC',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Juniper MIC Graphs'
                , 'action'        : 'viewJuniperMIC'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Juniper MIC Template'
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
        return self.JuniperDevMI()
    
InitializeClass(JuniperMIC)
