################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoExpansionCardMap

CiscoExpansionCardMap maps the entPhysicalTable table to cards objects

$Id: CiscoExpansionCardMap.py,v 1.2 2010/12/15 13:15:37 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CiscoExpansionCardMap(SnmpPlugin):
    """Map Cisco Chassis Card table to model."""

    maptype = "CiscoExpansionCardMap"
    modname = "ZenPacks.community.CiscoEnvMon.CiscoExpansionCard"
    relname = "cards"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('cardTable',
                    '.1.3.6.1.2.1.47.1.1.1.1',
                    {
                        '.2': 'setProductKey',
                        '.4': '_cbi',
                        '.5': '_class',
                        '.6': 'slot',
                        '.8': 'HWVer',
                        '.9': 'FWRev',
                        '.10': 'SWVer',
                        '.11': 'serialNumber',
                        '.13': '_pn',
                    }
        ),
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        chassis = {}
        for oid, card in tabledata.get("cardTable",{}).iteritems():
            if int(card['_class']) == 5 and card['_cbi'] == 1:
                chassis[oid] = card['slot']
        for oid, card in tabledata.get("cardTable",{}).iteritems():
            if int(card.get('_class', 0)) != 9: continue
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                if int(getattr(om, '_cbi', 0)) > 2:
                    om.slot = chassis.get(str(om._cbi), None)
                    if not om.slot: continue
                om.id = self.prepId(om.slot)
                if getattr(om,'HWVer','').strip(): om.HWVer=om.HWVer.split()[0]
                om.setProductKey = MultiArgs(om.setProductKey, 'Cisco', om._pn)
            except AttributeError:
                continue
            rm.append(om)
        return rm
