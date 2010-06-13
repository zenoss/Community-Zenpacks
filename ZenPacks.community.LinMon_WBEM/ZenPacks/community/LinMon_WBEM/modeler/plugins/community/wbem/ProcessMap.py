################################################################################
#
# This program is part of the LinMon_WBEM Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""ProcessMap

ProcessMap finds various software packages installed on a device.

$Id: ProcessMap.py,v 1.0 2010/02/21 21:35:43 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.WBEMDataSource.WBEMPlugin import WBEMPlugin


class ProcessMap(WBEMPlugin):

    maptype = "ProcessMap"
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"
    classname = 'createFromObjectMap'

    tables = {
            "Linux_UnixProcess":
                (
                "Linux_UnixProcess",
                None,
                "root/cimv2",
                    {
                    'Parameters':'parameters',
                    'Name':'procName',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect WBEM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        instances = results["Linux_UnixProcess"]
        rm = self.relMap()
        for instance in instances:
            om = self.objectMap(instance)
            if not getattr(om, 'procName', False): 
                log.warn("Skipping process with no name")
                continue
            om.parameters.pop(0)
            om.parameters = ' '.join(om.parameters)
            
            rm.append(om)

        if not rm:
            log.warning("No process information from Linux_UnixProces")
            return None

        return rm
