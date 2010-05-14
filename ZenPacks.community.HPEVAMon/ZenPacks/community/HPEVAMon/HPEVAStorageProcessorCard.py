################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageProcessorCard

HPEVAStorageProcessorCard is an abstraction of a HPEVA_StorageProcessorCard

$Id: HPEVAStorageProcessorCard.py,v 1.0 2010/05/06 15:01:27 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from Products.ZenModel.ExpansionCard import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

class HPEVAStorageProcessorCard(ExpansionCard, HPEVAComponent):
    """HPStorageProcessorCard object"""

    portal_type = meta_type = 'HPEVAStorageProcessorCard'


    caption = ""
    FWRev = 0
    
    monitor = True
    
    _properties = ExpansionCard._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
		 )

    _relations = ExpansionCard._relations + (
        ("fcports", ToMany(ToOne,
	            "ZenPacks.community.HPEVAMon.HPEVAHostFCPort",
	            "controller")),
	)
	
    factory_type_information = ( 
        { 
            'id'             : 'HPEVAStorageProcessorCard',
            'meta_type'      : 'HPEVAStorageProcessorCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StorageProcessorCard_icon.gif',
            'product'        : 'HPEVAMon',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewHPEVAStorageProcessorCard',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAStorageProcessorCard'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : ("Change Device", )
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    def getStatus(self):
        """
        Return the components status
	"""
        return int(round(self.cacheRRDValue('OperationalStatus', 0)))

InitializeClass(HPEVAStorageProcessorCard)
