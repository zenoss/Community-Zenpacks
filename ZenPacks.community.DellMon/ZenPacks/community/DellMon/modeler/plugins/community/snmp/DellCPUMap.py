################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellCPUMap

DellCPUMap maps the processorDeviceTable and processorDeviceStatusTable tables
to cpu objects

$Id: DellCPUMap.py,v 1.0 2009/05/27 21:03:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class DellCPUMap(SnmpPlugin):
    """Map Dell System Management cpu table to model."""

    maptype = "DellCPUMap"
    modname = "ZenPacks.community.DellMon.DellCPU"
    relname = "cpus"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('hrProcessorTable',
	            '.1.3.6.1.2.1.25.3.3.1',
		    {
		        '.1': '_cpuidx',
		    }
	),
        GetTableMap('cpuTable',
	            '.1.3.6.1.4.1.674.10892.1.1100.30.1',
		    {
                        '.2': 'socket',
                        '.8': '_manuf',
                        '.12': 'clockspeed',
                        '.13': 'extspeed',
                        '.14': 'voltage',
                        '.16': '_version',
		        '.17': 'core',
		    }
	),
        GetTableMap('cacheTable',
	            '.1.3.6.1.4.1.674.10892.1.1100.40.1',
		    {
		        '.6': 'cpuidx',
			'.11': 'level',
			'.13': 'size',
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
        cores = len(tabledata.get("hrProcessorTable")) / len(cputable)
        if cores == 0: cores = 1
        rm = self.relMap()
        cpumap = {}
	cachemap = {}
        if cachetable:
            for cache in cachetable.values():
                if cache['level'] > 2:
                    if not cachemap.has_key(cache['cpuidx']):
	                cachemap[cache['cpuidx']] = {}
                    cachemap[cache['cpuidx']][cache['level']-2] = cache.get('size',0)
        for cpu in cputable.values():
            om = self.objectMap(cpu)
            model = getattr(om, '_version').replace("(R)", "")
            if not model.startswith(getattr(om, '_manuf')):
                model = "%s_%s" %(getattr(om, '_manuf'), model)
            om.setProductKey = model 
            om.id = self.prepId("socket%s" % (om.socket))
	    om.core = getattr(om, 'core', 0)
	    if om.core == 0: om.core = cores
	    for clevel, csize in cachemap[om.socket].iteritems():
	        setattr(om, "cacheSizeL%d"%clevel, csize)
            rm.append(om)
        return rm

