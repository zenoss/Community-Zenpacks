################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MsSqlDatabaseMap.py

MsSqlDatabaseMap maps the MSSQL Databases table to Database objects

$Id: MsSqlDatabaseMap.py,v 1.1 2009/08/13 19:35:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.community.ZenODBC.OdbcPlugin import OdbcPlugin

class MsSqlDatabaseMap(OdbcPlugin):
    

    ZENPACKID = 'ZenPacks.community.MsSQLMon_ODBC'

    maptype = "MsSqlDatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.MsSQLMon_ODBC.MsSql90Database"
    deviceProperties = \
                OdbcPlugin.deviceProperties + ('zWinUser',
		                               'zWinPassword',
					       'zMsSqlConnectionString',
					       )


    def queries(self, device):
        cs =  ';'.join((getattr(device, 'zMsSqlConnectionString', None),
                        'SERVER=%s'%str(device.manageIp),
                        'UID=%s'%getattr(device, 'zWinUser', None),
                        'PWD=%s'%getattr(device, 'zWinPassword', None)))
        return {
            "dbsize": (cs,
                """USE master;
                sp_databases;""",
		['dbname', 'size', 'remarks']),
            "dbtypes90": (cs,
                """USE master;
                SELECT name, compatibility_level, state FROM sys.databases;""",
		['dbname', 'type', 'status']),
            "dbtypes80":(cs,
                """USE master;
                SELECT name, cmptlevel, status FROM sysdatabases;""",
		['dbname', 'type', 'status']),
            }

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        types = {1: 'SQL Server',
	        60: 'SQL Server 6.0',
	        65: 'SQL Server 6.5',
	        70: 'SQL Server 7.0',
	        80: 'SQL Server 2000',
		90: 'SQL Server 2005',
		}
        rm = self.relMap()
	dbsize = {}
	for db in results.get('dbsize', []):
	    dbsize[db['dbname']] = db['size'] * 1024
	databases = results.get('dbtypes90', None)
	if not databases:
	    databases = results.get('dbtypes80', None)
            self.modname = "ZenPacks.community.MsSQLMon_ODBC.MsSql80Database"
        if not databases: return	    
        for database in databases:
	    try:
                om = self.objectMap(database)
	        if not dbsize.get(om.dbname): om.monitor = False
                om.id = self.prepId(om.dbname)
	        om.type = types.get(getattr(om, 'type', 1), types[1])
	        om.blockSize = 8192
	        om.totalBlocks = dbsize.get(om.dbname, 0) / om.blockSize
            except AttributeError:
                continue
            rm.append(om)
        return rm
