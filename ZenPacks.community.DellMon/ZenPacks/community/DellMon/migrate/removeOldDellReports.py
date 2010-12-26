################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__='''

Delete the previous DRAC and Storage Controllers reports.  

$Id:$
'''
from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version

class removeOldDellReports(ZenPackMigration):
    version = Version(2, 3)

    def migrate(self, pack):
        if hasattr(pack.dmd.Reports, 'Device Reports'):
            devReports = pack.dmd.Reports['Device Reports']

            if hasattr(devReports, 'Dell DRAC Controllers'):
                devReports._delObject('Dell DRAC Controllers')

            if hasattr(devReports, 'Dell Storage Controllers'):
                devReports._delObject('Dell Storage Controllers')

removeOldDellReports()


