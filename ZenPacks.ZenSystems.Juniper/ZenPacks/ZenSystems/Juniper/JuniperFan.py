##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 17th, 2011
# Revised:
#
# JuniperFan object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""JuniperFan

JuniperFan is a component of a JuniperDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

from Products.ZenModel.Fan import *

import logging
log = logging.getLogger('JuniperFan')

class JuniperFan(Fan):
    """Juniper Fan object"""

    portal_type = meta_type = 'JuniperFan'
    
    #**************Custom data Variables here from modeling************************
    
    fanContainerIndex = 0
    fanDescr = ''
    fanType = ''
    fanSerialNo = ''
    fanRevision = ''
    fanChassisId = 0
    fanState = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = Fan._properties + (
        {'id':'fanContainerIndex', 'type':'int', 'mode':''},
        {'id':'fanDescr', 'type':'string', 'mode':''},
        {'id':'fanType', 'type':'string', 'mode':''},
        {'id':'fanSerialNo', 'type':'string', 'mode':''},
        {'id':'fanRevision', 'type':'string', 'mode':''},
        {'id':'fanChassisId', 'type':'int', 'mode':''},
        {'id':'fanState', 'type':'int', 'mode':''},
        )
    #****************
    

# Do we need any of this factory stuff or can it just inherit from Fan ???
# If this is uncommented, you get the extra menus from the Display dropdown
#    factory_type_information = ( 
#        { 
#            'id'             : 'Fan',
#            'meta_type'      : 'Fan',
#            'description'    : """Juniper Fan info""",
#            'product'        : 'ZenModel',
#            'factory'        : 'manage_addFan',
#            'immediate_view' : 'viewJuniperFan',
#            'actions'        :
#            ( 
#                { 'id'            : 'status'
#                , 'name'          : 'Juniper Fan Graphs'
#                , 'action'        : 'viewJuniperFan'
#                , 'permissions'   : (ZEN_VIEW, )
#                },
#                { 'id'            : 'perfConf'
#                , 'name'          : 'Juniper Fan Template'
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


InitializeClass(JuniperFan)
