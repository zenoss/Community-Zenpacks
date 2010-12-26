################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__='''

Delete the previous HPEVA reports.  

$Id:$
'''
from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

class removeOldHPEVAReports(ZenPackMigration):
    version = Version(1, 8)

    def migrate(self, pack):
        if hasattr(pack.dmd.Reports, 'Device Reports'):
            devReports = pack.dmd.Reports['Device Reports']

            if hasattr(devReports, 'HPEVA'):
                devReports._delObject('HPEVA')

removeOldHPEVAReports()


