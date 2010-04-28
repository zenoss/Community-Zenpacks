
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass

class ZenPack(ZenPackBase):
    """ NWMon loader
    """
    packZProperties = [
            ('zNWFileSystemMapIncludeNames', '', 'string'),
            ]

    def install(self, app):
        if not hasattr(self.dmd.Devices.Server, 'NetWare'):
            manage_addDeviceClass(self.dmd.Devices.Server, 'NetWare')
        dc = self.dmd.Devices.Server.NetWare
        dc.description = 'Novell NetWare Servers'
        dc.devtypes = ['SNMP',]
        dc.zIcon = '/zport/dmd/server-netware.png'
        dc.zLinks = "<a href='https://${here/manageIp}:8009' target='_'>Novell Remote Manager</a> <a href='https://${here/manageIp}/nps' target='_'>iManager</a>"
        dc.zCollectorPlugins = self.dmd.Devices.Server.zCollectorPlugins + [
                                                            'community.snmp.NWDeviceMap',
                                                            'community.snmp.NWFileSystemMap']
        if not hasattr(self.dmd.Devices.Server.NetWare, 'NCS'):
            manage_addDeviceClass(self.dmd.Devices.Server.NetWare, 'NCS')
        nwcs = self.dmd.Devices.Server.NetWare.NCS
        nwcs.description = 'Novell Cluster Virtual Resources'
        nwcs.devtypes = ['SNMP',]
        nwcs.zCollectorPlugins = ['zenoss.snmp.NewDeviceMap',
                                'zenoss.snmp.DeviceMap',
                                'zenoss.snmp.IpServiceMap',
                                'zenoss.snmp.HRSWRunMap',
                                'community.snmp.Interface2IPMap',
                                'community.snmp.NWFileSystemMap',
                                ]
        ZenPackBase.install(self, app)
        dc.zNWFileSystemMapIncludeNames = '^SYS'
        nwcs.zNWFileSystemMapIncludeNames = '^VOLUME_NAME'
