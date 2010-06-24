import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class pools(SnmpPlugin):

    relname = "pools"
    modname = 'ZenPacks.community.ZeusLoadBalancer.ZeusPool'
    
    columns = {
    '.1': 'poolName',
    '.2': 'poolAlgorithm',
    '.3': 'poolNodes',
    '.4': 'poolDraining',
    '.5': 'poolFailPool',
    '.10': 'poolPersistence',
    }
    
    snmpGetTableMaps = (
    GetTableMap('poolinfo', '.1.3.6.1.4.1.7146.1.2.3.2.1', columns),
    )

    def process(self, device, results, log):
        """collect snmp information from this zxtm"""

       
    
        # log that we are processing device
        log.info('processing %s for device %s', self.name(), device.id)
        log.debug("SNMP results: %r", results)

        poolCount = 0

        rm = self.relMap()

        # We do this manually to grab the OID suffix which becomes
        # the snmpindex, ascii encoded into OID's is horrible!
        for suffix, data in results[1]['poolinfo'].iteritems():
            om = self.objectMap(data)

            # Remove the extra " characters out of the pool names
            newName = om.poolName.replace('"', '')
            om.poolName = newName

            om.id = self.prepId(om.poolName)

            log.debug("Found Pool: %s" % om.poolName)

            om.snmpindex = suffix
            rm.append(om)
            poolCount = poolCount + 1

        log.info("Finished processing %s, %i pools found", self.name(), poolCount)
        return [rm]
