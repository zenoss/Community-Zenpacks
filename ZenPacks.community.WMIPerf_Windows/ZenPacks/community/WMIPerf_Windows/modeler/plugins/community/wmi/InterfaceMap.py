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

$Id: InterfaceMap.py,v 1.0 2010/01/14 10:55:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

import re
from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId

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
                                               'zInterfaceMapIgnoreTypes')

    tables = {
            "Win32_NetworkAdapterConfiguration":
                (
                "Win32_NetworkAdapterConfiguration",
                None,
                "root/cimv2",
                    {
		    'Description':'interfaceName',
                    'InterfaceIndex':'ifindex',
                    'IPAddress':'setIpAddresses',
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
		    '__path':'snmpindex',
		    'AdapterType':'type',
                    'InterfaceIndex':'ifindex',
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
                    '__path':'snmpindex',
                    'Name':'Name',
		    }
                ),
            }


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        dontCollectIntNames = getattr(device, 'zInterfaceMapIgnoreNames', None)
        dontCollectIntTypes = getattr(device, 'zInterfaceMapIgnoreTypes', None)
        rm = self.relMap()
	interfaceStat = {}
	interfaceSpeed = {}
	instances = results["Win32_PerfRawData_Tcpip_NetworkInterface"]
	if instances:
            for instance in instances:
	        try:
		    key = prepId(instance['Name'])
		    interfaceStat[key] = instance['snmpindex']
		    interfaceSpeed[key] = instance['speed']
	        except: continue
	interfaceConf = {}
	instances = results["Win32_NetworkAdapter"]
	if instances:
            for instance in instances:
	        key = instance.pop('ifindex')
	        try: interfaceConf[key] = instance
	        except: continue
	instances = results["Win32_NetworkAdapterConfiguration"]
	if not instances: return
        for instance in instances:
	    if not instance['_ipenabled']: continue
	    try:
	        instance.update(interfaceConf.get(instance['ifindex'],{}))
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
		om.snmpindex = interfaceStat.get(om.id, 0)
		if om.speed == 0: om.speed = interfaceSpeed.get(om.id, 0)
		if om.operStatus == 2 or om.operStatus == 9: om.operStatus = 1
		else: om.operStatus = 2
		if om.adminStatus == 2 or om.adminStatus == 0: om.adminStatus = 1
		else:om.adminStatus = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm
