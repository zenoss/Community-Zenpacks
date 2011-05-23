##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 3rd, 2011
# Revised:
#
# ApcPduOutlet object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""ApcPduOutlet

ApcPduOutlet is a component of a ApcPduDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('ApcPduOutlet')

class ApcPduOutlet(DeviceComponent, ManagedEntity):
    """APC PDU Outlet object"""

    portal_type = meta_type = 'ApcPduOutlet'
    
    #**************Custom data Variables here from modeling************************
    
    outNumber = 0
    outName = ''
    outState = 'Unknown'
    outBank = 0
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'outNumber', 'type':'int', 'mode':''},
        {'id':'outName', 'type':'string', 'mode':''},
        {'id':'outState', 'type':'string', 'mode':''},
        {'id':'outBank', 'type':'int', 'mode':''},
        )
    #****************
    
    _relations = (
        ("ApcPduDevOut", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.ApcPdu.ApcPduDevice", "ApcPduOut")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'ApcPduOutlet',
            'meta_type'      : 'ApcPduOutlet',
            'description'    : """APC PDU Outlet info""",
            'product'        : 'ApcPdu',
            'immediate_view' : 'viewApcPduOutlet',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'APC PDU Outlet Graphs'
                , 'action'        : 'viewApcPduOutlet'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'APC PDU Outlet Template'
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
        return str( self.outNumber ) + "-" + self.outName


    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName


    def device(self):
        return self.ApcPduDevOut()
    
    def monitored(self):
        """
        Dummy
        """
        return True
        
InitializeClass(ApcPduOutlet)
