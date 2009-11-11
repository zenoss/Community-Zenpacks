################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MsSql2kDatabaseMap.py

MsSql2kDatabaseMap maps the MSSQL 2000 Databases table to Database objects

$Id: MsSqlDatabaseMap.py,v 1.0 2009/11/11 11:00:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.community.ZenODBC.OdbcPlugin import OdbcPlugin

class MsSql2kDatabaseMap(OdbcPlugin):
    

    ZENPACKID = 'ZenPacks.community.MsSQLMon_ODBC'

    maptype = "MsSql2kDatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.MsSQLMon_ODBC.MsSql80Database"
    deviceProperties = \
                OdbcPlugin.deviceProperties + ('zWinUser',
		                               'zWinPassword',
					       'zMsSqlConnectionString',
					       )


    def queries(self, device):
        cs =  ';'.join((getattr(device, 'zMsSqlConnectionString', None),
	                'DATABASE=master',
                        'SERVER=%s'%str(device.manageIp),
                        'UID=%s'%getattr(device, 'zWinUser', None),
                        'PWD=%s'%getattr(device, 'zWinPassword', None)))
        return {
            "dbsize": (cs,
                """USE master;
                sp_databases;""",
		['dbname', 'size', 'remarks']),
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
		}
        rm = self.relMap()
	dbsize = {}

	for db in results.get('dbsize', []):
	    dbsize[db['dbname']] = db['size'] * 1024
	databases = results.get('dbtypes80', None)
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
