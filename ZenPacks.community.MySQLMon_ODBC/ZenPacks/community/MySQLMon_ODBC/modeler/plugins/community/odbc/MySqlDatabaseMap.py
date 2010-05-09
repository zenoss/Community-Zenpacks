################################################################################
#
# This program is part of the MySQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MySqlDatabaseMap.py

MySqlDatabaseMap maps the MySQL Databases table to Database objects

$Id: MySqlDatabaseMap.py,v 1.1 2009/08/09 21:28:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

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
        cs =  ';'.join((getattr(device, 'zMySqlConnectionString', None),
                        'DATABASE=information_schema',
                        'SERVER=%s'%str(device.manageIp),
                        'UID=%s'%getattr(device, 'zMySqlUsername', None),
                        'PWD=%s'%getattr(device, 'zMySqlPassword', None)))
        return {
            "databases": (cs,
                """USE information_schema;
                SELECT table_schema, engine FROM TABLES GROUP BY table_schema;""",
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
