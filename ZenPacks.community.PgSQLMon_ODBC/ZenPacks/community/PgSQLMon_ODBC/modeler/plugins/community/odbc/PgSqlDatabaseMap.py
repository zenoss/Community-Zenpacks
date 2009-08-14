################################################################################
#
# This program is part of the PgSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""PgSqlDatabaseMap.py

PgSqlDatabaseMap maps the PostgreSQL Databases table to Database objects

$Id: PgSqlDatabaseMap.py,v 1.1 2009/08/13 20:59:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.community.ZenODBC.OdbcPlugin import OdbcPlugin

class PgSqlDatabaseMap(OdbcPlugin):
    

    ZENPACKID = 'ZenPacks.community.ZenODBC'

    maptype = "PgSqlDatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.PgSQLMon_ODBC.PgSqlDatabase"
    deviceProperties = \
                OdbcPlugin.deviceProperties + ('zPgSqlUsername',
		                               'zPgSqlPassword',
					       'zPgSqlConnectionString',
					       )


    def queries(self, device):
        cs =  ';'.join((getattr(device, 'zPgSqlConnectionString', None),
                        'Database=template1',
                        'Servername=%s'%str(device.manageIp),
                        'UID=%s'%getattr(device, 'zPgSqlUsername', None),
                        'PWD=%s'%getattr(device, 'zPgSqlPassword', None)))
        return {
            "version": (cs,
                """SELECT setting FROM pg_settings WHERE name = 'server_version';""",
                ['version']),
            "databases": (cs,
                """SELECT datname, pg_database_size(datname) FROM pg_database;""",
                ['dbname', 'totalBlocks']),
            }

	
    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
	databases = results.get('version')
	if type(databases) is list:
	    version = getattr(databases[0], 'version', '')
	    if version.startswith('8.3'):
                self.modname = "ZenPacks.community.PgSQLMon_ODBC.PgSql83Database"
	databases = results.get('databases')
	if not databases: return
        rm = self.relMap()
        for database in databases:
            try:
                om = self.objectMap(database)
                om.id = self.prepId(om.dbname)
                om.type = 'PostgreSQL'
                om.status = 2
            except AttributeError:
                continue
            rm.append(om)
        return rm
