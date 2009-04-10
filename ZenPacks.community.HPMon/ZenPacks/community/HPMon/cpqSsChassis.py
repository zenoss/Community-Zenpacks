################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqSsChassis

cpqSsChassis is an abstraction of a HP Storage System Chassis.

$Id: cpqSsChassis.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from HPExpansionCard import HPExpansionCard
from cpqFcaCntlr import cpqFcaCntlr
from cpqFcaPhyDrv import cpqFcaPhyDrv
from cpqFcaLogDrv import cpqFcaLogDrv

class cpqSsChassis(HPExpansionCard):
    """HP Storage System Chassis object"""

    portal_type = meta_type = 'cpqSsChassis'

    name = ""
    connectionType = 1
    model = ""
    
    # we monitor RAID Controllers
    monitor = True

    connectionTypes =  {1: 'other',
		        2: 'FC',
		        3: 'SCSI',
		        4: 'iSCSI',
		        5: 'SAS',
		        }

    _properties = HPExpansionCard._properties + (
        {'id':'name', 'type':'string', 'mode':'w'},
        {'id':'connectionType', 'type':'int', 'mode':'w'},
        {'id':'model', 'type':'string', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'cpqSsChassis',
            'meta_type'      : 'cpqSsChassis',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addcpqSsChassis',
            'immediate_view' : 'viewCpqSsChassis',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCpqSsChassis'
                , 'permissions'   : ('View',)
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

    def getCntlr(self):
        cards = []
        for card in self.hw.cards():
	    if isinstance(card, cpqFcaCntlr) and card.snmpindex.split('.')[0] == self.snmpindex:
	        cards.append(card)
        return cards

    def getPhyDrv(self):
        disks = []
        for disk in self.hw.harddisks():
	    if isinstance(disk, cpqFcaPhyDrv) and disk.snmpindex.split('.')[0] == self.snmpindex:
	        disks.append(disk)
        return disks

    def getLogDrv(self):
        disks = []
        for disk in self.hw.harddisks():
	    if isinstance(disk, cpqFcaLogDrv) and disk.snmpindex.split('.')[0] == self.snmpindex:
	        disks.append(disk)
        return disks

    def connectionTypeString(self):
        return self.connectionTypes.get(self.connectionType, self.connectionTypes[1])
	
InitializeClass(cpqSsChassis)
