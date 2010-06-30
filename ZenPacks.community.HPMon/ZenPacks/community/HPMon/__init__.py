
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


    def upgrade(self, app):
        from ZenPacks.community.deviceAdvDetail.thresholds.StatusThreshold import StatusThreshold
        for t in dmd.Devices.getAllRRDTemplates():
            for gt in t.thresholds():
                if isinstance(gt, StatusThreshold): continue
                if gt.id != '%s status'%t.id: continue
                template.thresholds.removeRelation(gt)
        ZenPackBase.upgrade(self, app)

