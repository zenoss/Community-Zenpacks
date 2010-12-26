
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ DellMon loader
    """
    packZProperties = [
            ('zDellExpansionCardMapIgnorePci', False, 'boolean'),
            ]

    def install(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
	    if not hasattr(devReports, 'Dell PowerEdge Reports'):
                dc = rClass('Dell PowerEdge Reports', None)
                devReports._setObject('Dell PowerEdge Reports', dc)
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
	    if not hasattr(devReports, 'Dell PowerEdge Reports'):
                dc = rClass('Dell PowerEdge Reports', None)
                devReports._setObject('Dell PowerEdge Reports', dc)
        ZenPackBase.upgrade(self, app)

    def remove(self, app, junk):
        ZenPackBase.remove(self, app, junk)
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
	    if hasattr(devReports, 'Dell PowerEdge Reports'):
                devReports._delObject('Dell PowerEdge Reports')
