################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """InterfaceMap

Gather IP network interface information from WMI, and 
create DMD interface objects

$Id: InterfaceMap.py,v 1.6 2010/12/20 21:54:31 egor Exp $"""

__version__ = '$Revision: 1.6 $'[11:-2]

import re
import types
from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin

def prepId(id, subchar='_'):
    """
    Make an id with valid url characters. Subs [^a-zA-Z0-9-_,.$\(\) ]
    with subchar.  If id then starts with subchar it is removed.

    @param id: user-supplied id
    @type id: string
    @return: valid id
    @rtype: string
    """
    _prepId = re.compile(r'[^a-zA-Z0-9-_,.$ ]').sub
    _cleanend = re.compile(r"%s+$" % subchar).sub
    if id is None: 
        raise ValueError('Ids can not be None')
    if type(id) not in types.StringTypes:
        id = str(id)
    id = _prepId(subchar, id)
    while id.startswith(subchar):
        if len(id) > 1: id = id[1:]
        else: id = "-"
    id = _cleanend("",id)
    id = id.strip()
    return str(id)


class InterfaceMap(WMIPlugin):
    """
    Map IP network names and aliases to DMD 'interface' objects
    """
    maptype = "InterfaceMap" 
    compname = "os"
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"
    deviceProperties = \
                WMIPlugin.deviceProperties + ('zInterfaceMapIgnoreNames',
                                               'zInterfaceMapIgnoreTypes',
                                               'zInterfaceMapIgnoreIpAddresses')

    tables = {
            "Win32_NetworkAdapterConfiguration":
                (
                "Win32_NetworkAdapterConfiguration",
                None,
                "root/cimv2",
                    {
                    'Description':'interfaceName',
                    'Index':'snmpindex',
                    'InterfaceIndex':'ifindex',
                    'IPAddress':'_setIpAddresses',
                    'IPEnabled':'_ipenabled',
                    'MTU':'mtu',
                    }
                ),
            "Win32_NetworkAdapter":
                (
                "Win32_NetworkAdapter",
                None,
                "root/cimv2",
                    {
                    'AdapterType':'type',
                    'DeviceID':'snmpindex',
#                    'InterfaceIndex':'ifindex',
                    'MACAddress':'macaddress',
                    'MaxSpeed':'speed',
                    'NetConnectionStatus':'operStatus',
                    'StatusInfo':'adminStatus',
                    }
                ),
            "Win32_PerfRawData_Tcpip_NetworkInterface":
                (
                "Win32_PerfRawData_Tcpip_NetworkInterface",
                None,
                "root/cimv2",
                    {
                    'CurrentBandwidth':'speed',
                    'Name':'Name',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        dontCollectIntNames = getattr(device, 'zInterfaceMapIgnoreNames', None)
        dontCollectIntTypes = getattr(device, 'zInterfaceMapIgnoreTypes', None)
        dontCollectIpAddresses = getattr(device, 'zInterfaceMapIgnoreIpAddresses', None)
        rm = self.relMap()
        if (dontCollectIpAddresses and re.search(dontCollectIpAddresses,
                                device.manageIp)):
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
        interfaceStat = {}
        interfaceSpeed = {}
        for instance in results.get("Win32_PerfRawData_Tcpip_NetworkInterface", []):
            try:
                key = prepId(instance['Name'])
                interfaceStat[key] = instance['Name']
                interfaceSpeed[key] = instance['speed']
            except: continue
        interfaceConf = {}
        for instance in results.get("Win32_NetworkAdapter", []):
            key = instance.pop('snmpindex')
            try: interfaceConf[int(key)] = instance
            except: continue
        for instance in results.get("Win32_NetworkAdapterConfiguration", []):
            if not instance['_ipenabled']: continue
            try:
                instance.update(interfaceConf.get(int(instance['snmpindex']),{}))
                if not instance.get('type', None): continue
                om = self.objectMap(instance)
                if dontCollectIntNames and re.search(dontCollectIntNames,
                                                            om.interfaceName):
                    log.debug("Interface %s matched the zInterfaceMapIgnoreNames zprop '%s'" % (
                                om.interfaceName, getattr(device, 'zInterfaceMapIgnoreNames')))
                    continue
                if dontCollectIntTypes and re.search(dontCollectIntTypes,
                                                            om.type):
                    log.debug( "Interface %s type %s matched the zInterfaceMapIgnoreTypes zprop '%s'" % (
                                om.interfaceName, om.type, getattr(device, 'zInterfaceMapIgnoreTypes')))
                    continue
                om.id = prepId(om.interfaceName)
                om.interfaceName = interfaceStat.get(om.id, None) or om.interfaceName
                om.setIpAddresses = []
                for ip in om._setIpAddresses:
                    if (dontCollectIpAddresses
                        and re.search(dontCollectIpAddresses, ip)):
                        continue
                    # ignore IPv6 Addresses
                    if ip.__contains__(':'): continue
                    om.setIpAddresses.append(ip)
                if not om.ifindex: om.ifindex = om.snmpindex
                om.snmpindex = 'Win32_NetworkAdapter.DeviceID="%s"'%om.snmpindex
                if om.speed == 0: om.speed = interfaceSpeed.get(om.id, 0)
                if om.operStatus in [None, 2, 9]: om.operStatus = 1
                else: om.operStatus = 2
                if om.adminStatus in [0, 2]: om.adminStatus = 1
                else:om.adminStatus = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm
