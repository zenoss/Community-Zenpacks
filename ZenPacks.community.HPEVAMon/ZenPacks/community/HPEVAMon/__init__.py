
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Acquisition import aq_base
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass


class ZenPack(ZenPackBase):
    """ HPEVAMon loader
    """

    dcProperties = {
        '/CIM/HPEVA': {
            'description': ('', 'string'),
            'zCollectorPlugins': (
                (
                'community.wbem.HPEVADeviceMap',
                'community.wbem.HPEVAStorageDiskEnclosureMap',
                'community.wbem.HPEVAStoragePoolMap',
                'community.wbem.HPEVAStorageProcessorCardMap',
                'community.wbem.HPEVAHostFCPortMap',
                'community.wbem.HPEVADiskDriveMap',
                'community.wbem.HPEVAConsistencySetMap',
                'community.wbem.HPEVAStorageVolumeMap',
                ),
                'lines',
            ),
            'zLinks': ("<a href='https://${here/zWbemProxy}:2372' target='_'>Command View EVA</a>", 'string'),
            'zPythonClass': ('ZenPacks.community.HPEVAMon.HPEVADevice', 'string'),
            'zSnmpMonitorIgnore': (True, 'boolean'),
            'zWbemMonitorIgnore': (False, 'boolean'),
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
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
	    if not hasattr(devReports, 'HP EVA Reports'):
                dc = rClass('HP EVA Reports', None)
                devReports._setObject('HP EVA Reports', dc)
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
	    if not hasattr(devReports, 'HP EVA Reports'):
                dc = rClass('HP EVA Reports', None)
                devReports._setObject('HP EVA Reports', dc)
        for devClass, properties in self.dcProperties.iteritems():
            self.addDeviceClass(app, devClass, properties)
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        for dcp in self.dcProperties.keys():
            try:
                dc = app.zport.dmd.Devices.getOrganizer(dcp)
                dc._delProperty('zCollectorPlugins')
                dc._delProperty('zPythonClass')
                dc._delProperty('zSnmpMonitorIgnore')
                dc._delProperty('zWbemMonitorIgnore')
            except: continue
        ZenPackBase.remove(self, app, leaveObjects)
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
	    if hasattr(devReports, 'HP EVA Reports'):
                devReports._delObject('HP EVA Reports')
