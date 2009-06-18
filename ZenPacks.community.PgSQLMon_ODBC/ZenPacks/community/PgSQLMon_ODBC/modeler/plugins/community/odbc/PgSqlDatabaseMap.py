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

$Id: PgSqlDatabaseMap.py,v 1.0 2009/05/15 16:59:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.community.ZenODBC.modeler.plugins.community.odbc.OdbcPlugin import OdbcPlugin

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

    cs = ''
    tables = {"version":
                ("SELECT setting FROM pg_settings WHERE name = 'server_version'",
		['version',]),
            "databases":
                ("SELECT datname, pg_database_size(datname) FROM pg_database",
		['dbname', 'totalBlocks']),
	    }
    uid = None
    pwd = None

    def prepare(self, device, log):
	self.cs = getattr(device, 'zPgSqlConnectionString', None)
        self.cs = "%s;Database=template1;Servername=%s" %(self.cs, str(device.id))
        self.uid = getattr(device, 'zPgSqlUsername', None)
        self.pwd = getattr(device, 'zPgSqlPassword', None)
	return (self.cs, self.tables, self.uid, self.pwd)
	
    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        log.info('results %s', results)
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
