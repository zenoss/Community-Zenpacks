################################################################################
#
# This program is part of the LinMon_WBEM Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""LinCPUMap

LinCPUMap maps the instances of Linux_Processor CMPI class to cpu objects

$Id: LinCPUMap.py,v 1.0 2009/08/01 15:57:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.ZenUtils.Utils import prepId

class LinCPUMap(WBEMPlugin):

    maptype = "LinCPUMap"
    compname = "hw"
    relname = "cpus"
    modname = "Products.ZenModel.CPU"
    
    
    def queries(self):
        return {
            "Linux_Processor":
                (
                "linux_Processor",
                None,
                "root/cimv2",
                None,
                ),
            }
    
    def process(self, device, results, log):
        """collect wbem information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for cpu in results["Linux_Processor"]:
            om = self.objectMap()
            om.id = prepId(cpu['DeviceID'])
            om.slot = cpu['DeviceID']
            om.setProductKey = cpu['ElementName']
            om.clockspeed = long(cpu['MaxClockSpeed'])
            rm.append(om)
        return rm

