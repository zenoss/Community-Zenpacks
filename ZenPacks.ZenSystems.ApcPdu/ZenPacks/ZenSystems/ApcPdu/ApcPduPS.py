##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 4th, 2011
# Revised:		Feb 11th, 2011
#			Make power supply a standalone, single-instance component
#
# ApcPduPS object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""ApcPduPS

ApcPduPS is a component of a ApcPduDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('ApcPduPS')

class ApcPduPS(DeviceComponent, ManagedEntity):
    """APC PDU PS object"""

    portal_type = meta_type = 'ApcPduPS'
    
    #**************Custom data Variables here from modeling************************
    
    supply1Status = ''
    supply2Status = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'supply1Status', 'type':'string', 'mode':''},
        {'id':'supply2Status', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("ApcPduDevP", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.ApcPdu.ApcPduDevice", "ApcPduP")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'ApcPduPS',
            'meta_type'      : 'ApcPduPS',
            'description'    : """APC PDU PS info""",
            'product'        : 'ApcPdu',
            'immediate_view' : 'viewApcPduPS',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'APC PDU PS Graphs'
                , 'action'        : 'viewApcPduPS'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'APC PDU PS Template'
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
        return self.ApcPduDevP()
    
    def monitored(self):
        """
        Dummy
        """
        return True
        
InitializeClass(ApcPduPS)
