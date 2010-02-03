
import Globals
import os.path
import sys

from Products.CMFCore.DirectoryView import registerDirectory
skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())
libDir = os.path.join(os.path.dirname(__file__), 'lib')
if os.path.isdir(libDir):
    sys.path.append(libDir)

from Acquisition import aq_base
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.DeviceClass import manage_addDeviceClass

class ZenPack(ZenPackBase):
    """ WBEMDataSource loader
    """
    packZProperties = [
            ('zWbemMonitorIgnore', True, 'boolean'),
            ('zWbemPort', '5989', 'string'),
            ('zWbemProxy', '', 'string'),
            ('zWbemUseSSL', True, 'boolean'),
	    ]

    def install(self, app):
        if not hasattr(app.zport.dmd.Devices.Server, 'WBEM'):
            manage_addDeviceClass(app.zport.dmd.Devices.Server, 'WBEM')
        dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM")
	dc.description = ''
	dc.devtypes = ['WMI', 'WBEM']
        if not hasattr(aq_base(dc),'zWbemMonitorIgnore'):
	    dc._setProperty('zWbemMonitorIgnore', False, 'boolean')
        if not hasattr(app.zport.dmd.Events.Status, 'Wbem'):
            app.zport.dmd.Events.createOrganizer("/Status/Wbem")
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if not hasattr(app.zport.dmd.Devices.Server, 'WBEM'):
            manage_addDeviceClass(app.zport.dmd.Devices.Server, 'WBEM')
            dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM")
	    dc.description = ''
	    dc.devtypes = ['WMI', 'WBEM']
            if not hasattr(aq_base(dc),'zWbemMonitorIgnore'):
	        dc._setProperty('zWbemMonitorIgnore', False, 'boolean')
        if not hasattr(app.zport.dmd.Events.Status, 'Wbem'):
            app.zport.dmd.Events.createOrganizer("/Status/Wbem")
        ZenPackBase.upgrade(self, app)

    def remove(self, app, leaveObjects=False):
        try:
            dc = app.zport.dmd.Devices.getOrganizer("/Server/WBEM")
	    dc._delProperty('zWbemMonitorIgnore')
	except: pass
        ZenPackBase.remove(self, app, leaveObjects)
