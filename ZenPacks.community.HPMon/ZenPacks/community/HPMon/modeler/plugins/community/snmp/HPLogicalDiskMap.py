################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPLogicalDiskMap

HPLogicalDiskMap maps the cpqDaLogDrvTable, cpqFcaLogDrvTable or cpqScsiLogDrvTabletables
to disks objects

$Id: HPHardDiskMap.py,v 1.0 2009/04/24 13:13:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap

class HPLogicalDiskMap(SnmpPlugin):
    """Map HP/Compaq insight manager Logical Disk tables to model."""

    maptype = "HPLogicalDiskMap"
    modname = "ZenPacks.community.HPMon.HPLogicalDisk"
    relname = "logicaldisks"
    compname = "hw"

    oms = {}

    diskTypes = {1: 'other',
                }

    snmpGetMap = GetMap({'.1.3.6.1.2.1.1.2.0' : 'snmpOid'})

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        if not device.id in self.oms:
            return rm
        for om in self.oms[device.id]:
            rm.append(om)
        del self.oms[device.id]
        return rm
