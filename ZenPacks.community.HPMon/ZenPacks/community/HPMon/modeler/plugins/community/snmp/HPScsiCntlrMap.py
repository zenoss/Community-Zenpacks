################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPScsiCntlrMap

HPScsiCntlrMap maps the cpqScsiCntlrTable table to cpqScsiCntlr objects

$Id: HPScsiCntlrMap.py,v 1.1 2009/08/18 17:02:53 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPExpansionCardMap import HPExpansionCardMap

class HPScsiCntlrMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqScsiCntlrTable table to model."""

    maptype = "cpqScsiCntlr"
    modname = "ZenPacks.community.HPMon.cpqScsiCntlr"

    snmpGetTableMaps = (
        GetTableMap('cpqScsiCntlrTable',
	            '.1.3.6.1.4.1.232.5.2.2.1.1',
		    {
			'.3': 'model',
			'.4': 'FWRev',
			'.6': 'slot',
			'.7': 'status',
			'.13': 'serialNumber',
			'.14': 'scsiwidth',
		    }
	),
    )

    models =   {1: 'other',
                2: 'Compaq 32-Bit Fast SCSI-2 Controller',
                3: 'Compaq Systempro/XL Integrated SCSI-2 Options Port',
                4: 'Compaq Integrated Fast-SCSI-2 Controller/P',
                5: 'Compaq 32-Bit Fast-Wide SCSI-2 /E Controller',
                6: 'Compaq 32-Bit Fast-Wide SCSI-2 /P Controller',
                7: 'Compaq Deskpro XL Integrated PCI SCSI-2 Controller',
                8: 'Compaq Wide-Ultra SCSI Controller',
                9: 'Compaq Extended SCSI Controller',
                10: 'Compaq Wide Ultra2 SCSI Controller',
                11: 'Compaq 64-Bit Dual Channel Wide Ultra2 SCSI Controller',
                12: 'Compaq Wide Ultra3 SCSI Adapter',
                13: 'Compaq StorageWorks Library Adapter',
                14: 'HP 64-Bit/133MHz PCI-X 2CH Ultra320 HBA',
                15: 'HP PCI-X Dual Channel Ultra320 SCSI Adapter',
                16: 'Unknown SCSI Controller',
                17: 'HP Single Channel Ultra320 SCSI HBA G2',
                18: 'HP Single Channel Ultra320 SCSI HBA',
                19: 'HP SC11Xe Host Bus Adapter',
                }

    scsiwidths =   {1: 'other',
		    2: 'Narrow SCSI',
		    3: 'Wide SCSI',
		    }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	cardtable = tabledata.get('cpqScsiCntlrTable')
	if not device.id in HPExpansionCardMap.oms:
	    HPExpansionCardMap.oms[device.id] = []
        for oid, card in cardtable.iteritems():
            try:
                om = self.objectMap(card)
		om.snmpindex = oid.strip('.')
                om.id = self.prepId("cpqScsiCntlr%s" % om.snmpindex.replace('.', '_'))
                om.slot = getattr(om, 'slot', 0)
		om.model = self.models.get(getattr(om, 'model', 16), '%s (%d)' %(self.models[16], om.model))
                om.setProductKey = "%s" % om.model
		om.scsiwidth = self.scsiwidths.get(getattr(om, 'scsiwidth', 1), '%s (%d)' %(self.scsiwidths[1], om.scsiwidth))
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
	return

