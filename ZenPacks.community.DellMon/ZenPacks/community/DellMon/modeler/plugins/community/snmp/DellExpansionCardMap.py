################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellExpansionCardMap

DellExpansionCardMap maps the pCIDeviceTable table to cards objects

$Id: DellExpansionCardMap.py,v 1.2 2010/08/14 00:07:15 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class DellExpansionCardMap(SnmpPlugin):
    """Map Dell System Management PCI table to model."""

    maptype = "DellExpansionCardMap"
    modname = "ZenPacks.community.DellMon.DellExpansionCard"
    relname = "cards"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('pciTable',
                    '.1.3.6.1.4.1.674.10892.1.1100.80.1',
                    {
                        '.5': 'status',
                        '.6': 'slot',
                        '.8': '_manuf',
                        '.9': '_model',
                    }
        ),
        GetTableMap('storageCntlrTable',
                    '.1.3.6.1.4.1.674.10893.1.20.130.1.1',
                    {
                        '.1': 'snmpindex',
                        '.2': '_model',
                        '.3': '_manuf',
                        '.4': 'controllerType',
                        '.8': 'FWRev',
                        '.9': '_cacheSizeM',
                        '.10': 'cacheSize',
                        '.38': 'status',
                        '.41': 'SWVer',
                        '.42': 'slot',
                        '.43': 'role',
                    }
        ),
    )

    controllerTypes = { 1: 'SCSI',
                        2: 'PowerVault 660F',
                        3: 'PowerVault 662F',
                        4: 'IDE',
                        5: 'SATA',
                        6: 'SAS',
                        }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        getdata, tabledata = results
        pcicardtable = tabledata.get('pciTable')
        cntlrtable = tabledata.get('storageCntlrTable')
        cntlrs = {}
        ttable = ''.join(chr(x) for x in range(256))
        for oid, cntlr in cntlrtable.iteritems():
            cntlr['snmpindex'] = oid.strip('.')
            cntlrs[cntlr['_model'].translate(ttable, ' /'.lower())] = cntlr
        for oid, card in pcicardtable.iteritems():
            try:
                cntlr = cntlrs.get(card['_model'].translate(ttable, ' /-'.lower()), None)
                if cntlr:
                    om = self.objectMap(cntlr)
                    om.modname = "ZenPacks.community.DellMon.DellStorageCntlr"
                    om.model = om._model
                    om.controllerType = self.controllerTypes.get(getattr(om, 'controllerType', 0), 'Unknown')
                    om.cacheSize = "%d" % (getattr(om, '_cacheSizeM', 0) * 1048576 + getattr(om, 'cacheSize', 0))
                    om.slot = card['slot']
                else: 
                    om = self.objectMap(card)
                    om.snmpindex = oid.strip('.')
                om.id = self.prepId("pci%s" % om.slot)
                om._manuf = getattr(om, '_manuf', 'Unknown').split('(')[0].strip()
                om.setProductKey = MultiArgs(om._model, om._manuf)
            except AttributeError:
                continue
            rm.append(om)
        return rm
