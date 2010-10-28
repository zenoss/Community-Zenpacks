################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap

class DellEqualLogicStoragePoolMap(SnmpPlugin):
	"""Map Dell System Management Logical Disk table to model."""

	maptype = "DellEqualLogicStoragePoolMap"
	modname = "ZenPacks.community.DellEqualLogicMon.DellEqualLogicStoragePool"
	relname = "storagepools"
	compname = "os"

	snmpGetTableMaps = (
		GetTableMap('storagePoolTable',
                    '.1.3.6.1.4.1.12740.16.1.1.1',
                    {
                        '.3': 'caption',
                        '.8': 'description',
                    }
	),
	GetTableMap('storagePoolStatsTable',
                '.1.3.6.1.4.1.12740.16.1.2.1',
			    {
					'.1': '_sizeM',
					'.2': '_usedM',
		    	 }
	),
	)

	def process(self, device, results, log):
		"""collect snmp information from this device"""
		log.info('processing %s for device %s', self.name(), device.id)
		getdata, tabledata = results
		pooltable = tabledata.get('storagePoolTable')
		poolstats = tabledata.get('storagePoolStatsTable')
		rm = self.relMap()
		sizeM = 0
		usedM = 0
		for oid, stats in poolstats.iteritems():
			om = self.objectMap(stats)
			sizeM = stats.get( '_sizeM', 0 ) * 1048576
			usedM = stats.get( '_usedM', 0 ) * 1048576
			#print "%d" % sizeM
		#for pool, stats in zip(pooltable.values(), poolstats.values()):
		for oid, pool in pooltable.iteritems():
			try:
				om = self.objectMap(pool)
				om.id = self.prepId(om.caption)
				om.snmpindex = oid.strip('.')
				#sizeM = stats.get( '_sizeM', 0 ) * 1048576
				om.poolSpace = "%d" % sizeM
				om.poolUsedSpace = "%d" % usedM
			except AttributeError:
				continue
			rm.append(om)
		return rm
