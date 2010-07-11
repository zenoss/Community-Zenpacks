################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MsSql2k5DatabaseMap.py

MsSql2k5DatabaseMap maps the MSSQL 2005 Databases table to Database objects

$Id: MsSqlDatabaseMap.py,v 1.1 2010/07/11 18:36:14 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.community.ZenODBC.OdbcPlugin import OdbcPlugin

class MsSql2k5DatabaseMap(OdbcPlugin):

    ZENPACKID = 'ZenPacks.community.MsSQLMon_ODBC'

    maptype = "MsSql2k5DatabaseMap"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.MsSQLMon_ODBC.MsSql90Database"
    deviceProperties = \
                OdbcPlugin.deviceProperties + ('zWinUser',
                                               'zWinPassword',
                                               'zMsSqlConnectionString',
                                               )


    def queries(self, device):
        cs = [getattr(device, 'zMsSqlConnectionString', 'DRIVER={FreeTDS}')]
        if not cs[0].upper().__contains__('SERVER='):
            cs.append('SERVER=%s'%device.manageIp)
        cs.append('DATABASE=master')
        uid = getattr(device, 'zWinUser', None)
        if uid: cs.append('UID=%s'%uid)
        pwd = getattr(device, 'zWinPassword', None)
        if pwd: cs.append('PWD=%s'%pwd)
        cs =  ';'.join(cs)
        return {
            "dbsize": (cs,
                """USE master;
                sp_databases;""",
                ['DATABASE_NAME', 'DATABASE_SIZE', 'REMARKS']),
            "dbtypes90": (cs,
                """USE master;
                SELECT name as dbname, compatibility_level as type, state as status FROM sys.databases;""",
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
            dbsize[db['DATABASE_NAME']] = db['DATABASE_SIZE'] * 1024
        databases = results.get('dbtypes90', None)
        if not databases: return
        for database in databases:
            try:
                om = self.objectMap(database)
                if not dbsize.get(om.dbname): om.monitor = False
                om.id = self.prepId(om.dbname)
                om.type = types.get(getattr(on, 'type' , 1), types[1])
                om.blockSize = 8192
                om.totalBlocks = dbsize.get(om.dbname, 0) / om.blockSize
            except AttributeError:
                continue
            rm.append(om)
        return rm
