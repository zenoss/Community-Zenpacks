################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MsSqlDatabaseMap.py

MsSqlDatabaseMap maps the MS SQL Databases table to Database objects

$Id: MsSqlDatabaseMap.py,v 1.7 2010/10/06 19:06:07 egor Exp $"""

__version__ = "$Revision: 1.7 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.DataMaps import MultiArgs
from ZenPacks.community.ZenODBC.OdbcPlugin import OdbcPlugin

class MsSqlDatabaseMap(ZenPackPersistence, OdbcPlugin):

    ZENPACKID = 'ZenPacks.community.MsSQLMon_ODBC'

    maptype = "MsSqlDatabaseMap"
    compname = "os"
    relname = "softwaredbsrvinstances"
    modname = "ZenPacks.community.MsSQLMon_ODBC.MsSqlSrvInst"
    deviceProperties = \
                OdbcPlugin.deviceProperties + ('zWinUser',
                                               'zWinPassword',
                                               'zMsSqlConnectionString',
                                               'zMsSqlSrvInstances',
                                               )


    def queries(self, device):
        queries = {}
        uid = pwd = None
        cs = [getattr(device, 'zMsSqlConnectionString', 'DRIVER={FreeTDS};TDS_Version=8.0')]
        options = [opt.split('=')[0].strip().upper() for opt in cs[0].split(';')]
        if 'SERVER' not in options: cs.append('SERVER=%s'%device.manageIp)
        cs.append('DATABASE=master')
        if 'UID' not in options: uid = getattr(device, 'zWinUser', None)
        if uid: cs.append('UID=%s'%uid)
        if 'PWD' not in options: pwd = getattr(device, 'zWinPassword', None)
        if pwd: cs.append('PWD=%s'%pwd)
        for inst in getattr(device, 'zMsSqlSrvInstances', '').split() or ['']:
            if cs[1].startswith('SERVER=') and inst != '':
                cs[1] = 'SERVER=%s\%s' % (device.manageIp, inst)
            queries['si_%s'%inst] = (
                """SELECT CONVERT(Char(128), SERVERPROPERTY('InstanceName')) AS InstanceName,
                    CONVERT(Char(128), SERVERPROPERTY('Edition')) AS Edition,
                    CONVERT(Char(128), SERVERPROPERTY('LicenseType')) AS LicenseType,
                    CONVERT(Int, SERVERPROPERTY('NumLicenses')) AS NumLicenses,
                    CONVERT(Int, SERVERPROPERTY('ProcessID')) AS ProcessID,
                    CONVERT(Char(128), SERVERPROPERTY('ProductVersion')) AS ProductVersion,
                    CONVERT(Char(128), SERVERPROPERTY('ProductLevel')) AS ProductLevel,
                    RTRIM((CASE WHEN SERVERPROPERTY('isClustered') = 1 THEN 'isClustered ' ELSE '' END) + (CASE WHEN SERVERPROPERTY('IsFullTextInstalled') = 1 THEN 'IsFullTextInstalled ' ELSE '' END) + (CASE WHEN SERVERPROPERTY('IsIntegratedSecurityOnly') = 1 THEN 'IsIntegratedSecurityOnly ' ELSE '' END) + (CASE WHEN SERVERPROPERTY('IsSingleUser') = 1 THEN 'IsSingleUser ' ELSE '' END)) AS dbsiproperties,
                    @@version AS Version
                """,
                None,
                ';'.join(cs),
                {
                    'InstanceName':'dbsiname',
                    'Edition':'edition',
                    'LicenseType':'licenseType',
                    'NumLicenses':'numLicenses',
                    'ProcessID':'processID',
                    'ProductVersion':'productVersion',
                    'ProductLevel':'productLevel',
                    'Version':'setProductKey',
                    'dbsiproperties':'dbsiproperties',
                })
            queries['db_%s'%inst] = (
                "sp_helpdb",
                None,
                ';'.join(cs),
                {
                    'name':'dbname',
                    'db_size':'totalBlocks',
                    'owner':'contact',
                    'dbid':'dbid',
                    'created':'activeTime',
                    'status':'status',
                    'compatibility_level':'type',
                })
        return queries

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        types = {1: 'SQL Server',
                60: 'SQL Server 6.0',
                65: 'SQL Server 6.5',
                70: 'SQL Server 7.0',
                80: 'SQL Server 2000',
                90: 'SQL Server 2005',
                100: 'SQL Server 2008',
                }
        statuses = {'ONLINE':0,
                'OFFLINE':1,
                'RESTORING':2,
                'RECOVERING':3,
                'RECOVERY_PENDING':4,
                'SUSPECT':5,
                'EMERGENCY':6,
                }

        maps = [self.relMap()]
        databases = []
        for instname in getattr(device, 'zMsSqlSrvInstances', '').split() or ['']:
            inst = results.get('si_%s'%instname, [None])[0]
            dbs = results.get('db_%s'%instname, None)
            if not dbs: continue
            if not inst:
                databases.extend(dbs)
                continue
            om = self.objectMap(inst)
            if not om.dbsiname: om.dbsiname = instname or 'MSSQLSERVER'
            om.id = self.prepId(om.dbsiname)
            om.dbsiproperties = om.dbsiproperties.split()
            pn, arch = om.setProductKey.split(' - ', 1)
            if not arch.__contains__('(X64)'):pn = '%s (%s)' % (pn, om.dbsiname)
            else: pn = '%s (64-Bit) (%s)' % (pn, om.dbsiname)
            om.setProductKey = MultiArgs(pn, 'Microsoft')
            maps[-1].append(om)
            for db in dbs:
                db['setDBSrvInst'] = om.dbsiname
                databases.append(db)
        self.relname = "softwaredatabases"
        self.modname = "ZenPacks.community.MsSQLMon_ODBC.MsSqlDatabase"
        maps.append(self.relMap())
        if not databases: return maps
        for database in databases:
            try:
                om = self.objectMap(database)
                if not om.status: om.status = 1
                else:
                    om.dbproperties = []
                    for dbprop in om.status.split(', '):
                        try:
                            var, val = dbprop.split('=')
                            if var == 'Status': val = statuses.get(val, 0)
                            setattr(om, var.lower(), val)
                        except: om.dbproperties.append(dbprop)
                if not hasattr(om, 'setDBSrvInst'):
                    om.id = self.prepId(om.dbname)
                else:
                    om.id = self.prepId('%s_%s'%(om.setDBSrvInst, om.dbname))
                om.activeTime = str(om.activeTime)
                om.type = types.get(getattr(om, 'type' , 1), types[1])
                om.blockSize = 8192
                om.totalBlocks = round(float(om.totalBlocks.split()[0]) * 128)
            except AttributeError:
                continue
            maps[-1].append(om)
        return maps
