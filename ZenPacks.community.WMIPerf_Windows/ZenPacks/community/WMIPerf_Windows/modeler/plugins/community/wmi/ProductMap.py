################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""ProductMap

ProductMap finds various software packages installed on a device.

$Id: ProductMap.py,v 1.0 2010/01/29 16:43:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.EnterpriseOIDs import EnterpriseOIDs


class ProductMap(WMIPlugin):

    maptype = "SoftwareMap"
    modname = "Products.ZenModel.Software"
    relname = "software"
    compname = "os"

    tables = {
            "Win32_Product":
                (
                "Win32_Product",
                None,
                "root/cimv2",
                    {
                    'Name':'name',
                    'Description':'description',
                    'InstallDate2':'setInstallDate',
                    'Vendor':'_vendor',
                    'Version':'version',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        instances = results["Win32_CacheMemory"]
        rm = self.relMap()
        for instance in instances:
            om = self.objectMap(instance)
            om.id = self.prepId(om.name)
            om._vendor = om._vendor.split()[0]
            if om._vendor not in EnterpriseOIDs.values():
                om._vendor = 'Unknown'
            om.setProductKey = MultiArgs(om.name, om._vendor)
            if hasattr(om, 'setInstallDate'):
                om.setInstallDate = "%d/%02d/%02d %02d:%02d:%02d" % om.setInstallDate[:6]
            rm.append(om)
        return rm
