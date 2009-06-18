################################################################################
#
# This program is part of the RDBMS Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Database

Database maps the rdbmsDbInfoTable table to Database objects

$Id: Database.py,v 1.0 2009/01/08 11:19:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class DatabaseMap(SnmpPlugin):
    """Map RDBMS table to model."""

    maptype = "Database"
    compname = "os"
    relname = "softwaredatabases"
    modname = "ZenPacks.community.RDBMS.Database"
    deviceProperties =  \
      SnmpPlugin.deviceProperties + ('zDatabaseMapIgnoreNames',)

    oid = {}
    columns = {}

    oid['rdbmsDbInfoTable'] = '.1.3.6.1.2.1.39.1.2.1'
    columns['rdbmsDbInfoTable'] = {'.1': 'dbname','.3': 'blockSize','.4': 'totalBlocks'}

    snmpGetTableMaps = []
    for tkey in oid.keys():
        snmpGetTableMaps.append(GetTableMap(tkey, oid[tkey], columns[tkey]))

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
	dontCollect = getattr(device, 'zDatabaseMapIgnoreNames', None)
        for tkey in self.oid.keys():
            table = tabledata.get(tkey)
            if not table: continue
            for entry in table.values():
                if dontCollect and re.search(dontCollect, entry['dbname']): continue
                try:
                    om = self.objectMap(entry)
                    om.id = self.prepId(om.dbname)
		    om.description = om.dbname
		    om.blockSize = 1024 ** (getattr(om, "sizeUnits", 2) - 1)
                except AttributeError:
                    continue
                rm.append(om)
        return rm
