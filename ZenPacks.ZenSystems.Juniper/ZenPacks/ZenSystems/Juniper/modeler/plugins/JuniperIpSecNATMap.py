##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 7th, 2011
# Revised:		
#
# JuniperIpSecNAT modeler plugin
# NATs will only be populated on SRX devices
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperIpSecNATMap

Gather table information from Juniper IpSecNAT tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

def decToAscii(decName):
    """ Convert list of decimal numbers to ASCII string"""
    ascList = []
    for i in decName:
        ascList.append(chr(int(i)))
    return ''.join(ascList)

class JuniperIpSecNATMap(SnmpPlugin):
    """Map Juniper IpSecNAT table to model."""
    maptype = "JuniperIpSecNATMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperIpSecNAT"
    relname = "JuniperIpSecN"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxJsSrcNatStatsTable',
                    '.1.3.6.1.4.1.2636.3.39.1.7.1.1.4.1',
                    {
                        '.4':  'natPoolType',
                        '.5':  'natNumPorts',
                        '.6':  'natNumSess',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        natTable = tabledata.get('jnxJsSrcNatStatsTable')

# If no data supplied then simply return
        if not natTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in natTable.items():
            try:
                om = self.objectMap(data)
                om.natPoolType = self.poolTypeLookup[om.natPoolType]
# Need to extract rule name and ip address from oid - they are separated by 0
                natoid = oid.split('.')
#                log.info('natoid is %s' % (natoid))
                natRuleLen = int(natoid[0]) + 1
                natRule = decToAscii(natoid[1:natRuleLen])
                natIpAddr = '.'.join(natoid[natRuleLen+1:])
#
                om.snmpindex = oid.strip('.')
                om.natId = self.prepId(natRule + "_" + natIpAddr)
                om.id = om.natId.replace('.','_')
            except AttributeError:
                log.info(' Attribute error')
                continue
            rm.append(om)
        return rm

    poolTypeLookup = { 1: 'PAT',
                       2: 'No PAT',
                       3: 'Static',
                     }

