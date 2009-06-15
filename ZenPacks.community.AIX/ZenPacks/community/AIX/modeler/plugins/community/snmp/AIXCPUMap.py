__doc__="""AIXCPUMap

This modeler determines the processors on the device and updates appropriately.
Note that on LPARs we can have *fractions* of a CPU.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class AIXCPUMap(SnmpPlugin):
    """IBM AIX cpu table"""
    
    maptype = "AIXCPUMap"  # Metadata, not explicitly called
    compname = "hw"  # hw or os | Subcomponents of the Device class. Only hw or os is allowed unless we are targetting an extended Device Class
                     # with additional subcomponents.

    relname = "cpus"  # Relationship name defined in a zenpack relationship or the base relationships
                      # the first entry in the relationship map
                      # eg    _relations = Hardware._relations + (
                      #       ("cpus", ToManyCont(ToOne, "Products.ZenModel.CPU", "hw")),

    modname = "Products.ZenModel.CPU" # the full path to the module where the class to be created is defined
                                      # If the class name is the same as the module then classname doesn't need to be defined.

    #
    # These column names are for the aixProcessorTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    cpucols = {
        '.1': 'title', # aixProcessorName
        '.2': 'snmpindex', # aixProcessorIndex
        '.3': 'setProductKey', # aixProcessorType
        #'.4': 'aixProcessorDescr',
        '.5': 'clockspeed', # aixProcessorSpeed
    }

    #
    # These column names are for the aixMemTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    cachecols = {
        '.1': 'title', # aixMemName
        '.2': 'snmpindex', # aixProcessorIndex
        #'.3': 'aixMemLocation',
        '.4': 'aixMemSize',
        #'.5': 'aixMemDescr',
    }


    snmpGetTableMaps = (
        GetTableMap( 'aixProcessorTable', '.1.3.6.1.4.1.2.6.191.9.7.1.1', cpucols),
        GetTableMap( 'aixMemTable', '.1.3.6.1.4.1.2.6.191.9.4.1.1', cachecols),
    )
    
    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info('processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results

        cache_table= tabledata.get( "aixMemTable" )
        if not cache_table:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            return

        #
        # There is only one L2 cache size
        #
        l2cache= 0
        for memory_entry in cache_table.values():
            if not self.checkColumns(memory_entry, self.cachecols, log):
               continue

            om = self.objectMap(memory_entry)

            #
            # From this same table we determine L2 cache, so determine if it's RAm or cache
            #
            if om.title[0:7] == "L2cache":
               l2cache= om.aixMemSize

        l2cache= l2cache * 1024

        cputable = tabledata.get( "aixProcessorTable" )
        if not cputable:
            log.warn('No SNMP response from %s for the %s plugin', device.id, self.name() )
            return

        relationship = self.relMap()
        maps = []
        cpumap = {}
        for cpu in cputable.values():
            if not self.checkColumns(cpu, self.cpucols, log):
               continue

            om = self.objectMap(cpu)
            om.id = self.prepId(om.title)
            log.debug( 'Found %s', om.id )
            om.setProductKey = MultiArgs(om.setProductKey, "IBM")
            om.socket = om.title

            #
            # If for some reason we get empty entries, just bail out
            #
            if not om.clockspeed or om.clockspeed <= 0:
               continue

            om.clockspeed = om.clockspeed / 10**6
            om.cacheSizeL2 = l2cache
            om._manuf = "IBM"
            relationship.append(om)

        #return rm
        maps.append(relationship)

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No filesystems found by %s for %s", self.name(), device.id)
           return

        return maps


