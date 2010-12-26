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

$Id: ProcessMap.py,v 1.6 2010/10/14 20:17:12 egor Exp $"""

__version__ = '$Revision: 1.5 $'[11:-2]

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
        rm = self.relMap()
        for instance in results.get("Win32_Process", []):
            try:
                om = self.objectMap(instance)
                if not getattr(om, 'procName', False): 
                    log.warning("Skipping process with no name")
                    continue
                parameters = getattr(om, 'parameters', None)
                if parameters is None: om.parameters = '' #om.procName
#                om.parameters = ''
#                if parameters.startswith('"'):
#                    parameters = parameters.split('"', 2)
#                    if len(parameters) > 2: om.parameters = parameters[2]
#                else:
#                    parameters = parameters.split(' ', 1)
#                    if len(parameters) > 1: om.parameters = parameters[1]
                rm.append(om)
            except AttributeError:
                continue
        if not rm:
            log.warning("No process information from Win32_Process class")
            return None
        return rm
