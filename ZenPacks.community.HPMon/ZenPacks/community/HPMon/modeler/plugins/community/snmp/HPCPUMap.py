################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPCPUMap

HPCPUMap maps the cpqSeCpuTable and cpqSeCpuCacheTable tables to cpu objects

$Id: HPCPUMap.py,v 1.0 2008/12/01 13:54:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class HPCPUMap(SnmpPlugin):
    """Map HP/Compaq insight manager cpu table to model."""

    maptype = "HPCPUMap"
    modname = "ZenPacks.community.HPMon.HPCPU"
    relname = "cpus"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('cpuTable',
	            '.1.3.6.1.4.1.232.1.2.2.1.1',
		    {
		        '.1': '_cpuidx',
		        '.3': 'setProductKey',
		        '.4': 'clockspeed',
		        '.5': 'null',
		        '.6': 'null',
		        '.7': 'extspeed',
		        '.8': 'null',
		        '.9': 'socket',
		        '.15':'core',
		    }
	),
        GetTableMap('cacheTable',
	            '.1.3.6.1.4.1.232.1.2.2.3.1',
		    {
		        '.1': 'cpuidx',
			'.2': 'level',
			'.3': 'size',
		    }
	), 
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cputable = tabledata.get("cpuTable")
        cachetable = tabledata.get("cacheTable")
        if not cputable: return
        rm = self.relMap()
        cpumap = {}
	cachemap = {}
        if cachetable:
            for cache in cachetable.values():
	        cachemap[cache['cpuidx']] = {}
                if cache['level'] == 1: 
                    cachemap[cache['cpuidx']][1] = cache.get('size',0)
                elif cache['level'] == 2:
                    cachemap[cache['cpuidx']][2] = cache.get('size',0)
        for cpu in cputable.values():
            del cpu['null']
            om = self.objectMap(cpu)
            idx = getattr(om, 'socket', om._cpuidx)
            om.id = self.prepId("%s_%s" % (om.setProductKey,idx))
	    om.core = getattr(om, 'core', 1)
	    if om.core == 0: om.core = 1
            try: 
                om.cacheSizeL1 = cachemap[om._cpuidx][1]
	    except:
	        pass
            try:
                om.cacheSizeL2 = cachemap[om._cpuidx][2]
	    except:
	        pass
            rm.append(om)
        return rm
