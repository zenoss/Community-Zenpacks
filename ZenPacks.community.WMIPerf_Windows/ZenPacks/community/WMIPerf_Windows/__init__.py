
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
    """ WMIPerf_Windows loader
    """

    def install(self, app):
        try:
            dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM/Win")
        except:
            if not hasattr(app.zport.dmd.Devices.Server, 'WBEM'):
                manage_addDeviceClass(app.zport.dmd.Devices.Server, 'WBEM')
                dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM")
                dc.description = ''
                dc.devtypes = ['WMI', 'WBEM']
            if not hasattr(app.zport.dmd.Devices.Server.WBEM, 'Win'):
                manage_addDeviceClass(app.zport.dmd.Devices.Server.WBEM, 'Win')
                dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM/Win")
                dc.description = ''
                dc.devtypes = ['WMI', 'WBEM']
            else:
                dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM/Win")
        if not hasattr(aq_base(dc),'zCollectorPlugins'):
            dc._setProperty("zCollectorPlugins", 
                    (
                        'community.wmi.NewDeviceMap',
                        'community.wmi.DeviceMap',
                        'community.wmi.ProcessorMap',
                        'community.wmi.InterfaceMap',
                        'community.wmi.FileSystemMap',
                        'community.wmi.ProductMap',
                    ), type = 'lines')
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        try:
            dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM/Win")
        except:
            if not hasattr(app.zport.dmd.Devices.Server, 'WBEM'):
                manage_addDeviceClass(app.zport.dmd.Devices.Server, 'WBEM')
                dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM")
                dc.description = ''
                dc.devtypes = ['WMI', 'WBEM']
            if not hasattr(app.zport.dmd.Devices.Server.WBEM, 'Win'):
                manage_addDeviceClass(app.zport.dmd.Devices.Server.WBEM, 'Win')
                dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM/Win")
                dc.description = ''
                dc.devtypes = ['WMI', 'WBEM']
            else:
                dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM/Win")
        if not hasattr(aq_base(dc),'zCollectorPlugins'):
            dc._setProperty("zCollectorPlugins", 
                    (
                        'community.wmi.NewDeviceMap',
                        'community.wmi.DeviceMap',
                        'community.wmi.ProcessorMap',
                        'community.wmi.InterfaceMap',
                        'community.wmi.FileSystemMap',
                        'community.wmi.ProductMap',
                    ), type = 'lines')
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        try:
            dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM/Win")
            dc._delProperty('zCollectorPlugins')
        except: pass
        ZenPackBase.remove(self, app, leaveObjects)
