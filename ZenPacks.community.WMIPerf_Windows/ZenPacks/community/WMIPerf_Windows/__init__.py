
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Acquisition import aq_base
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass
from Products.ZenModel.OperatingSystem import OperatingSystem

def logicalProcessors(self):
    return round(self.device().cacheRRDValue('LoadPercentage_count', 1))

if not hasattr(OperatingSystem, 'logicalProcessors'):
    OperatingSystem.logicalProcessors = logicalProcessors

class ZenPack(ZenPackBase):
    """ WMIPerf_Windows loader
    """

    dcProperties = {
        '/CIM/WMI': {
            'description': ('', 'string'),
#            'devtypes': (['WMI', 'WBEM'], 'lines'),
            'zCollectorPlugins': (
                (
                'community.wmi.NewDeviceMap',
                'community.wmi.DeviceMap',
                'community.wmi.ProcessorMap',
                'community.wmi.InterfaceMap',
                'community.wmi.FileSystemMap',
                'community.wmi.ProcessMap',
                'community.wmi.RouteMap',
                'community.wmi.DiskDriveMap',
                'community.wmi.WinServiceMap',
                'zenoss.portscan.IpServiceMap',
                ),
                'lines',
            ),
            'zWmiMonitorIgnore': (False, 'boolean'),
            'zIcon': ('/zport/dmd/img/icons/server-windows.png', 'string'),
        },
        '/CIM/WMI/Win2000': {
            'description': ('', 'string'),
#            'devtypes': (['WMI', 'WBEM'], 'lines'),
            'zCollectorPlugins': (
                (
                'community.wmi.NewDeviceMap',
                'community.wmi.DeviceMap',
                'community.wmi.ProcessorMap',
                'community.wmi.InterfaceMap',
                'community.wmi.FileSystemMap',
                'community.wmi.ProcessMap',
                'community.wmi.DiskDriveMap',
                'community.wmi.WinServiceMap',
                'zenoss.portscan.IpServiceMap',
                ),
                'lines',
            ),
            'zWmiMonitorIgnore': (False, 'boolean'),
            'zIcon': ('/zport/dmd/img/icons/server-windows.png', 'string'),
        },
    }

    def addDeviceClass(self, app, dcp, properties):
        try:
            dc = app.zport.dmd.Devices.getOrganizer(dcp)
        except:
            dcp, newdcp = dcp.rsplit('/', 1)
            dc = self.addDeviceClass(app, dcp, self.dcProperties.get(dcp, {}))
            manage_addDeviceClass(dc, newdcp)
            dc = app.zport.dmd.Devices.getOrganizer("%s/%s"%(dcp, newdcp))
            dc.description = ''
        for prop, value in properties.iteritems():
            if not hasattr(aq_base(dc), prop):
                dc._setProperty(prop, value[0], type = value[1])
        return dc

    def install(self, app):
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        for dcp in self.dcProperties.keys():
            try:
                dc = app.zport.dmd.Devices.getOrganizer(dcp)
                dc._delProperty('zCollectorPlugins')
            except: continue
        ZenPackBase.remove(self, app, leaveObjects)
