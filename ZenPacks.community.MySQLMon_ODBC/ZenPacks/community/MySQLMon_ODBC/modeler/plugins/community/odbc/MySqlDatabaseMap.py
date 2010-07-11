################################################################################
#
# This program is part of the MySQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MySqlDatabaseMap.py

MySqlDatabaseMap maps the MySQL Databases table to Database objects

$Id: MySqlDatabaseMap.py,v 1.2 2010/07/11 17:40:34 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.community.ZenODBC.OdbcPlugin import OdbcPlugin

class MySqlDatabaseMap(OdbcPlugin):


    ZENPACKID = 'ZenPacks.community.MySQLMon_ODBC'

    maptype = "MySqlDatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.MySQLMon_ODBC.MySqlDatabase"
    deviceProperties = \
                OdbcPlugin.deviceProperties + ('zMySqlUsername',
                                               'zMySqlPassword',
                                               'zMySqlConnectionString',
                                               )


    def queries(self, device):
        cs = [getattr(device, 'zMySqlConnectionString', 'DRIVER={MySQL}')]
        if not cs[0].upper().__contains__('SERVER='):
            cs.append('SERVER=%s'%device.manageIp)
        cs.append('DATABASE=information_schema')
        uid = getattr(device, 'zMySqlUsername', None)
        if uid: cs.append('UID=%s'%uid)
        pwd = getattr(device, 'zMySqlUsername', None)
        if pwd: cs.append('PWD=%s'%pwd)
        cs = ';'.join(cs)
        return {
            "databases": (cs,
                """USE information_schema;
                SELECT table_schema as dbname, engine as type FROM TABLES GROUP BY table_schema;""",
                ['dbname', 'type']),
            }


    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        databases = results.get('databases')
        if not databases: return
        rm = self.relMap()
        for database in databases:
            try:
                om = self.objectMap(database)
                om.id = self.prepId(om.dbname)
                om.status = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm
