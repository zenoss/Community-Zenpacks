################################################################################
# 
# This file is part of ZenPacks.community.LLDP
#
# Copyright (C) 2011 GSI Helmholtzzentrum fuer Schwerionenforschung Gmbh
#                    Christoph Handel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
################################################################################

__doc__ = """Model Layer 2 Links using LLDP"""

__version__ = "0.1"

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap


class LLDPMap(SnmpPlugin):
    """Map Layer 2 links using LLDP"""

    maptype = "LLDPMap"
    modname = "ZenPacks.community.LLDP.LLDPLink"
    relname = "lldplinks"
    compname = "os"

    snmpGetTableMaps = (
        GetTableMap('lldpLocPort',
                    '.1.0.8802.1.1.2.1.3.7.1',
                    {
                        '.4': 'desc',
                    }
                    ),
        GetTableMap('lldpRemPort',
                    '.1.0.8802.1.1.2.1.4.1.1',
                    {
                        '.8': 'desc',
                        '.9': 'sys',
                    }
                    ),
        GetTableMap('lldpRemMan',
                    '.1.0.8802.1.1.2.1.4.2.1',
                    {
                        '.4': 'ifid',
                    }
                    ),
        )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        locPort = tabledata.get("lldpLocPort")
        remPort = tabledata.get("lldpRemPort")
        remMan = tabledata.get("lldpRemMan")
        rm = self.relMap()
        if not remPort:
            log.info("no LLDP information available")
            return rm
        if not locPort:
            log.info("LLDP no local Ports found")
            return rm
        # prepare remIp
        remIps = {}
        for id, remote in remMan.items():
            # ignoring multiple mgmt ips and multiple time entries,
            # just keep last you find
            idx = id.split(".")[1]
            ip = ".".join(id.split(".")[-4:])
            remIps[idx] = ip
        for id, port in remPort.items():
            # extract the local index
            idx = id.split(".")[1]
            locDesc = locPort[idx].get("desc", "unknown")
            remSys = port.get("sys", "unknown")
            remDesc = port.get("desc", "unknown")
            remIp = remIps.get(idx, "")
            om = self.processLink(log, idx, locDesc, remSys, remDesc, remIp)
            rm.append(om)
        return rm

    def processLink(self, log, locIdx, locDesc, remSys, remDesc, remIp):
        log.info('found a link %s -> %s:%s' % (locDesc, remSys, remDesc))
        om = self.objectMap()
        om.id = locIdx
        om.title = locDesc
        om.locPortDesc = locDesc
        om.locIndex = locIdx
        om.remPortDesc = remDesc
        om.remSysName = remSys
        om.remMgmtAddr = remIp
        return om
