__doc__="""AIXLparInfoMap

This modeler determines the lpar info
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap

class AIXLparInfoMap(SnmpPlugin):
    """Get the AIX Lpar Info"""

    maptype = "AIXLparInfoMap"
    modname = "ZenPacks.community.AIX.AIXLparInfo"
    relname = "lparinfo"
    compname = "hw"

    #
    # These column names are for the aixPvTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    Table_columns = {
        '.12': 'maxmem',
        '.13': 'minmem',
        '.15': 'lparnum',
        '.16': 'shared', # 0=dedicated, 1=shared
        '.17': 'capped', # 0=uncapped, 1=Capped
        '.18': 'smt',
        '.20': 'minvcpu',
        '.21': 'maxvcpu',
        '.22': 'mincap',
        '.23': 'maxcap',
        '.25': 'onlinemem',
        '.28': 'vcpu',
        '.32': 'entitledcap',
        '.33': 'weight',
        '.37': 'entitledpct',
    }

    snmpGetTableMaps = (
        GetTableMap('Table', '1.3.6.1.4.1.2.3.1.2.2.2.1.18', Table_columns),
    )

    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info('processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results

        table = tabledata.get( "Table" )
        om = self.objectMap(table)
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
            om.id = self.prepId('lparinfo')
            relationship.append(om)
        maps.append(relationship)

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No filesystems found by %s for %s", self.name(), device.id)
           return
        log.debug(maps)
        return maps

