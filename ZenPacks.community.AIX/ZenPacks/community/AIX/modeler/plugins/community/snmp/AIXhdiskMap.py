
__doc__="""AIXhdiskMap

This modeler determines the hdisk devices on the device and updates appropriately.
Note that on AIX an hdisk may be a SAN LUN or a physical disk (pdisk).
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class AIXhdiskMap(SnmpPlugin):
    """Get the AIX hdisk list"""

    maptype = "AIXhdiskMap"
    modname = "ZenPacks.community.AIX.AIXHardDisk"
    relname = "harddisks"
    compname = "hw"

    #
    # These column names are for the aixPvTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    aixHdTable_columns = {
        '.1': 'title', # aixHdName
        '.2': 'snmpindex', # aixHdIndex
        '.3': 'aixhdtype', # aixHdIndex
        '.4': 'aixhdsize', # aixHdSize
        '.5': 'aixhdinterface', # aixHdInterface
        '.6': 'aixhdstatus', # aixHdStatus
        '.7': 'aixhdlocation', # aixHdLocation
        '.8': 'aixhdidentifier', # aixHdIdentifier
        '.9': 'aixhddescription', # aixHdDescr
        '.10': 'aixhdManufacturerName', # aixHdManufacturerName
        '.11': 'aixhdModelName', # aixHdManufacturerName
        '.12': 'aixhdSerialNumber', # aixHdSN
        '.13': 'aixhdPartNumber', # aixHdPN
        '.14': 'aixhdFRU', # aixHdFRU
        '.14': 'aixhdEC', # aixHdEC
    }

    snmpGetTableMaps = (
        GetTableMap('aixHdTable', '.1.3.6.1.4.1.2.6.191.9.3.1.1', aixHdTable_columns),
    )

    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info('processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results

        hdisk_table = tabledata.get( "aixHdTable" )
        if not hdisk_table:
            log.warn('No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", getdata )
            log.warn( "Columns= %s", self.aixHdTable_columns ) 
            return

        relationship = self.relMap()
        maps = []
        for hdisk in hdisk_table.values():
            if not self.checkColumns(hdisk, self.aixHdTable_columns, log):
               continue

            om = self.objectMap(hdisk)
            log.debug( 'Found %s', om.title )
            om.id = self.prepId(om.title)
            om.setProductKey = MultiArgs(om.aixhdModelName.rstrip().lstrip(), om.aixhdManufacturerName.rstrip().lstrip())
            relationship.append(om)

        maps.append(relationship)

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No hdisks found by %s for %s", self.name(), device.id)
           return

        return maps

