
__doc__="""AIXmemory

This modeler determines the total amount of memory on the device and updates appropriately.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class AIXmemory(SnmpPlugin):
    """Map IBM AIX memory table"""

    maptype = "AIXmemory"
    compname = "hw"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"

    #
    # These column names are for the aixMemTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #

    columns = {
        '.1': 'title', # aixMemName
        '.2': 'snmpindex', # aixMemIndex
        #'.3': 'aixMemLocation',
        '.4': 'aixMemSize',
        #'.5': 'aixMemDescr',
    }

    snmpGetTableMaps = (
        GetTableMap( 'aixMemTable', '.1.3.6.1.4.1.2.6.191.9.4.1.1', columns),
    )

    active= 1  # aixPageStatus.active == 1

    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info( 'processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results

        memory_table = tabledata.get( "aixMemTable" )
        if not memory_table:
            log.warn('No SNMP response from %s for the %s plugin', device.id, self.name() )
            return

        #
        # Unfortunately Zenoss doesn't seem to gather more detailed info
        # about paging spaces
        #
        maps = []
        totalMemory= 0
        for memory_entry in memory_table.values():
            if not self.checkColumns(memory_entry, self.columns, log):
               continue

            om = self.objectMap(memory_entry)

            #
            # From this same table we determine L2 cache, so determine if it's RAm or cache
            #
            if om.title[0:3] == "mem":
               totalMemory= totalMemory + om.aixMemSize * 1024 * 1024

        log.info( "Found %s Bytes of RAM found by %s for %s", totalMemory, self.name(), device.id)
        maps.append(ObjectMap({"totalMemory": totalMemory}, compname="hw"))

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No RAM found by %s for %s", self.name(), device.id)
           return

        return maps


