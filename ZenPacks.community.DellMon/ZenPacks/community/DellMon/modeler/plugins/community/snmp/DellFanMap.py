################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellFanMap

DellFanMap maps the coolingDeviceTable table to fab objects

$Id: DellFanMap.py,v 1.1 2010/02/19 19:58:07 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class DellFanMap(SnmpPlugin):
    """Map Dell System Management Fans table to model."""

    maptype = "DellFanMap"
    modname = "ZenPacks.community.DellMon.DellFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('coolingDeviceTable',
                    '.1.3.6.1.4.1.674.10892.1.700.12.1',
                    {
                        '.5': 'status',
                        '.7': 'type',
                        '.8': '_locale',
                        '.13': 'threshold',
                    }
        ),
    )


    typemap = {1: 'Other', 
                2: 'Unknown',
                3: 'Fan',
                4: 'Blower',
                5: 'Chip Fan',
                6: 'Cabinet Fan',
                7: 'Power Supply Fan',
                8: 'Heat Pipe',
                9: 'Refrigeration',
                10: 'Active Cooling',
                11: 'Passive Cooling',
                }


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        fantable = tabledata.get('coolingDeviceTable')
        for oid, fan in fantable.iteritems():
            try:
                om = self.objectMap(fan)
                om.snmpindex = oid.strip('.')
                om.type = self.typemap.get(getattr(om, 'type', 2), self.typemap[2])
                om.id = self.prepId(getattr(om, '_locale', 'Unknown'))
            except AttributeError:
                continue
            rm.append(om)
        return rm
