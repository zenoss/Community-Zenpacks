import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class virtualservers(SnmpPlugin):

    relname = "virtualServers"
    modname = 'ZenPacks.community.ZeusLoadBalancer.ZeusVirtualServer'
    
    columns = {
    '.1': 'vsName',
    '.2': 'vsPort',
    '.3': 'vsProtocol',
    }
    
    snmpGetTableMaps = (
    GetTableMap('vsinfo', '.1.3.6.1.4.1.7146.1.2.2.2.1', columns),
    )

    def process(self, device, results, log):
        """collect snmp information from this zxtm"""

       
    
        # log that we are processing device
        log.info('processing %s for device %s', self.name(), device.id)
        log.debug("SNMP results: %r", results)

        vsCount = 0

        rm = self.relMap()

        # We do this manually to grab the OID suffix which becomes
        # the snmpindex, ascii encoded into OID's is horrible!
        for suffix, data in results[1]['vsinfo'].iteritems():
            om = self.objectMap(data)

            # Remove the extra " characters out of the pool names
            newName = om.vsName.replace('"', '')
            om.vsName = newName

            om.id = self.prepId(om.vsName)

            log.debug("Found Virtual Server: %s" % om.vsName)

            om.snmpindex = suffix
            rm.append(om)
            vsCount = vsCount + 1

        log.info("Finished processing %s, %i virtual servers found", self.name(), vsCount)
        return [rm]
