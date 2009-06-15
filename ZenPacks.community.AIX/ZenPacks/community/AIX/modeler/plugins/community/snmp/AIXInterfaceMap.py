###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__="""AIXInterfaceMap

InterfaceMap maps the interface and IP tables to interface objects
"""

import re
from Products.ZenUtils.Utils import cleanstring, unsigned
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class AIXInterfaceMap(SnmpPlugin):

    order = 80
    maptype = "InterfaceMap" 
    compname = "os"
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"
    deviceProperties = \
                SnmpPlugin.deviceProperties + ('zInterfaceMapIgnoreNames',
                                               'zInterfaceMapIgnoreTypes')

    snmpGetTableMaps = (
        # If table
        GetTableMap('iftable', '.1.3.6.1.2.1.2.2.1',
                {'.1': 'ifindex',
                 '.2': 'id',
                 '.3': 'type',
                 '.4': 'mtu',
                 '.5': 'speed',
                 '.6': 'macaddress',
                 '.7': 'adminStatus',
                 '.8': 'operStatus'}
        ),
        # AIX If table
        GetTableMap('aixiftable', '.1.3.6.1.4.1.2.6.191.9.8.1.1', {
                '.1': 'id',
                 '.2': 'ifindex',
                 '.3': 'aixNetworkType',
                 #'.4': 'aixNetworkInterface', # eg EN or LO or ....
                 '.5': 'aixNetworkStatus', # 1 for available, 2 for defined state
                 #'.6': 'aixNetworkLocation', # Slot number
                 '.7': 'aixNetworkDescr',
        } ),
        # ipAddrTable is the better way to get IP addresses
        GetTableMap('ipAddrTable', '.1.3.6.1.2.1.4.20.1',
                {'.1': 'ipAddress',
                 '.2': 'ifindex',
                 '.3': 'netmask'}
        ),
        # Use the ipNetToMediaTable as a backup to the ipAddrTable
        GetTableMap('ipNetToMediaTable', '.1.3.6.1.2.1.4.22.1',
                {'.1': 'ifindex',
                 '.3': 'ipaddress',
                 '.4': 'iptype'}
        ),
        # Interface Description
        GetTableMap('ifalias', '.1.3.6.1.2.1.31.1.1.1',
                {
                '.18' : 'description',
                '.15' : 'highSpeed',
                }
        ),
    )

    def process(self, device, results, log):
        """Gather SNMP information from the the standard MIB
           and match it with what AIX provides."""

        log.info( 'processing %s for device %s', self.name(), device.id)

        getdata, tabledata = results

        #
        # Find all available AIX adapters
        #
        aixiftable = tabledata.get("aixiftable")
        if aixiftable is None:
            log.error( '%s: Unable to gather data for aixiftable!', self.name() )
            return

        available_interfaces= {}
        for index, data in aixiftable.items():
            if data.get('aixNetworkStatus') != 1: # ie not in 'available' state
                continue
            id= data.get('id')
            if_type= data.get('aixNetworkType')
            if_desc= data.get('aixNetworkDescr')
            log.debug( "Found 'available' interface %s with desc= %s", id, if_desc )
            available_interfaces[ id ]= { 'description':if_desc, 'type':if_type, }

        #
        # Now match the AIX OID interfaces with the HOST-MIB OID interfaces.
        # This is necessary as we'll still be using the collectors for HOST-MIB,
        # so we'll need to keep the interface indices the same (ie all HOST-MIB indices).
        #
        iptable= tabledata.get("ipAddrTable") \
            or tabledata.get("ipNetToMediaTable")
        iftable= tabledata.get("iftable")
        ifalias= tabledata.get("ifalias")
        if iptable is None or iftable is None:
            log.error( '%s: Unable to gather HOST-MIB data!', self.name() )
            return
        if not ifalias:
            ifalias = {}

        #
        # NB: One of the issues is that the regular HOST-MIB entries find id's like
        # en2; Product: 10 Gigabit-SR Ethernet PCI-X Adapter Manufacturer: not available! Part Number: 16R0599 FRU Number: 16R0599
        #
        #      which is, of course, really annoying.  Remove any of the tripe after
        #      the first semi-colon in order to return to sanity.
        #

        #
        # add interface alias (Cisco description) to iftable
        #
        for ifidx, data in ifalias.items():
            if not iftable.has_key(ifidx):
                continue

            iftable[ifidx]['description'] = data.get('description', '')
            # if we collect ifAlias name use it
            # this is in the map subclass InterfaceAliasMap
            id = data.get('id', None)
            if id:
                semicolon_index= id.find( ';' )
                if semicolon_index != -1:
                    id= id[:semicolon_index]
                iftable[ifidx]['id'] = id

            iftable[ifidx]['description'] = data.get('description', '')
            # handle 10GB interfaces using IF-MIB::ifHighSpeed
            speed = iftable[ifidx].get('speed',0)
            if speed == 4294967295L or speed < 0:
                try: iftable[ifidx]['speed'] = data['highSpeed']*1e6
                except KeyError: pass

        for ifidx, data in iftable.items():
            try:
                data['speed'] = unsigned(data['speed'])
            except KeyError:
                pass

        rm= self.relMap()
        omtable = {}
        for ip, row in iptable.items():
            if not row.has_key("ifindex"): continue

            # Fix data up if it is from the ipNetToMediaTable.
            if len(ip.split('.')) == 5:
                if row['iptype'] != 1: continue
                ip = '.'.join(ip.split('.')[1:])
                row['netmask'] = '255.255.255.0'

            strindex = str(row['ifindex'])
            if not omtable.has_key(strindex) and not iftable.has_key(strindex):
                log.warn("skipping %s points to missing ifindex %s",
                            row.get('ipAddress',""), row.get('ifindex',""))
                continue

            if not omtable.has_key(strindex):
                log.debug( "Examining %s", iftable[strindex] )
                om = self.processInt(device, iftable[strindex], available_interfaces )
                if not om: continue
                log.debug( "Adding iface %s", om.id )
                rm.append(om)
                omtable[strindex] = om
                del iftable[strindex]
            elif omtable.has_key(strindex):
                om = omtable[strindex]
            else:
                log.warn("ip points to missing ifindex %s skipping", strindex)
                continue

            if not hasattr(om, 'setIpAddresses'): om.setIpAddresses = []
            if row.has_key('ipAddress'): ip = row['ipAddress']
            if row.has_key('netmask'): ip = ip + "/" + str(self.maskToBits(row['netmask'].strip()))
            om.setIpAddresses.append(ip)
            #om.ifindex = row.ifindex #FIXME ifindex is not set!

        for iface in iftable.values():
            log.debug( "Examining %s", iface['id'] )
            om = self.processInt(device, iface, available_interfaces )
            if om:
                log.debug( "Adding iface %s", om.id )
                rm.append(om)

        return rm



    def processInt(self, device, iface, available_interfaces ):
        """Create an object map for the iface, but only if:

           * the iface has an 'id' key
           * after cleanup, the id makes sense
           * the interface id is in the available_interfaces dictionary
           * the interface id is not in the zInterfaceMapIgnoreNames zProperty
           * the interface type is not in the zInterfaceMapIgnoreTypes zProperty
"""
        om = self.objectMap(iface)
        if not hasattr(om, 'id'): return None
        om.id = cleanstring(om.id) #take off \x00 at end of string
        # Left in interfaceName, but added title for
        # the sake of consistency
        if not om.id:
            om.id = 'Index_%s' % iface.get('ifindex', "")
        semicolon_index= om.id.find( ';' )
        if semicolon_index != -1:
            om.id= om.id[:semicolon_index]
        om.interfaceName = om.id
        om.title = om.id
        om.id = self.prepId(om.interfaceName)
        if not om.id:
            return None

        dontCollectIntNames = getattr(device, 'zInterfaceMapIgnoreNames', None)
        if (dontCollectIntNames
            and re.search(dontCollectIntNames, om.interfaceName)):
            return None

        if available_interfaces.has_key( om.id ):
            om.type= available_interfaces[ om.id ][ 'type' ]
        else:
            return None

        dontCollectIntTypes = getattr(device, 'zInterfaceMapIgnoreTypes', None)
        if dontCollectIntTypes and re.search(dontCollectIntTypes, om.type):
            return None
        if hasattr(om, 'macaddress'): om.macaddress = self.asmac(om.macaddress)
        return om

