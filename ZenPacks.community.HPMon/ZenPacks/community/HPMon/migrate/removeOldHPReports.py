################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__='''

Delete the previous HP iLO Boards and HP Storage Controllers reports.  

$Id:$
'''
from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

class removeOldHPReports(ZenPackMigration):
    version = Version(2, 1)

    def migrate(self, pack):
        if hasattr(pack.dmd.Reports, 'Device Reports'):
            devReports = pack.dmd.Reports['Device Reports']

            if hasattr(devReports, 'HP iLO Boards'):
                devReports._delObject('HP iLO Boards')

            if hasattr(devReports, 'HP Storage Controllers'):
                devReports._delObject('HP Storage Controllers')

removeOldHPReports()


