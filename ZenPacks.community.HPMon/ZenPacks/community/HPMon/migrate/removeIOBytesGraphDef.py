################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

class removeIOBytesGraphDef( ZenPackMigration ):
    """
    remove IO Bytes GraphDef from RRDTemplates
    """
    version = Version(2, 1)

    def migrate(self, pack):

        hpTemplates = [ 'cpqDaPhyDrv',
                        'cpqFcaPhyDrv',
                        'cpqScsiPhyDrv',
                        ]

        for template in pack.dmd.Devices.Server.getAllRRDTemplates():
            if template.id not in hpTemplates: continue
            if hasattr(template.graphDefs, 'IO Bytes'):
                template.graphDefs._delObject('IO Bytes')
            if hasattr(template.graphs, 'IO Bytes'):
                template.graphs._delObject('IO Bytes')

removeIOBytesGraphDef()
