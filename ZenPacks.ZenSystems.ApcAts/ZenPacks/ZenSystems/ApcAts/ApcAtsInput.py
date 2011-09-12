##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 7th, 2011
# Revised:
#
# ApcAtsInput object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""ApcAtsInput

ApcAtsInput is a component of a ApcAtsDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('ApcAtsInput')

class ApcAtsInput(DeviceComponent, ManagedEntity):
    """APC ATS Input object"""

    portal_type = meta_type = 'ApcAtsInput'
    
    #**************Custom data Variables here from modeling************************
    
    inputType = ''
    inputName = ''
    inputFrequency = 0
    inputVoltage = 0
    statusSelectedSource = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'inputType', 'type':'string', 'mode':''},
        {'id':'inputName', 'type':'string', 'mode':''},
        {'id':'inputFrequency', 'type':'int', 'mode':''},
        {'id':'inputVoltage', 'type':'int', 'mode':''},
        {'id':'statusSelectedSource', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("ApcAtsDevIn", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.ApcAts.ApcAtsDevice", "ApcAtsIn")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'ApcAtsInput',
            'meta_type'      : 'ApcAtsInput',
            'description'    : """APC ATS Input info""",
            'product'        : 'ApcAts',
            'immediate_view' : 'viewApcAtsInput',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'APC ATS Input Graphs'
                , 'action'        : 'viewApcAtsInput'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'APC ATS Input Template'
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
        return self.ApcAtsDevIn()
    
    def monitored(self):
        """
        Dummy
        """
        return True
        
InitializeClass(ApcAtsInput)
