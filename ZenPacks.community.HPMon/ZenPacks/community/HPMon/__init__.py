
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from ZenPacks.community.deviceAdvDetail.thresholds.StatusThreshold import StatusThreshold
from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
    """ HPMon loader
    """

    packZProperties = [
            ('zHPExpansionCardMapIgnorePci', 'False', 'boolean'),
	    ]

    compClasses = [ 'cpqDaCntlr',
                    'cpqDaLogDrv',
                    'cpqDaPhyDrv',
                    'cpqFcaCntlr',
                    'cpqFcaHostCntlr',
                    'cpqFcaLogDrv',
                    'cpqFcaPhyDrv',
                    'cpqFcTapeCntlr',
                    'cpqIdeAtaDisk',
                    'cpqIdeController',
                    'cpqIdeLogicalDrive',
                    'cpqNicIfPhysAdapter',
                    'cpqSasHba',
                    'cpqSasLogDrv',
                    'cpqSasPhyDrv',
                    'cpqScsiCntlr',
                    'cpqScsiLogDrv',
                    'cpqScsiPhyDrv',
                    'cpqSePciSlot',
                    'cpqSiMemModule',
                    'cpqSm2Cntlr',
                    'cpqSsChassis',
                    'HPFan',
                    'HPPowerSupply',
                    'HPsdFan',
                    'HPTemperatureSensor',
                ]


    def upgrade(self, app):
        for t in dmd.Devices.getAllRRDTemplates():
            for gt in t.thresholds():
                if isinstance(gt, StatusThreshold): continue
	        if gt.id != '%s status'%t.id or t.id not in compClasses:
	            continue
                t.thresholds.removeRelation(gt)
        ZenPackBase.upgrade(self, app)

