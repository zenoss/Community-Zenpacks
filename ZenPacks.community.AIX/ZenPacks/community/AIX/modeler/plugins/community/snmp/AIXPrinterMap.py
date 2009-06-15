__doc__="""AIXPrinterMap

This modeler determines the tape devices on the device and updates appropriately.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class AIXPrinterMap(SnmpPlugin):
    """Get the AIX printer list"""

    maptype = "AIXPrinterMap"
    modname = "ZenPacks.community.AIX.AIXPrinter"
    relname = "printer"
    compname = "hw"

    #
    # These column names are for the aixPvTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    Table_columns = {
        '.1': 'title',
        '.2': 'snmpindex',
        '.3': 'aixprintertype',
        '.4': 'aixprinterinterface',
        '.5': 'aixprinterstatus',
        '.6': 'aixprinterdescription',
        '.7': 'aixprinterlocation',
        '.8': 'aixprinterportnumber',
    }

    snmpGetTableMaps = (
        GetTableMap('Table', '.1.3.6.1.4.1.2.6.191.9.1.1.1', Table_columns),
    )

    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info('processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results

        table = tabledata.get( "Table" )
        if not table:
            log.warn('No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", getdata )
            log.warn( "Columns= %s", self.Table_columns )
            return

        relationship = self.relMap()
        maps = []
        for component in table.values():
            if not self.checkColumns(component, self.Table_columns, log):
               continue

            om = self.objectMap(component)
            log.debug( 'Found %s', om.title )
            om.id = self.prepId(om.title)
            relationship.append(om)

        maps.append(relationship)

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No printers found by %s for %s", self.name(), device.id)
           return

        return maps

