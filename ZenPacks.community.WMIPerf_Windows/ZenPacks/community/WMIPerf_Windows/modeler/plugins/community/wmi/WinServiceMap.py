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

$Id: WinServiceMap.py,v 1.3 2010/12/21 18:48:29 egor Exp $"""

__version__ = '$Revision: 1.3 $'[11:-2]


from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin

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
                    'AcceptPause':'_acceptPause',
                    'AcceptStop':'_acceptStop',
                    'Caption':'_description',
                    'Name':'_name',
                    'PathName':'pathName',
                    'ServiceType':'serviceType',
                    'StartMode':'startMode',
                    'StartName':'startName',
                    'State':'_state',
                    }
                ),
            }


    def process(self, device, results, log):
        """Collect win service info from this device.
        """
        log.info('Processing WinServices for device %s' % device.id)
        rm = self.relMap()
        for instance in results.get("Win32_Service", []):
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om._name)
                om.setServiceClass = {'name':om._name,
                                      'description':om._description,
                                      }
                rm.append(om)
            except: continue
        return rm

