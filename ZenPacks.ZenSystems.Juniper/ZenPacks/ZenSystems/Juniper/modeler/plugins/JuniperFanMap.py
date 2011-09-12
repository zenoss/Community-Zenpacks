##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 17th, 2011
# Revised:		
#
# JuniperFan modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperFanMap

Gather table information from Juniper Fan tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperFanMap(SnmpPlugin):
    """Map Juniper Fan table to model."""
    maptype = "JuniperFanMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('jnxContentsTable',
                    '.1.3.6.1.4.1.2636.3.1.8.1',
                    {
                        '.1': 'fanContainerIndex',
                        '.5': 'fanType',
                        '.6': 'fanDescr',
                        '.7': 'fanSerialNo',
                        '.8': 'fanRevision',
#                        '.10': 'fanPartNo',
                        '.11': 'fanChassisId',
                    }
        ),
        GetTableMap('jnxOperatingTable',
                    '.1.3.6.1.4.1.2636.3.1.13.1',
                    {
                        '.6': 'fanState',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        contentsTable = tabledata.get('jnxContentsTable')
        operatingTable = tabledata.get('jnxOperatingTable')

# If no data supplied then simply return
        if not contentsTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in contentsTable.items():
            try:
                om = self.objectMap(data)
                fandescr = om.fanDescr
                isaFan = re.match(r'(.*FAN.*)', fandescr.upper())
                if not isaFan:
                    continue
                else:
                    for oid1, data1 in operatingTable.items():
                        if oid1 == oid:
                            om.fanState = data1['fanState']
                            om.snmpindex = oid1.strip('.')
# Transform numeric fanState into a status string via operatingStateLookup
                    if (om.fanState < 1 or om.fanState > 7):
                        om.fanState = 1
                    om.fanState = self.operatingStateLookup[om.fanState]
                    om.id = self.prepId(om.snmpindex)
                    rm.append(om)
            except AttributeError:
                log.info(' Attribute error')
                continue
#            log.info('rm %s' % (rm) )

        return rm

    operatingStateLookup = { 1: 'Unknown',
                             2: 'Running',
                             3: 'Ready',
                             4: 'Reset',
                             5: 'RunningAtFullSpeed (Fan)',
                             6: 'Down',
                             7: 'Standby'
                           }
