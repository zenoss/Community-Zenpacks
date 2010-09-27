################################################################################
#
# This program is part of the RDBMS Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DatabaseMap.py

DatabaseMap maps the RDBMS Databases table to Database objects

$Id: DatabaseMap.py,v 1.1 2010/09/27 00:13:04 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class DatabaseMap(ZenPackPersistence, SnmpPlugin):

    ZENPACKID = 'ZenPacks.community.RDBMS'

    maptype = "DatabaseMap"
    compname = "os"
    relname = "softwaredbsrvinstances"
    modname = "ZenPacks.community.RDBMS.DBSrvInst"


    snmpGetTableMaps = (
        GetTableMap('applEntry',
                    '.1.3.6.1.2.1.27.1.1',
                    {
                        '.1': 'applIndex',
                        '.2': 'applName',
                    }),
        GetTableMap('rdbmsDbTable',
                    '.1.3.6.1.2.1.39.1.1.1',
                    {
                        '.3': '_vendorName',
                        '.4': 'dbname',
                        '.5': 'contact',
                    }),
        GetTableMap('rdbmsDbInfoTable',
                    '.1.3.6.1.2.1.39.1.2.1',
                    {
                        '.1': 'type',
                        '.2': 'version',
                        '.3': 'blockSize',
                        '.4': 'totalBlocks',
                    }),
        GetTableMap('rdbmsSrvTable',
                    '.1.3.6.1.2.1.39.1.5.1',
                    {
                        '.2': 'vendor',
                        '.3': 'product',
                        '.4': 'contact',
                    }),
        GetTableMap('rdbmsRelTable',
                    '.1.3.6.1.2.1.39.1.9.1',
                    {
                        '.1': 'state',
                        '.2': 'activeTime',
                    }),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        databases = {}
        instname = {}
        for oid, dbInst in tabledata.get('applEntry', {}).iteritems():
            instname[dbInst['applIndex']] = dbInst['applName']
        for oid, db in tabledata.get('rdbmsDbInfoTable', {}).iteritems():
            databases[oid.strip('.')] = db
        for oid, db in tabledata.get('rdbmsRelTable', {}).iteritems():
            dbid, instid = oid.split('.')
            if dbid not in databases: continue
            if 'setDBSrvInst' in databases[dbid]: continue
            databases[dbid]['setDBSrvInst'] = instname.get(instid, instid)
            databases[dbid]['status'] = db['state']
            databases[dbid]['activeTime'] = self.asdate(db['activeTime'])
        maps = [self.relMap()]
        for oid, inst in tabledata.get('rdbmsSrvTable', {}).iteritems():
            om = self.objectMap()
            om.snmpindex = oid.strip('.')
            om.dbsiname = instname.get(om.snmpindex, None) or om.snmpindex 
            om.id = self.prepId(om.dbsiname)
            om.contact = inst.get('contact')
            om.setProductKey = MultiArgs(
                                inst.get('product', None) or 'RDBMS Server',
                                inst.get('vendor', None) or 'Unknown')
            maps[-1].append(om)
        self.relname = "softwaredatabases"
        self.modname = "ZenPacks.community.RDBMS.Database"
        maps.append(self.relMap())
        for oid, database in tabledata.get('rdbmsDbTable', {}).iteritems():
            database.update(databases.get(oid.strip('.'), {}))
            try:
                om = self.objectMap(database)
                if not hasattr(om, 'setDBSrvInst'): om.id=self.prepId(om.dbname)
                else: om.id = self.prepId('%s_%s'%(om.setDBSrvInst, om.dbname))
                om.snmpindex = oid.strip('.')
                om.totalBlocks = int(om.totalBlocks) / int(om.blockSize or 1)
            except AttributeError:
                continue
            maps[-1].append(om)
        return maps
