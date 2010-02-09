################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""ProcessMap

ProcessMap finds various software packages installed on a device.

$Id: ProcessMap.py,v 1.0 2010/02/09 17:18:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin


class ProcessMap(WMIPlugin):

    maptype = "ProcessMap"
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"
    classname = 'createFromObjectMap'

    tables = {
            "Win32_Process":
                (
                "Win32_Process",
                None,
                "root/cimv2",
                    {
                    'CommandLine':'parameters',
                    'Name':'procName',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        instances = results["Win32_Process"]
        rm = self.relMap()
        for instance in instances:
            om = self.objectMap(instance)
            if not getattr(om, 'procName', False): 
                log.warn("Skipping process with no name")
                continue
            parameters = getattr(om, 'parameters', None)
            if parameters is None: continue
            parameters = parameters.split(' ', 1)
            if len(parameters) > 1:
                om.parameters = parameters[1]
            else:
                om.parameters = ''
            rm.append(om)

        if not rm:
            log.warning("No process information from hrSWRunEntry %s",
                        HRSWRUNENTRY)
            return None

        return rm
