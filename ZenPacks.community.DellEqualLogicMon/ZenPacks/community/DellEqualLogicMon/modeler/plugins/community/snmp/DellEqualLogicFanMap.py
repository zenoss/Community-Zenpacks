################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class DellEqualLogicFanMap(SnmpPlugin):
    """Map Dell System Management Fans table to model."""

    maptype = "DellEqualLogicFanMap"
    modname = "ZenPacks.community.DellEqualLogicMon.DellEqualLogicFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('coolingDeviceTable',
                    '.1.3.6.1.4.1.12740.2.1.7.1',
                    {
                        '.4': 'status',
                        '.2': '_locale',
                        '.7': 'lowThreshold',
                        '.5': 'highThreshold',
                    }
        ),
    )

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
		om.type = "Fan"
                om.id = self.prepId(getattr(om, '_locale', 'Unknown'))
            except AttributeError:
                continue
            rm.append(om)
        return rm
