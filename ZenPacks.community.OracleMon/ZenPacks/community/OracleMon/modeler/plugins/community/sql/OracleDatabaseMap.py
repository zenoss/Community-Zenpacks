################################################################################
#
# This program is part of the OracleMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OracleDatabaseMap.py

OracleDatabaseMap maps the Oracle Databases table to Database objects

$Id: OracleDatabaseMap.py,v 1.1 2010/12/19 21:31:35 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.DataMaps import MultiArgs
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
import re

class OracleDatabaseMap(ZenPackPersistence, SQLPlugin):


    ZENPACKID = 'ZenPacks.community.OracleMon'

    maptype = "OracleDatabaseMap"
    compname = "os"
    relname = "softwaredbsrvinstances"
    modname = "ZenPacks.community.OracleMon.OracleSrvInst"
    deviceProperties = SQLPlugin.deviceProperties + ('zOracleUser',
                                                'zOraclePassword',
                                                'zOracleConnectStrings',
                                                'zOracleTablespaceIgnoreNames',
                                                'zOracleTablespaceIgnoreTypes',
                                                )


    def queries(self, device):
        queries = {}
        inst = 0
        for dsn in getattr(device, 'zOracleConnectStrings', []):
            cs = 'cx_Oracle,%s,%s,%s'
            dsn = dsn.replace('${dev/manageIp}', device.manageIp)
            if getattr(device, 'zOracleUser', '').upper() == 'SYS':cs=cs + ',mode=2'
            cs = cs%(getattr(device, 'zOracleUser', ''),
                    getattr(device, 'zOraclePassword', ''),
                    dsn)
            queries['si_%s'%inst] = (
                """SELECT NAME,
                          ( SELECT BANNER
                            FROM v$version
                            WHERE rownum = 1
                          ) VERSION,
                          '%s' DSN,
                          0 STATUS
                    FROM v$database"""%dsn,
                None,
                cs,
                {
                    'NAME':'dbsiname',
                    'VERSION':'setProductKey',
                    'DSN':'dsn',
                    'STATUS':'status',
                })
            queries['db_%s'%inst] = (
                """SELECT TABLESPACE_NAME,
                          a.CONTENTS,
                          a.BLOCK_SIZE,
                          b.BYTES/a.BLOCK_SIZE BLOCKS,
                          a.STATUS,
                          ( SELECT NAME
                            FROM v$database
                            WHERE rownum = 1
                          ) DATABASE
                   FROM ( SELECT TABLESPACE_NAME,
                                 CONTENTS,
                                 STATUS,
                                 BLOCK_SIZE
                          FROM dba_tablespaces ) a
                   INNER JOIN
                        ( SELECT TABLESPACE_NAME,
                                 sum(BYTES) BYTES
                          FROM dba_data_files
                          GROUP BY TABLESPACE_NAME) b
                   USING (TABLESPACE_NAME)""",
                None,
                cs,
                {
                    'TABLESPACE_NAME':'dbname',
                    'CONTENTS':'type',
                    'BLOCK_SIZE':'blockSize',
                    'BLOCKS':'totalBlocks',
                    'STATUS':'status',
                    'DATABASE':'setDBSrvInst',
                })
            inst = inst + 1
        return queries


    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        skiptsnames = getattr(device, 'zOracleTablespaceIgnoreNames', None)
        skiptstypes = getattr(device, 'zOracleTablespaceIgnoreTypes', None)
        maps = [self.relMap()]
        databases = []
        for tname, instances in results.iteritems():
            if tname.startswith('si_'):
                for inst in instances:
                    om = self.objectMap(inst)
                    om.id = self.prepId(om.dbsiname)
                    om.setProductKey = MultiArgs(om.setProductKey, 'Oracle')
                    maps[-1].append(om)
            else: databases.extend(instances)
        self.relname = "softwaredatabases"
        self.modname = "ZenPacks.community.OracleMon.OracleTablespace"
        maps.append(self.relMap())        
        for tspace in databases:
            if (skiptsnames and re.search(skiptsnames,tspace['dbname'])):continue
            if (skiptstypes and re.search(skiptstypes,tspace['type'])):continue
            try:
                om = self.objectMap(tspace)
                om.id = self.prepId('%s_%s'%(om.setDBSrvInst, om.dbname))
                om.status = {'ONLINE':2,'OFFLINE':4,'INVALID':5}.get(om.status, 1)
            except AttributeError:
                continue
            maps[-1].append(om)
        return maps
