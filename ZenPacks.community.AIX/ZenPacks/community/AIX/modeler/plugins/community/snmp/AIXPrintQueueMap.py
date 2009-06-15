__doc__="""AIXPrintQueueMap

This modeler determines the print queues on the device and updates appropriately.
"""

import re

from Products.ZenUtils.Utils import unsigned
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class AIXPrintQueueMap(SnmpPlugin):

    maptype = "AIXPrintQueueMap"
    relname = "printqueue"
    modname = "ZenPacks.community.AIX.AIXPrintQueue"
    compname = "os" # which subcomponent to place this into .. if missing
                    # becomes root of the device

    #deviceProperties =  \
    #  SnmpPlugin.deviceProperties + ('zFileSystemMapIgnoreNames',)

    #
    # These column names are for the aixFsTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    columns = {
         '.1': 'aixprintqueuename',
         #'.2': 'aixprintqueuedevice',
         '.3': 'aixprintqueuestate',
         #'.4': 'aixprintqueueaction',
         #'.5': 'aixprintqueuedescipline',
         #'.6': 'aixprintqueueacctfile',
         #'.7': 'aixprintqueuehost',
         #'.8': 'aixprintqueueRQ',
         '.9': 'aixprintqueueJobNum',
         '.10': 'snmpindex', # special name for templates to get the snmpindex
    }

    snmpGetTableMaps = (
        GetTableMap('aixPrintQueueTable', '.1.3.6.1.4.1.2.6.191.3.1.1.1', columns),
    )

    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        #
        # Gather the data using SNMP and just exit if there's an SNMP
        # issue.  If we don't, the filesystem table in Zenoss will get
        # wiped out.  Ouch!
        #
        pqtable = tabledata.get( "aixPrintQueueTable" )
        if not pqtable:
            log.warn('No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", getdata )
            log.warn( "Columns= %s", self.columns ) 
            return

        rm = self.relMap()
        maps = []
        for pq in pqtable.values():
            if not pq.has_key("aixprintqueuename"):
               continue # Ignore blank entries

            if not self.checkColumns(pq, self.columns, log):
               log.warn( "Data= %s", getdata )
               log.warn( "Columns= %s", self.columns ) 
               continue

            om = self.objectMap(pq)
            log.debug( "Found Print Queue %s", pq['aixprintqueuename'] )


            #
            # The internal id that Zenoss uses can be used in URLs, while
            # Unix filesystem names cannot.  Map to an URL-safe name.
            #
            om.id = self.prepId(om.aixprintqueuename)

            rm.append(om)
        maps.append(rm)

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No filesystems found by %s for %s", self.name(), device.id)
           return

        return maps
