import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class BladeServers(SnmpPlugin):

    #maptype = "bladeserverBladeServersMap" # no longer used
    relname = "bladeservers"
    modname = 'ZenPacks.community.HPBladeChassis.BladeServer'
    
    columns = {
	'.3': 'snmpindex',
	'.4': 'bsDisplayName',
	'.8': 'bsPosition',
	'.9': 'bsHeight',
	'.10': 'bsWidth',
	'.11': 'bsDepth',
	'.15': 'bsSlotsUsed',
	'.16': 'bsSerialNum',
	'.17': 'bsProductId',
    }
    
    snmpGetTableMaps = (
	GetTableMap('bladeinfo', '.1.3.6.1.4.1.232.22.2.4.1.1.1', columns),
    )

    def process(self, device, results, log):
	"""collect snmp information from this blade server"""
	
	# log that we are processing device
	log.info('processing %s for device %s', self.name(), device.id)
	log.debug("BladeServer results: %r", results)
	getdata, tabledata = results
	table = tabledata.get("bladeinfo")
	rm = self.relMap()
	for info in table.values():
	    #verify column exists
	    #if not self.checkColumns(info, self.columns, log): continue
	   
            # Verify blade actually takes up a spot (removes Unknowns)
            if info['bsSlotsUsed'] == 0:
		log.debug("Skipping blade %s due to Slots: %s" % (info['bsDisplayName'],info['bsSlotsUsed']))
                continue
                
            log.info("Found HP Blade: %s at position %s" % (info['bsDisplayName'], info['bsPosition']))
	    # create the object map which puts our snmp stat into
	    # the BladeServer object
	    om = self.objectMap(info)
	    om.id = self.prepId(om.bsDisplayName)
	    rm.append(om)
	return [rm]

