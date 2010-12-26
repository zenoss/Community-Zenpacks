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

$Id: MySqlDatabaseMap.py,v 1.4 2010/12/15 21:04:28 egor Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.DataMaps import MultiArgs
from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class MySqlDatabaseMap(ZenPackPersistence, SQLPlugin):


    ZENPACKID = 'ZenPacks.community.MySQLMon_ODBC'

    maptype = "MySqlDatabaseMap"
    compname = "os"
    relname = "softwaredbsrvinstances"
    modname = "ZenPacks.community.MySQLMon_ODBC.MySqlSrvInst"
    deviceProperties = \
                SQLPlugin.deviceProperties + ('zMySqlUsername',
                                              'zMySqlPassword',
                                              'zMySqlConnectionString',
                                              )


    def queries(self, device):
        queries = {}
        inst = 0
        uid = getattr(device, 'zMySqlUsername', None)
        pwd = getattr(device, 'zMySqlPassword', None)
        for cs in getattr(device, 'zMySqlConnectionString', ['DRIVER={MySQL}']):
            options = dict([opt.split('=') for opt in cs.split(';')])
            cs = ['MySQLdb']
            cs.append("host='%s'"%options.get('SERVER', device.manageIp))
            cs.append("port=%s"%options.get('PORT', '3306'))
            cs.append("db='information_schema'")
            if uid or 'UID' in options:
                cs.append("user='%s'"%options.get('UID', uid))
            if pwd or 'PWD' in options:
                cs.append("passwd='%s'"%options.get('PWD', pwd))
            queries['si_%s'%inst] = (
                "SHOW VARIABLES",
                None,
                ','.join(cs),
                {
                    'hostname':'hostname',
                    'port':'port',
                    'license':'license',
                    'version':'version',
                    'version_compile_machine':'setProductKey',
                })
            queries['vr_%s'%inst] = (
                "SHOW VARIABLES WHERE Variable_name like 'have_%' AND Value='YES'",
                None,
                ','.join(cs),
                {
                    'Variable_name':'have',
                })
            queries['db_%s'%inst] = (
                """SELECT table_schema,
                          engine,
                          MIN(create_time) as created,
                          version,
                          MIN(table_collation) as collation,
                          '%s' as instance
                   FROM TABLES
                   GROUP BY table_schema"""%inst,
                None,
                ','.join(cs),
                {
                    'table_schema':'dbname',
                    'engine':'type',
                    'created':'activeTime',
                    'version':'version',
                    'collation':'collation',
                    'instance':'setDBSrvInst',
                })
            inst = inst + 1
        return queries


    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        maps = [self.relMap()]
        databases = []
        for tname, instances in results.iteritems():
            if tname.startswith('si_'):
                for inst in instances:
                    om = self.objectMap(inst)
                    om.dbsiname = tname[3:]
                    om.id = self.prepId(om.dbsiname)
                    om.setProductKey = MultiArgs('MySQL Server %s (%s)'%(
                                        om.version, om.setProductKey), 'MySQL')
                    have = results.get('vr_%s'%om.dbsiname,[])
                    om.have = [h['have'][5:] for h in have]
                    maps[-1].append(om)
            elif tname.startswith('vr_'): continue 
            else: databases.extend(instances)
        self.relname = "softwaredatabases"
        self.modname = "ZenPacks.community.MySQLMon_ODBC.MySqlDatabase"
        maps.append(self.relMap())        
        for database in databases:
            try:
                om = self.objectMap(database)
                om.id = self.prepId('%s_%s'%(om.setDBSrvInst, om.dbname))
                om.activeTime = str(om.activeTime)
                om.setDBSrvInst = str(om.setDBSrvInst)
                om.status = 2
            except AttributeError:
                continue
            maps[-1].append(om)
        return maps
