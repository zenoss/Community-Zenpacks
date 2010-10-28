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

class DellEqualLogicVolumeMap(SnmpPlugin):
	"""Map Dell System Management Logical Disk table to model."""

	maptype = "DellEqualLogicVolumeMap"
	modname = "ZenPacks.community.DellEqualLogicMon.DellEqualLogicVolume"
	relname = "volumes"
	compname = "os"

	snmpGetTableMaps = (
		GetTableMap('volumeTable',
					'.1.3.6.1.4.1.12740.5.1.7.1.1',
					{
						'.4': 'caption',
						'.6': 'description',
						'.8': '_sizeM',
						'.26': 'thinProvisioned',
						'.27': '_actual',
					}
		),
	)

	def process(self, device, results, log):
		"""collect snmp information from this device"""
		log.info('processing %s for device %s', self.name(), device.id)
		getdata, tabledata = results
		voltable = tabledata.get('volumeTable')
		rm = self.relMap()
		for oid, volumes in voltable.iteritems():
			try:
				om = self.objectMap(volumes)
				om.id = self.prepId(om.caption)
				om.volumeProvisionedSize = "%d" % (getattr(om, '_sizeM', 0) * 1048576)
				if(getattr(om, 'thinProvisioned', 0) == 1):
					om.volumeReservedSize = "%d" % ((getattr(om, '_actual', 0) / 100.0) * (getattr(om, '_sizeM', 0) * 1048576))
				else:
					om.volumeReservedSize = om.volumeProvisionedSize
					om.snmpindex = oid.strip('.')
			except AttributeError:
				continue
			if(om.volumeProvisionedSize != "0"):
				rm.append(om)
		return rm
