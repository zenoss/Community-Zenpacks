################################################################################
#
# This program is part of the VirtualIP Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""VirtualInterface

VirtualInterface maps the interface and ip tables to interface objects

$Id: VirtualInterfaceMap.py,v 1.0 2009/02/10 10:37:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

import re

import Globals
from Products.ZenUtils.Utils import cleanstring, unsigned
from Products.DataCollector.plugins.zenoss.snmp.InterfaceMap import InterfaceMap

class VirtualInterfaceMap(InterfaceMap):

    deviceProperties = \
        InterfaceMap.deviceProperties + ('zInterfaceMapIgnoreIpAddresses',)

    def process(self, device, results, log):
        """collect snmp information from this device"""
        getdata, tabledata = results
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        dontCollectIpAddresses = getattr(device, 'zInterfaceMapIgnoreIpAddresses', None)
        if (dontCollectIpAddresses 
            and re.search(dontCollectIpAddresses, device.manageIp)):
	    om = self.objectMap()
	    om.id = self.prepId("Virtual IP Address")
	    om.title = om.id
	    om.interfaceName = om.id
	    om.type = "softwareLoopback"
	    om.speed = 1000000000
	    om.mtu = 1500
	    om.ifindex = "1"
	    om.adminStatus = 1
	    om.operStatus = 1
	    om.monitor = False
            om.setIpAddresses = [device.manageIp, ]
	    rm.append(om)
            return rm

        iptable = tabledata.get("ipAddrTable") \
            or tabledata.get("ipNetToMediaTable")
        iftable = tabledata.get("iftable")
        ifalias = tabledata.get("ifalias")
        if iptable is None or iftable is None: return
        if not ifalias: ifalias = {}

        # add interface alias (cisco description) to iftable
        for ifidx, data in ifalias.items():
            if not iftable.has_key(ifidx): continue
            iftable[ifidx]['description'] = data.get('description', '')
            # if we collect ifAlias name use it
            # this is in the map subclass InterfaceAliasMap
            id = data.get('id', None)
            if id:
                iftable[ifidx]['id'] = id
            iftable[ifidx]['description'] = data.get('description', '')
            # handle 10GB interfaces using IF-MIB::ifHighSpeed
            speed = iftable[ifidx].get('speed',0)
            if speed == 4294967295L or speed < 0:
                try: iftable[ifidx]['speed'] = data['highSpeed']*1e6
                except KeyError: pass

        for ifidx, data in iftable.items():
            try:
                data['speed'] = unsigned(data['speed'])
            except KeyError:
                pass

        omtable = {}
        for ip, row in iptable.items():
            #FIXME - not getting ifindex back from HP printer
            if not row.has_key("ifindex"): continue

            # Fix data up if it is from the ipNetToMediaTable.
            if len(ip.split('.')) == 5:
                if row['iptype'] != 1: continue
                ip = '.'.join(ip.split('.')[1:])
                row['netmask'] = '255.255.255.0'
            strindex = str(row['ifindex'])
            if not omtable.has_key(strindex) and not iftable.has_key(strindex):
                log.warn("skipping %s points to missing ifindex %s",
                            row.get('ipAddress',""), row.get('ifindex',""))
                continue                                 
            if not omtable.has_key(strindex):
                om = self.processInt(log, device, iftable[strindex])
                if not om: continue
                rm.append(om)
                omtable[strindex] = om
                del iftable[strindex]
            elif omtable.has_key(strindex): 
                om = omtable[strindex]
            else:
                log.warn("ip points to missing ifindex %s skipping", strindex) 
                continue
            if not hasattr(om, 'setIpAddresses'): om.setIpAddresses = []
            if row.has_key('ipAddress'): ip = row['ipAddress']
            if (dontCollectIpAddresses 
                and re.search(dontCollectIpAddresses, ip)):
                continue
            if row.has_key('netmask'): ip = ip + "/" + str(self.maskToBits(row['netmask'].strip()))
            om.setIpAddresses.append(ip)
            #om.ifindex = row.ifindex #FIXME ifindex is not set!

        for iface in iftable.values():
            om = self.processInt(log, device, iface)
            if om: rm.append(om)
        return rm
