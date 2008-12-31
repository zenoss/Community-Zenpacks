###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap

class HPSIMTemperatureMap(SnmpPlugin):
    """Map HP insight manager temperature table to model."""

    maptype = "HPSIMTemperatureMap"
    meta_type = "HPTemperatureSensor"
    modname = "ZenPacks.community.HPSIMMonitor.HPTemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"

#    ocolumns = {
#        '1':'cpqHeTemperatureChassis',
#        '2':'cpqHeTemperatureIndex',
#        '3':'cpqHeTemperatureLocale',
#        '4':'cpqHeTemperatureThreshold',
#        '5':'cpqHeTemperatureCondition',
#        '6':'cpqHeTemperatureThresholdType',
#        '7':'cpqHeTemperatureHwLocation'
#    }

    columns = {
        '.1':'chassis',
        '.2':'snmpindex',
        '.3':'locale',
        '.6':'state',
#        '.7':'hwlocation'
    }

    sensorLocale = {
        1:'other',
        2:'unknown',
        3:'system',
        4:'systemBoard',
        5:'ioBoard',
        6:'cpu',
        7:'memory',
        8:'storage',
        9:'removableMedia',
        10:'powerSupply',
        11:'ambient',
        12:'chassis',
        13:'bridgeCard'
    }

    conditions = {
        0:'other',
        2:'ok',
        3:'degraded',
        4:'failed'
    }

    snmpGetTableMaps = (
        GetTableMap('hp-temp-table', '.1.3.6.1.4.1.232.6.2.6.8.1', columns),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        getdata, tabledata = results
        temptable = tabledata.get("hp-temp-table")
        log.info('processing %s for device %s', self.name(), device.id)
        names = {}
        if not temptable: return
        rm = self.relMap()
        for sensor in temptable.values():
            try:
                newsensor={}
                newsensor['snmpindex'] = '%s.%s' % (sensor['chassis'],sensor['snmpindex'])
                if not sensor.has_key('hwlocation'):
                    if sensor['locale'] not in names:
                        names[sensor['locale']] = 0
                    newsensor['id'] = '%s %s' % (self.sensorLocale[sensor['locale']],str(names[sensor['locale']]))
                    names[sensor['locale']] = names[sensor['locale']] + 1
                else:
                    newsensor['id'] = sensor['hwlocation']
                newsensor['state'] = self.conditions.get(sensor['state'],'unknown')
                newsensor['id'] = self.prepId(newsensor['id'])
                om = self.objectMap(newsensor)
            except AttributeError:
                continue
            rm.append(om)
        return rm

