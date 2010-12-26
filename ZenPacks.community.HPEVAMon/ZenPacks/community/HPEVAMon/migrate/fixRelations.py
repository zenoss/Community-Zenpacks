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

fix Relations.  

$Id:$
'''
from Products.ZenModel.ZenPack import ZenPackMigration
from Products.ZenModel.migrate.Migrate import Version
from ZenPacks.community.HPEVAMon.HPEVADevice import HPEVADevice as dt

class fixRelations(ZenPackMigration):
    version = Version(1, 8)

    def migrate(self, pack):
        for d in pack.dmd.Devices.getSubDevices(lambda dev:isinstance(dev, dt)):
            d.hw.buildRelations()
            d.os.buildRelations()
            for comp in d.getDeviceComponents():
                comp.buildRelations()

fixRelations()


