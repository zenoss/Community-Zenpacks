
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase


class ZenPack(ZenPackBase):

    newplugins = ('community.snmp.CiscoExpansionCardMap',
                  'community.snmp.CiscoFanMap',
                  'community.snmp.CiscoPowerSupplyMap',
                  'community.snmp.CiscoTemperatureSensorMap',
                 )

    def install(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
            if not hasattr(devReports, 'Cisco Reports'):
                dc = rClass('Cisco Reports', None)
                devReports._setObject('Cisco Reports', dc)
        ZenPackBase.install(self, app)
        dc = app.zport.dmd.Devices.getOrganizer('Network/Router/Cisco')
        cpl = list(getattr(dc, 'zCollectorPlugins'))
        for plugin in self.newplugins:
            if not plugin in cpl: cpl.append(plugin)
        dc.zCollectorPlugins = list(cpl)

    def upgrade(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
            if not hasattr(devReports, 'Cisco Reports'):
                dc = rClass('Cisco Reports', None)
                devReports._setObject('Cisco Reports', dc)
        ZenPackBase.upgrade(self, app)
        dc = app.zport.dmd.Devices.getOrganizer('Network/Router/Cisco')
        cpl = list(getattr(dc, 'zCollectorPlugins'))
        for plugin in self.newplugins:
            if not plugin in cpl: cpl.append(plugin)
        dc.zCollectorPlugins = list(cpl)

    def remove(self, app, leaveObjects=False):
        dc = app.zport.dmd.Devices.getOrganizer('Network/Router/Cisco')
        cpl = list(getattr(dc, 'zCollectorPlugins'))
        for plugin in self.newplugins:
            if plugin in cpl: cpl.remove(plugin)
        dc.zCollectorPlugins = list(cpl)
        ZenPackBase.remove(self, app, leaveObjects)
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            if hasattr(devReports, 'Cisco Reports'):
                devReports._delObject('Cisco Reports')
