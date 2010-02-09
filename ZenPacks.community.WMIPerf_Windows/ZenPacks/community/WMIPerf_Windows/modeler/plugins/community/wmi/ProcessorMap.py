################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""ProcessorMap

ProcessorMap maps the CIM_Processor class to cpus objects

$Id: ProcessorMap.py,v 1.0 2010/01/14 09:35:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.ZenUtils.Utils import prepId

import re
PROCCACHELEVEL = re.compile(r'.*(\d).*(\d).*')

def getManufacturerAndModel(key):
    """
    Attempts to parse accurate manufacturer and model information of a CPU from
    the single product string passed in.

    @param key: A product key. Hopefully containing manufacturer and model name.
    @type key: string
    @return: A MultiArgs object containing the model and manufacturer.
    @rtype: Products.DataDollector.plugins.DataMaps.MultiArgs
    """
    cpuDict = {
        'Intel': '(Intel|Pentium|Xeon)',
        'AMD': '(AMD|Opteron|Athlon|Sempron|Phenom|Turion)',
        }

    for manufacturer, regex in cpuDict.items():
        if re.search(regex, key):
            return MultiArgs(key, manufacturer)

    # Revert to default behavior if no specific match is found.
    return MultiArgs(key, "Unknown")


class ProcessorMap(WMIPlugin):

    maptype = "ProcessorMap"
    compname = "hw"
    relname = "cpus"
    modname = "Products.ZenModel.CPU"

    tables = {
            "Win32_Processor":
                (
                "Win32_Processor",
                None,
                "root/cimv2",
                    {
                    '__path':'snmpindex',
                    'DeviceID':'id',
                    'Name':'_name',
                    'CurrentVoltage':'voltage',
                    'MaxClockSpeed':'clockspeed',
                    'ExternalBusClockSpeed':'_extspeed',
                    'ExtClock':'extspeed',
                    'SocketDesignation':'socket'
                    }
                ),
            "Win32_CacheMemory":
                (
                "Win32_CacheMemory",
                None,
                "root/cimv2",
                    {
                    'MaxCacheSize':'maxCacheSize',
                    'Purpose':'purpose',
                    }
                ),
            }

    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        cacheMem = {}
        instances = results["Win32_CacheMemory"]
        for instance in instances:
            try:
                purpose = PROCCACHELEVEL.search(instance['purpose']).groups()
                if purpose[0] not in cacheMem:
                    cacheMem[purpose[0]] = {}
                cacheMem[purpose[0]][purpose[1]] = instance['maxCacheSize']
            except: continue
        instances = results["Win32_Processor"]
        if not instances: return
        for instance in instances:
            om = self.objectMap(instance)
            try:
                om.id = prepId(om.id)
                om.socket = om.id[3:]
                if not om.extspeed: om.extspeed = om._extspeed
                cache = cacheMem.get(om.socket, {})
                om.cacheSizeL1 = cache.get('1', 0)
                om.cacheSizeL2 = cache.get('2', 0)
#                om.cacheSizeL3 = cache.get('3', 0)
                om.setProductKey = getManufacturerAndModel(om._name)
            except AttributeError:
                continue
            rm.append(om)
        return rm
