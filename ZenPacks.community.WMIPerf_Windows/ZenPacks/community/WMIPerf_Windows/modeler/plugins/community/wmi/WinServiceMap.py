################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """WinServiceMap

WinServiceMap gathers status of Windows services

$Id: WinServiceMap.py,v 1.0 2010/02/17 10:58:48 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.ZenUtils.Utils import prepId

class WinServiceMap(WMIPlugin):

    maptype = "WinServiceMap"
    compname = "os"
    relname = "winservices"
    modname = "Products.ZenModel.WinService"

    tables = {
            "Win32_Service":
                (
                "Win32_Service",
                None,
                "root/cimv2",
                    {
                    'AcceptPause':'acceptPause',
                    'AcceptStop':'acceptStop',
                    'Caption':'description',
                    'Name':'_name',
                    'PathName':'pathName',
                    'ServiceType':'serviceType',
                    'StartMode':'startMode',
                    'StartName':'startName',
                    'State':'state',
                    }
                ),
            }


    def process(self, device, results, log):
        """Collect win service info from this device.
        """
        log.info('Processing WinServices for device %s' % device.id)
        instances = results["Win32_Service"]
        if not instances: return
        rm = self.relMap()
        for instance in instances:
            om = self.objectMap(instance)
            om.id = prepId(om._name)
            om.setServiceClass = {'name':om._name, 'description':om.description}
            rm.append(om)
        return rm

