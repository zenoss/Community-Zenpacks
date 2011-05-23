##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 28th, 2011
# Revised:		
#
# JuniperBGP modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperBGPMap

Gather table information from Juniper BGP tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperBGPMap(SnmpPlugin):
    """Map Juniper BGP table to model."""
    maptype = "JuniperBGPMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperBGP"
    relname = "JuniperBG"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxBgpM2PeerTable',
#                    '.1.3.6.1.4.1.2636.5.1.1.2.1.1.1',
                    '.1.3.6.1.2.1.15.3.1',
                    {
                        '.2':  'bgpStateInt',
                        '.5':  'bgpLocalAddress',
                        '.7':  'bgpRemoteAddress',
                        '.9':  'bgpRemoteASN',
                        '.16': 'bgpLastUpDown',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        bgpTable = tabledata.get('jnxBgpM2PeerTable')

# If no data supplied then simply return
        if not bgpTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in bgpTable.items():
            try:
                om = self.objectMap(data)
                if (om.bgpStateInt < 1 or om.bgpStateInt > 6):
                    om.bgpStateInt = 0
                om.bgpStateText = self.operatingStateLookup[om.bgpStateInt]
                om.bgpLastUpDown = om.bgpLastUpDown / 60 / 60 / 24
                om.snmpindex = oid.strip('.')
                tempname = om.bgpLocalAddress.replace(' ','_')
                tempname = tempname.replace('.','_')
                om.id = self.prepId( tempname + '_' + str( om.snmpindex.replace('.','_') ) )
            except AttributeError:
                log.info(' Attribute error')
                continue
            rm.append(om)
#            log.info('rm %s' % (rm) )

        return rm

    def hexToIp(self,hexAddr):
        ipAddr=[]
        hexAddrList = hexAddr.split(' ')
        for i in hexAddrList:
            ipAddr.append(str(int(i,16)))
        return '.'.join(ipAddr)

    def binaryToIp(self, binAddr):
        ipAddr = []
        for i in binAddr:
            ipAddr.append(str(ord(i)))
        return '.'.join(ipAddr)

    operatingStateLookup = { 0: 'Unknown',
                             1: 'Idle',
                             2: 'Connect',
                             3: 'Active',
                             4: 'OpenSent',
                             5: 'OpenConfirm',
                             6: 'Established',
                           }

