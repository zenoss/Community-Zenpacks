##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 7th, 2011
# Revised:		
#
# JuniperIpSecPolicy modeler plugin
# Policys will only be populated on SRX devices
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperIpSecPolicyMap

Gather table information from Juniper IpSecPolicy tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

def decToAscii(decName):
    """ Convert list of decimal numbers to ASCII string"""
    ascList = []
    for i in decName:
        ascList.append(chr(int(i)))
    return ''.join(ascList)

class JuniperIpSecPolicyMap(SnmpPlugin):
    """Map Juniper IpSecPolicy table to model."""
    maptype = "JuniperIpSecPolicyMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperIpSecPolicy"
    relname = "JuniperIpSecP"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxJsPolicyTable',
                    '.1.3.6.1.4.1.2636.3.39.1.4.1.1.2.1',
                    {
                        '.5':  'policyAction',
                        '.7':  'policyState',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        policyTable = tabledata.get('jnxJsPolicyTable')

# If no data supplied then simply return
        if not policyTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in policyTable.items():
            try:
                om = self.objectMap(data)
                om.policyAction = self.policyActionLookup[om.policyAction]
                om.policyState = self.policyStateLookup[om.policyState]
#
# Need to extract policyToZone, policyFromZone and PolicyName from the oid
#
#                log.info('oid is %s' % (oid))
                policyoid = oid.split('.')
#                log.info('policyoid is %s' % (policyoid))
                polFromLen = int(policyoid[0]) + 1
                om.policyFromZone = decToAscii(policyoid[1:polFromLen])
                policyoid = policyoid[polFromLen:]
                polToLen = int(policyoid[0]) + 1
                om.policyToZone  = decToAscii(policyoid[1:polToLen])
                policyoid = policyoid[polToLen:]
                polNameLen = int(policyoid[0]) + 1
                om.policyName = decToAscii(policyoid[1:polNameLen])
#                log.info('policyFromZone is %s and policyToZone is %s and policyName is %s' % (om.policyFromZone, om.policyToZone, om.policyName))
#
                om.snmpindex = oid.strip('.')
                om.policyId = self.prepId(om.policyFromZone + "_" + om.policyToZone + "_" + om.policyName )
                om.id = om.policyId.replace(' ','_')
            except AttributeError:
                log.info(' Attribute error')
                continue
            rm.append(om)
        return rm

    policyActionLookup = { 1: 'Permit',
                           2: 'Deny',
                           3: 'Reject',
                         }

    policyStateLookup = { 1: 'Active',
                          2: 'Inactive',
                          3: 'Unavailable',
                        }

