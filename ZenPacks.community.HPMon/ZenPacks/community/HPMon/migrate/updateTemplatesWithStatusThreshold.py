###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, 2008, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import Globals
from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version
from ZenPacks.community.deviceAdvDetail.thresholds.StatusThreshold \
        import StatusThreshold

class updateTemplatesWithStatusThreshold( ZenPackMigration ):
    """
    update RRDTemplates with statusThreshold
    """

    version = Version(1, 4)



    def migrate(self, pack):
        dmd = pack.__primary_parent__.__primary_parent__

        hpTemplates = [ 'cpqDaCntlr',
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

        # Update existing templates to use the new StatusThreshold
        for template in dmd.Devices.Server.getAllRRDTemplates():
            if template.id not in hpTemplates: continue
            for threshold in template.thresholds():
                if isinstance(threshold, StatusThreshold): continue
	        if threshold.id != '%s status'%template.id: continue
                new = StatusThreshold(threshold.id)
                template.thresholds.removeRelation(threshold)
                setattr(new, "dsnames", getattr(threshold, "dsnames"))
                setattr(new, "enabled", getattr(threshold, "enabled"))
                setattr(new, "escalateCount", getattr(threshold, "escalateCount"))
                setattr(new, "eventClass", getattr(threshold, "eventClass"))
                threshold = new
            template.thresholds._setObject(threshold.id, threshold)

updateTemplatesWithStatusThreshold()
