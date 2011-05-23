##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 1st, 2011
# Revised:
#
# JuniperPowerSupply object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperPowerSupply

JuniperPowerSupply is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

from Products.ZenModel.PowerSupply import *

import logging
log = logging.getLogger('JuniperPowerSupply')

class JuniperPowerSupply(PowerSupply):
    """Juniper PowerSupply object"""

    portal_type = meta_type = 'JuniperPowerSupply'
    
    #**************Custom data Variables here from modeling************************
    
    powerSupplyContainerIndex = 0
    powerSupplyDescr = ''
    powerSupplyType = ''
    powerSupplySerialNo = ''
    powerSupplyPartNo = ''
    powerSupplyRevision = ''
    powerSupplyChassisId = 0
    powerSupplyState = 0
    powerSupplyTemp = 0
    powerSupplyCPU = 0
    powerSupplyMemory = 0
    powerSupplyUpTime = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = PowerSupply._properties + (
        {'id':'powerSupplyContainerIndex', 'type':'int', 'mode':''},
        {'id':'powerSupplyDescr', 'type':'string', 'mode':''},
        {'id':'powerSupplyType', 'type':'string', 'mode':''},
        {'id':'powerSupplySerialNo', 'type':'string', 'mode':''},
        {'id':'powerSupplyPartNo', 'type':'string', 'mode':''},
        {'id':'powerSupplyRevision', 'type':'string', 'mode':''},
        {'id':'powerSupplyChassisId', 'type':'int', 'mode':''},
        {'id':'powerSupplyState', 'type':'int', 'mode':''},
        {'id':'powerSupplyTemp', 'type':'int', 'mode':''},
        {'id':'powerSupplyCPU', 'type':'int', 'mode':''},
        {'id':'powerSupplyMemory', 'type':'int', 'mode':''},
        {'id':'powerSupplyUpTime', 'type':'string', 'mode':''},
        )
    #****************
    

# Do we need any of this factory stuff or can it just inherit from PowerSupply ???
# If this is uncommented, you get the extra menus from the Display dropdown
#    factory_type_information = ( 
#        { 
#            'id'             : 'PowerSupply',
#            'meta_type'      : 'PowerSupply',
#            'description'    : """Juniper PowerSupply info""",
#            'product'        : 'ZenModel',
#            'factory'        : 'manage_addPowerSupply',
#            'immediate_view' : 'viewJuniperPowerSupply',
#            'actions'        :
#            ( 
#                { 'id'            : 'status'
#                , 'name'          : 'Juniper PowerSupply Graphs'
#                , 'action'        : 'viewJuniperPowerSupply'
#                , 'permissions'   : (ZEN_VIEW, )
#                },
#                { 'id'            : 'perfConf'
#                , 'name'          : 'Juniper PowerSupply Template'
#                , 'action'        : 'objTemplates'
#                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
#                },                
#                { 'id'            : 'viewHistory'
#                , 'name'          : 'Modifications'
#                , 'action'        : 'viewHistory'
#                , 'permissions'   : (ZEN_VIEW, )
#                },
#            )
#          },
#        ) 

    def viewName(self):
        """Pretty version human readable version of this object"""
        return self.id


    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName


InitializeClass(JuniperPowerSupply)
