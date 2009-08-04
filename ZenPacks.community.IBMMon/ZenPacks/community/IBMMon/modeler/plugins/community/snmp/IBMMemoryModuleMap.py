################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMMemoryModuleMap

IBMMemoryModuleMap maps the PhysicalMemoryTable table to IBMMemoryModule objects

$Id: IBMMemoryModuleMap.py,v 1.0 2009/07/13 00:34:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBMMemoryModuleMap(SnmpPlugin):
    """Map IBM Director Memory Module table to model."""

    maptype = "IBMMemoryModule"
    modname = "ZenPacks.community.IBMMon.IBMMemoryModule"
    relname = "memorymodules"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('memoryModulesTable',
	            '1.3.6.1.4.1.2.6.159.1.1.120.1.1',
		    {
			'.1': 'id',
			'.2': '_active',
			'.7': '_formfactor',
			'.8': 'moduletype',
			'.10': '_speed',
			'.11': 'size',
		    }
	),
    )

    formfactors = { 0: 'Unknown',
                    1: 'Other',
                    2: 'SIP',
                    3: 'DIP',
                    4: 'ZIP',
                    5: 'SOJ',
                    6: 'Proprietary',
                    7: 'SIMM',
                    8: 'DIMM',
                    9: 'TSOP',
                    10: 'PGA',
                    11: 'RIMM',
                    12: 'SODIMM',
                    13: 'SRIMM',
                    14: 'SMD',
                    15: 'SSMP',
                    16: 'QFP',
                    17: 'TQFP',
                    18: 'SOIC',
                    19: 'LCC',
                    20: 'PLCC',
                    21: 'BGA',
                    22: 'FPBGA',
                    23: 'LGA',
                    }

    moduletypes = { 0: 'Unknown',
                    1: 'Other',
		    2: 'DRAM',
		    3: 'Synchronous DRAM',
		    4: 'Cache DRAM',
		    5: 'EDO',
		    6: 'EDRAM',
		    7: 'VRAM',
		    8: 'SRAM',
		    9: 'RAM',
		    10: 'ROM',
		    11: 'Flash',
		    12: 'EEPROM',
		    13: 'FEPROM',
		    14: 'EPROM',
		    15: 'CDRAM',
		    16: '3DRAM',
		    17: 'SDRAM',
		    18: 'SGRAM',
		    19: 'RDAM',
		    20: 'DDR',
		    }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	cardtable = tabledata.get('memoryModulesTable')
        rm = self.relMap()
        for oid, card in cardtable.iteritems():
            try:
                om = self.objectMap(card)
		om.snmpindex =  oid.strip('.')
		om.slot = om.id.split()[-1]
                om.id = self.prepId('%s%s' % (self.formfactors.get(
                            getattr(om, '_formfactor', 0), 'Unknown'), om.slot))
		om.size = getattr(om, 'size', 0)
		mtype = [self.moduletypes.get(getattr(om, 'moduletype', 1),
		                                            'Unknown'),]
		try:
		    mspeed = int(getattr(om, '_speed'))
		    if mspeed > 0: mtype.append('%dns' % mspeed) 
		except: pass
		om.moduletype = ' '.join(mtype)
		if getattr(om, '_active', 0) == 0: om.monitor = False
		om.status = 2
            except AttributeError:
                continue
            rm.append(om)
	return rm

