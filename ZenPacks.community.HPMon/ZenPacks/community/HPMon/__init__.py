
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
    """ HPMon loader
    """

    packZProperties = [
            ('zHPExpansionCardMapIgnorePci', 'False', 'boolean'),
            ]


    def install(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
	    if not hasattr(devReports, 'HP ProLiant Reports'):
                dc = rClass('HP ProLiant Reports', None)
                devReports._setObject('HP ProLiant Reports', dc)
        ZenPackBase.install(self, app)

    def upgrade(self, app):
        from ZenPacks.community.deviceAdvDetail.thresholds.StatusThreshold import StatusThreshold
        for t in self.dmd.Devices.getAllRRDTemplates():
            for gt in t.thresholds():
                if isinstance(gt, StatusThreshold): continue
                if gt.id != '%s status'%t.id: continue
                template.thresholds.removeRelation(gt)
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
	    if not hasattr(devReports, 'HP ProLiant Reports'):
                dc = rClass('HP ProLiant Reports', None)
                devReports._setObject('HP ProLiant Reports', dc)
        ZenPackBase.upgrade(self, app)

    def remove(self, app, junk):
        ZenPackBase.remove(self, app, junk)
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
	    if hasattr(devReports, 'HP ProLiant Reports'):
                devReports._delObject('HP ProLiant Reports')
