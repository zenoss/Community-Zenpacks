__doc__="""AIXVolumeGroupMap


This modeler determines the Volume Components of an AIX Subsystem.  
It Models the Volume Group, Logical Volumes, and Disks as well as their 
sub-components.  This cannot be done with individual modelers
due to a limitation on component depth in zenoss.

Note that on AIX an hdisk may be a SAN LUN or a physical disk (pdisk).
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, \
        GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class AIXVolumeGroupMap(SnmpPlugin):
    """Get the AIX hdisk list
    Note:
      this collector has to get tricky .. it is setting up nested subcomponents for
      this relationship model

      volume_group -> logical_volume -> filesystem
                                     -> paging
      volume_group -> pdisk -> hdisk
                            -> vpath
                            -> lun
"""

    maptype = "AIXVolumeGroupMap"
    modname = "ZenPacks.community.AIX.AIXVolumeGroup" # Location of BaseClass this data will go into
    relname = "volumegroup"  # RelationShip map short name found in _relations
    compname = "os"



    #
    # This table is included for reference
    #
    aixFsType = {
         1: 'jfs',
         2: 'jfs2',
         3: 'cdrfs',
         4: 'procfs',
         5: 'cachefs',
         6: 'autofs',
         7: 'afs',
         8: 'dfs',
         9: 'nfs',
         10: 'nfs3',
         11: 'other',
    }

    #
    # These column names are for the aixPvTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    aixPvTable_columns = {
        '.1': 'title', # aixPvName
        '.2': 'aixPvNameVg',
        '.3': 'aixPvState',
        '.4': 'aixPvSize',
        '.5': 'aixPvFree',
        '.6': 'aixPvNumLVs',
        '.7': 'snmpindex', # aixPvIndex
    }

    #
    # These column names are for the aixPvTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    aixVgTable_columns = {
        '.1': 'title', # aixVgName
        '.2': 'aixVgIdentifier',
        '.3': 'aixVgState',
        '.4': 'aixVgSize',
        '.5': 'aixVgFree',
        '.6': 'aixVgCurNumLVs',
        '.7': 'aixVgOpenLVs',
        '.8': 'aixVgActiveLVs',
        '.9': 'snmpindex', # aixVgIndex
    }

    aixLvTable_columns = {
        '.1': 'title', # aixLvName
        '.2': 'aixLvNameVg',
        '.3': 'aixLvType',
        '.4': 'aixLvMountPoint',
        '.5': 'aixLvSize',
        '.6': 'aixLvState',
        '.7': 'snmpindex', # aixLvIndex
    }

    #
    # These column names are for the aixFsTable from the
    #  /usr/samples/snmpd/aixmib.my MIB file located on your AIX hosts.
    # (It's in the bos.net.tcp.adt fileset.)
    #
    aixFsTable_columns = {
         '.1': 'snmpindex', # aixFsIndex
         '.2': 'storageDevice', # aixFsName
         '.3': 'mount', # aixFsMountPoint
         '.4': 'type', # aixFsType
         '.5': 'totalBlocks', # aixFsSize - a value in MB
         '.6': 'aixFsFree',
         '.7': 'aixFsNumInodes',
         '.8': 'aixFsUsedInodes',
         '.9': 'aixFsStatus',
         '.10': 'aixFsExecution',
         '.11': 'aixFsResultMsg',
    }

    aixPagingTable_columns = {
         '.8': 'snmpindex',
         '.1': 'aixPageName',
         '.2': 'aixPageNameVg',
         '.3': 'aixPageNamePv',
         '.4': 'aixPageSize',
         '.5': 'aixPagePercentUsed',
         '.6': 'aixPageStatus',
         '.7': 'aixPageType',
    }

    snmpGetTableMaps = (
        GetTableMap('aixPvTable', '.1.3.6.1.4.1.2.6.191.2.3.1.1', aixPvTable_columns),
        GetTableMap('aixVgTable', '.1.3.6.1.4.1.2.6.191.2.1.2.1', aixVgTable_columns),
        GetTableMap('aixLvTable', '.1.3.6.1.4.1.2.6.191.2.2.1.1', aixLvTable_columns),
        GetTableMap('aixFsTable', '.1.3.6.1.4.1.2.6.191.6.2.1', aixFsTable_columns),
        GetTableMap('aixPagingTable', '.1.3.6.1.4.1.2.6.191.2.4.2.1', aixPagingTable_columns),
    )


    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info('processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results

        pv_table = tabledata.get( "aixPvTable" )
        vg_table = tabledata.get( "aixVgTable" )
        lv_table = tabledata.get( "aixLvTable" )
        fs_table = tabledata.get( "aixFsTable" )
        paging_table = tabledata.get( "aixPagingTable" )

        if not pv_table or not vg_table or not lv_table or not fs_table:
            log.warn('No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", getdata )
            return

        relationship = self.relMap()
        maps = []

        # Loop through the Volume Groups
        skipvgnames = getattr(device, 'zVolumeGroupIgnoreNames', None)
        for vg in vg_table.values():
            if not self.checkColumns(vg, self.aixVgTable_columns, log):
                log.debug("Volume Group data missing ... skipping...")
                continue
            if skipvgnames and re.search(skipvgnames, vgom.title):
                log.info("Skipping volume group %s as it matches zVolumeGroupIgnoreNames.", vgom.title)
                continue

            vgom = self.objectMap(vg)
            vgom.id = self.prepId(vgom.title)

            # Find the Physical Volumes for this Volume Group
            pv_hash={}
            for pv in pv_table.values():
                if not self.checkColumns(pv, self.aixPvTable_columns, log):
                    log.debug("Physical volume data missing ... skipping...")
                    continue
                if pv['aixPvNameVg'] == vgom.title:
                    pv_hash[pv['title']]= pv

            # Find the Logical Volumes for this Volume Group
            lv_hash={}
            skiplvnames = getattr(device, 'zLogicalVolumeIgnoreNames', None)
            for lv in lv_table.values():
                if not self.checkColumns(lv, self.aixLvTable_columns, log):
                    log.debug("logical volume data missing ... skipping...")
                    continue
                if skiplvnames and re.search(skiplvnames, lv['title']):
                    log.info("Skipping logical volume %s as it matches zLogicalVolumeIgnoreNames.", lv['title'])
                    continue
                skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
                skipfstypes = getattr(device, 'zFileSystemMapIgnoreTypes', None)
                if lv['aixLvNameVg'] == vgom.title:
                    lv_hash[lv['title']]= lv

                    # Find any Filesystems that map to the logical volume
                    for fs in fs_table.values():
                        if not self.checkColumns(fs, self.aixFsTable_columns, log):
                            log.debug("filesystem data missing ... skipping...")
                            continue
                        if fs['storageDevice'] == "/dev/"+lv['title']:
                            if skipfsnames and re.search(skipfsnames, fs['mount']):
                                log.info("Skipping %s as it matches zFileSystemMapIgnoreNames.", fs['mount'])
                                continue

                            if skipfstypes and fs['type'] in skipfstypes:
                                log.info("Skipping %s (%s) as it matches zFileSystemMapIgnoreTypes.", fs['mount'], fs['type'])
                                continue

                            if fs['totalBlocks'] <= 0:
                                log.info("Skipping %s as its totalBlocks <= 0", fs['mount'])
                                continue

                        if fs['storageDevice'] == "/dev/"+lv['title']:
                            lv_hash[lv['title']]['getFsSetup']=fs

                    # Find any Paging Spaces that map to the logical volume
                    for paging in paging_table.values():
                        if not self.checkColumns(paging, self.aixPagingTable_columns, log):
                            log.debug("paging data missing ... skipping...")
                            continue
                        if paging['aixPageName'] == lv['title']:
                            lv_hash[lv['title']]['getPagingSetup']=paging

            vgom.getPvSetup = MultiArgs(pv_hash)
            vgom.getLvSetup = MultiArgs(lv_hash)
            relationship.append(vgom)
        maps.append(relationship)
        log.debug(maps)

        #
        # As a final sanity check, see if we found anything.  If we
        # didn't find anything, that's probably an error so just return.
        #
        if len(maps) == 0:
           log.warn( "No volume groups found by %s for %s", self.name(), device.id)
           return

        # Return valid maps found
        return maps
