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

$Id: MySqlDatabaseMap.py,v 1.0 2009/05/15 16:59:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.community.ZenODBC.modeler.plugins.community.odbc.OdbcPlugin import OdbcPlugin

class MySqlDatabaseMap(OdbcPlugin):
    

    ZENPACKID = 'ZenPacks.community.ZenODBC'

    maptype = "MySqlDatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.MySQLMon_ODBC.MySqlDatabase"
    deviceProperties = \
                OdbcPlugin.deviceProperties + ('zMySqlUsername',
		                               'zMySqlPassword',
					       'zMySqlConnectionString',
					       )

    cs = ''
    tables = {'databases':
                ('SELECT table_schema, engine FROM TABLES GROUP BY table_schema',
		['dbname', 'type']),
	    }
    uid = None
    pwd = None

    def prepare(self, device, log):
	self.cs = getattr(device, 'zMySqlConnectionString', None)
        self.cs = "%s;Database=information_schema;SERVER=%s" %(self.cs, str(device.manageIp))
        self.uid = getattr(device, 'zMySqlUsername', None)
        self.pwd = getattr(device, 'zMySqlPassword', None)
	return (self.cs, self.tables, self.uid, self.pwd)
	
    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
	databases = results.get('databases')
	if not databases: return
        rm = self.relMap()
        for database in databases:
	    try:
                om = self.objectMap(database)
                om.id = self.prepId(om.dbname)
            except AttributeError:
                continue
            rm.append(om)
        return rm
