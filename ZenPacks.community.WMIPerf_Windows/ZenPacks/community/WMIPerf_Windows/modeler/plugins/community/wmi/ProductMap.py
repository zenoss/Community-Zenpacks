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

$Id: ProductMap.py,v 1.1 2010/02/22 13:38:23 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

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
                    'Name':'setProductKey',
                    'Description':'description',
                    'InstallDate':'_setInstallDate',
                    'InstallDate2':'setInstallDate',
                    'Vendor':'_vendor',
#                    'Version':'version',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        instances = results["Win32_Product"]
        rm = self.relMap()
        for instance in instances:
            om = self.objectMap(instance)
            om.id = self.prepId(om.setProductKey)
            om._vendor = om._vendor.split()[0]
            if om._vendor not in EnterpriseOIDs.values():
                om._vendor = 'Unknown'
            om.setProductKey = MultiArgs(om.setProductKey, om._vendor)
            if getattr(om, 'setInstallDate', None):
                om.setInstallDate = "%d/%02d/%02d %02d:%02d:%02d" % (
                                                        om.setInstallDate[:6])
            elif getattr(om, '_setInstallDate', None):
                om.setInstallDate = "%s/%s/%s 00:00:00" % (
                                                        om._setInstallDate[:4],
                                                        om._setInstallDate[4:6],
                                                        om._setInstallDate[6:8])
            rm.append(om)
        return rm
