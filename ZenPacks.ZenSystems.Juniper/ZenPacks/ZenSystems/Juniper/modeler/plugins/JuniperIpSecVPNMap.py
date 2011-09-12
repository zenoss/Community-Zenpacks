##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 3rd, 2011
# Revised:		
#
# JuniperIpSecVPN modeler plugin
# VPNs will only be populated on SRX devices
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperIpSecVPNMap

Gather table information from Juniper IpSecVPN tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperIpSecVPNMap(SnmpPlugin):
    """Map Juniper IpSecVPN table to model."""
    maptype = "JuniperIpSecVPNMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperIpSecVPN"
    relname = "JuniperIpSecV"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxIkeTunnelMonEntry',
                    '.1.3.6.1.4.1.2636.3.52.1.1.2.1',
                    {
                        '.4':  'vpnPhase1LocalGwAddr',
                        '.6':  'vpnPhase1State',
                        '.11':  'vpnPhase1LocalIdValue',
                        '.14':  'vpnPhase1RemoteIdValue',
                    }
        ),
        GetTableMap('jnxIpSecTunnelMonEntry',
                    '.1.3.6.1.4.1.2636.3.52.1.2.2.1',
                    {
                        '.5':  'vpnPhase2LocalGwAddr',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        phase1Table = tabledata.get('jnxIkeTunnelMonEntry')
        phase2Table = tabledata.get('jnxIpSecTunnelMonEntry')

# If no data supplied then simply return
        if not phase1Table:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        p1Count = 0
        for oid, data in phase1Table.items():
            try:
                om = self.objectMap(data)
                if int(om.vpnPhase1State) == 1:
                    om.vpnPhase1State = 'Up'
                else:
                    om.vpnPhase1State = 'Down'
                om.snmpindex = oid.strip('.')
                om.id = self.prepId( om.snmpindex.replace('.','_') )
                p1Count = p1Count + 1
            except AttributeError:
                log.info(' Attribute error')
                continue
            p2Count = 0
            for oid2, data2 in phase2Table.items():
                try:
                    om.vpnPhase2LocalGwAddr = data2['vpnPhase2LocalGwAddr']
                    p2Count = p2Count + 1
                except AttributeError:
                    log.info(' Attribute error')
                    continue
#            log.info('rm %s p1Count is %s and p2Count is %s' % (rm, p1Count, p2Count) )
            rm.append(om)

        return rm


