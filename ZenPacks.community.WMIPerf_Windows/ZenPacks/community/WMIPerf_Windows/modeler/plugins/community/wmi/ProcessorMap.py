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

$Id: ProcessorMap.py,v 1.2 2010/04/21 18:53:05 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

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
    modname = "ZenPacks.community.WMIPerf_Windows.Win32Processor"

    tables = {
            "Win32_Processor":
                (
                "Win32_Processor",
                None,
                "root/cimv2",
                    {
                    '__path':'snmpindex',
                    'CpuStatus':'_status',
                    'DeviceID':'id',
                    'Name':'_name',
                    'CurrentVoltage':'voltage',
                    'MaxClockSpeed':'clockspeed',
                    'ExternalBusClockSpeed':'_extspeed',
                    'ExtClock':'extspeed',
                    'NumberOfCores':'core',
                    'SocketDesignation':'socket'
                    }
                ),
            "Win32_CacheMemory":
                (
                "Win32_CacheMemory",
                None,
                "root/cimv2",
                    {
                    'BlockSize':'BlockSize',
                    'Level':'level',
                    'NumberOfBlocks':'Blocks',
                    }
                ),
            }

    def processCacheMemory(self, instances):
        """processing CacheMemory table"""
        cache = {1:0, 2:0, 3:0}
        for inst in instances:
            try:
                level = int(inst['level']) - 2
                cache[level]=inst['BlockSize']*inst['Blocks']/1024+cache[level]
            except: continue
        return cache


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        cache = self.processCacheMemory(results.get("Win32_CacheMemory", None))
        instances = results["Win32_Processor"]
        if not instances: return
        cores = 1
        sockets = []
        if not instances[0]['core']:
            for instance in instances:
                if instance['socket'] in sockets: continue
                sockets.append(instance['socket'])
            sockets = len(sockets)
            for level in (1, 2, 3): cache[level] = cache[level] / sockets
            cores = len(instances) / sockets
        sockets = []
        for instance in instances:
            if instance['socket'] in sockets: continue
            sockets.append(instance['socket'])
            if not instance['core']: instance['core'] = cores
            om = self.objectMap(instance)
            if om._status == 0: continue
            try:
                om.id = prepId(om.id)
                om.socket = om.id[3:]
                if not om.extspeed: om.extspeed = om._extspeed
                om.cacheSizeL1 = cache.get(1, 0)
                om.cacheSizeL2 = cache.get(2, 0)
#                om.cacheSizeL3 = cache.get(3, 0)
                om.setProductKey = getManufacturerAndModel(om._name)
            except AttributeError:
                continue
            rm.append(om)
        return rm
