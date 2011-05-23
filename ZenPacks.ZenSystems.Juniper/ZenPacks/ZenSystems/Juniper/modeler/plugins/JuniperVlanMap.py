##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 7th, 2011
# Revised:		
#
# JuniperVlan modeler plugin
# VPNs will only be populated on SRX devices
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperVlanMap

Gather table information from Juniper Vlan tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperVlanMap(SnmpPlugin):
    """Map Juniper Vlan table to model."""
    maptype = "JuniperVlanMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperVlan"
    relname = "JuniperVl"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxExVlanTable',
                    '.1.3.6.1.4.1.2636.3.40.1.5.1.5.1',
                    {
                        '.2':  'vlanName',
                        '.3':  'vlanType',
                        '.4':  'vlanPortGroup',
                        '.5':  'vlanTag',
                    }
        ),
        GetTableMap('jnxVlanPortGroupTable',
                    '.1.3.6.1.4.1.2636.3.40.1.5.1.7.1',
                    {
                        '.3':  '_vlanPortStatus',
                    }
        ),
        GetTableMap('ifTable',
                    '.1.3.6.1.2.1.2.2.1',
                    {
                        '.1':  '_vlanIfIndex',
                        '.2':  '_vlanIfName',
                        '.6':  '_vlanIfMac',
                    }
        ),
        GetTableMap('jnxExVlanInterfaceTable',
                    '.1.3.6.1.4.1.2636.3.40.1.5.1.6.1',
                    {
                        '.2':  '_vlanIfIp',
                    }
        ),
        GetTableMap('dot1dBasePort',
                    '1.3.6.1.2.1.17.1.4.1',
                    {
                        '.1':  'basePort',
                        '.2':  'basePortIfIndex',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        vlanTable = tabledata.get('jnxExVlanTable')
        vlanPortGroupTable = tabledata.get('jnxVlanPortGroupTable')
        ifTable = tabledata.get('ifTable')
        vlanIfTable = tabledata.get('jnxExVlanInterfaceTable')
        basePortTable = tabledata.get('dot1dBasePort')

# If no data supplied then simply return
        if not vlanTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in vlanTable.items():
            try:
                om = self.objectMap(data)
                if int(om.vlanType) == 1:
                    om.vlanType = 'Static'
                elif int(om.vlanType) == 2:
                    om.vlanType = 'Dynamic'
                else:
                    om.vlanType = 'Unknown'
#                log.info(' 1st loop om.vlanType is %s, om.vlanName is %s, om.vlanPortGroup is %s' % (om.vlanType, om.vlanName, om.vlanPortGroup))
                interfaceInfo = []
                for oid1, data1 in vlanPortGroupTable.items():
                    portIndex = oid1.split('.')
                    portIndex = int(portIndex[-2])
#                    log.info(' oid1 is %s and portIndex is %s' % (oid1,portIndex))
                    if portIndex == om.vlanPortGroup:
                        ifIndex = oid1.split('.')
                        ifIndex = int(ifIndex[-1])
# This is actually the ifIndex to the port table, not the ifIndex into MIB-2 ifTable, so need to translate
                        for boid, bdata in basePortTable.items():
                            if bdata['basePort'] == ifIndex:
                                ifIndex = bdata['basePortIfIndex']
                                break
                        for oid2, data2 in ifTable.items():
#                            log.info(' 2nd loop for ifTable ifIndex is %s and portIndex is %s and data2[_vlanIfIndex] is %s' % (ifIndex, portIndex, data2['_vlanIfIndex']) )
                            if ifIndex == data2['_vlanIfIndex']:
                                ifName = data2['_vlanIfName']
                                ifMac = self.asmac(data2['_vlanIfMac'])
                                ifIp = ''
#                                log.info('3rd loop for vlaniftable ifindex is %s ifname is %s ifmac is %s ' % (ifIndex, ifName, ifMac))
                                for oid3, data3 in vlanIfTable.items():
                                    vlanIfIndex = oid3.split('.')
                                    vlanIfIndex = int(vlanIfIndex[-1])
#                                    log.info(' inside 3rd loop - vlanifindex is %s and vlanportgroup is %s' % (vlanIfIndex, om.vlanPortGroup))
                                    if vlanIfIndex == om.vlanPortGroup:
                                        hexIp = data3['_vlanIfIp']
                                        ifIp = self.binaryToIp(hexIp)
#                                ifInfo = str(ifIndex) + " " + ifName + " " + ifMac + " " + ifIp + "\n"
# Only want ifName in interfaceInfo
                                ifInfo = ifName + "\n"
                                interfaceInfo.append(ifInfo)
#                                log.info('interfaceInfo is %s' % (interfaceInfo))
                                break
                    om.vlanInterfaceInfo = ' '.join(interfaceInfo)
#                    log.info('coming out vlanname is %s vlantag is %s vlan portgroup is %s vlaninterfaceinfo is %s' % (om.vlanName, om.vlanTag, om.vlanPortGroup, om.vlanInterfaceInfo))
                om.snmpindex = oid.strip('.')
                om.id = self.prepId( om.snmpindex.replace('.','_') )
                rm.append(om)
            except AttributeError:
                log.info(' Attribute error')
                continue

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



