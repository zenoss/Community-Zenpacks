##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 4th, 2011
# Revised:
#
# ApcPduBank object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__="""ApcPduBank

ApcPduBank is a component of a ApcPduDevice Device

$Id: $"""

__version__ = "$Revision: $"[11:-2]

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity

import logging
log = logging.getLogger('ApcPduBank')

class ApcPduBank(DeviceComponent, ManagedEntity):
    """APC PDU Bank object"""

    portal_type = meta_type = 'ApcPduBank'
    
    #**************Custom data Variables here from modeling************************
    
    bankNumber = 0
    bankState = 0
    bankStateText = ''
    
    #**************END CUSTOM VARIABLES *****************************
    
    
    #*************  Those should match this list below *******************
    _properties = (
        {'id':'bankNumber', 'type':'int', 'mode':''},
        {'id':'bankState', 'type':'int', 'mode':''},
        {'id':'bankStateText', 'type':'string', 'mode':''},
        )
    #****************
    
    _relations = (
        ("ApcPduDevBan", ToOne(ToManyCont,
            "ZenPacks.ZenSystems.ApcPdu.ApcPduDevice", "ApcPduBan")),
        )

    factory_type_information = ( 
        { 
            'id'             : 'ApcPduBank',
            'meta_type'      : 'ApcPduBank',
            'description'    : """APC PDU Bank info""",
            'product'        : 'ApcPdu',
            'immediate_view' : 'viewApcPduBank',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'APC PDU Bank Graphs'
                , 'action'        : 'viewApcPduBank'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'APC PDU Bank Template'
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
#        return str( self.bankNumber )
        return self.id


    # use viewName as titleOrId because that method is used to display a human
    # readable version of the object in the breadcrumbs
    titleOrId = name = viewName


    def device(self):
        return self.ApcPduDevBan()
    
    def monitored(self):
        """
        Dummy
        """
        return True
        
InitializeClass(ApcPduBank)
