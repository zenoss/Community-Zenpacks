################################################################################
#
# This program is part of the LinMon_WBEM Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""ProcessorMap

ProcessorMap maps the CIM_Processor class to cpus objects

$Id: ProcessorMap.py,v 1.0 2010/02/21 20:29:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs
from Products.ZenUtils.Utils import prepId


class ProcessorMap(WBEMPlugin):

    maptype = "ProcessorMap"
    compname = "hw"
    relname = "cpus"
    modname = "Products.ZenModel.CPU"

    tables = {
            "Linux_Processor":
                (
                "Linux_Processor",
                None,
                "root/cimv2",
                    {
                    'DeviceID':'id',
                    'ElementName':'_name',
                    'MaxClockSpeed':'clockspeed',
                    }
                ),
            }
    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        instances = results["Linux_Processor"]
        if not instances: return
        for instance in instances:
            om = self.objectMap(instance)
            try:
                om.socket = om.id
                om.id = prepId(om.id)
                manuf = om._name.split()[0]
                if manuf not in EnterpriseOIDs.values():
                    manuf = 'Unknown'
                om.setProductKey = MultiArgs(om._name, manuf)
            except AttributeError:
                continue
            rm.append(om)
        return rm
