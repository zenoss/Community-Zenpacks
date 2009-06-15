__doc__="""AIXPCIMap

This modeler determines the adapters on the device and updates appropriately.
"""


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class AIXPCIMap(SnmpPlugin):
    """Gather information about adapters"""

    maptype = "AIXPCIMap"
    modname = "ZenPacks.community.AIX.AIXExpansionCard"
    relname = "cards"
    compname = "hw"

    #
    # These column names are for the pciTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    columns = {
        '.1': 'title', # aixAdapterName
        '.2': 'snmpindex', # aixAdapterIndex
        #'.3': 'aixAdapterType',
        #'.4': 'aixAdapterInterface',
        #'.5': 'aixAdapterStatus',
        '.6': 'slot', # aixAdapterLocation
        '.7': 'setProductKey', # aixAdapterDescr
    }

    snmpGetTableMaps = (
        GetTableMap( 'pciTable', '.1.3.6.1.4.1.2.6.191.9.9.1.1', columns),
    )

    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        pci_table = tabledata.get( "pciTable" )
        if not pci_table:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            return

        relationship = self.relMap()
        maps = []
        for card in pci_table.values():
            if not self.checkColumns(card, self.columns, log):
               continue

            om = self.objectMap(card)

            log.debug( "Found tile '%s' slot '%s' for product key '%s'", om.title, om.slot, om.setProductKey)

            om.setProductKey = MultiArgs(om.setProductKey, "IBM")

            om.id = self.prepId(om.title)
            relationship.append(om)

        maps.append(relationship)

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No adapters found by %s for %s", self.name(), device.id)
           return

        return maps

