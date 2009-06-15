__doc__="""AIXCdromMap

This modeler determines the cdrom devices on the device and updates appropriately.
Note that on AIX an hdisk may be a SAN LUN or a physical disk (pdisk).
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class AIXCdromMap(SnmpPlugin):
    """Get the AIX cdrom list"""

    maptype = "AIXCdromMap"
    modname = "ZenPacks.community.AIX.AIXCdrom"
    relname = "cdrom"
    compname = "hw"

    #
    # These column names are for the aixPvTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    Table_columns = {
        '.1': 'title', # aixCdromName
        '.2': 'snmpindex', # aixCdromIndex
        '.3': 'aixcdromtype', # aixCdromType
        '.4': 'aixcdrominterface', # aixCdromInterface
        '.5': 'aixcdromdescription', # aixCdromDescr
        '.6': 'aixcdromstatus', # aixCdromStatus
        '.7': 'aixcdromlocation', # aixCdromLocation
        '.8': 'aixcdromManufacturerName', # aixCdromManufacturerName
        '.9': 'aixcdromModelName', # aixCdromModelName
        '.10': 'aixcdromPartNumber', # aixCdromPN
        '.11': 'aixcdromFRU', # aixCdromFRU
        '.12': 'aixcdromEC', # aixCdromEC
    }

    snmpGetTableMaps = (
        GetTableMap('Table', '.1.3.6.1.4.1.2.6.191.9.5.1.1', Table_columns),
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
            om.setProductKey = MultiArgs(om.aixcdromModelName.rstrip().lstrip(), om.aixcdromManufacturerName.rstrip().lstrip())

        maps.append(relationship)

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No cdroms found by %s for %s", self.name(), device.id)
           return

        return maps

