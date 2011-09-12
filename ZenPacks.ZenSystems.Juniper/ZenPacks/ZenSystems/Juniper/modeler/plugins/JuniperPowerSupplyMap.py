##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 1st, 2011
# Revised:		
#
# JuniperPowerSupply modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperPowerSupplyMap

Gather table information from Juniper PowerSupply tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperPowerSupplyMap(SnmpPlugin):
    """Map Juniper PowerSupply table to model."""
    maptype = "JuniperPowerSupplyMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperPowerSupply"
    relname = "powersupplies"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('jnxContentsTable',
                    '.1.3.6.1.4.1.2636.3.1.8.1',
                    {
                        '.1': 'powerSupplyContainerIndex',
                        '.5': 'powerSupplyType',
                        '.6': 'powerSupplyDescr',
                        '.7': 'powerSupplySerialNo',
                        '.8': 'powerSupplyRevision',
                        '.10': 'powerSupplyPartNo',
                        '.11': 'powerSupplyChassisId',
                    }
        ),
        GetTableMap('jnxOperatingTable',
                    '.1.3.6.1.4.1.2636.3.1.13.1',
                    {
                        '.6': 'powerSupplyState',
                        '.7': 'powerSupplyTemp',
                        '.8': 'powerSupplyCPU',
                        '.13': 'powerSupplyUpTime',
                        '.15': 'powerSupplyMemory',
                    }
        ),
    )
    pSRegex = (
        # Power Supply 0
        re.compile(r'(^POWER SUPPLY.*)'),
        # PEM 0
        re.compile(r'(.*PEM.*)'),
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
                powerSupplydescr = om.powerSupplyDescr
                powerSupplydescr = powerSupplydescr.upper()
                for regex in self.pSRegex:
#                    log.info(' regex is %s and powerSupplyDescr is %s' % (regex, powerSupplydescr))
                    m = regex.search(powerSupplydescr)
                    if not m:
                        continue
                    else:
                        for oid1, data1 in operatingTable.items():
                            if oid1 == oid:
                                om.powerSupplyTemp = data1['powerSupplyTemp']
                                om.powerSupplyCPU = data1['powerSupplyCPU']
                                om.powerSupplyMemory = data1['powerSupplyMemory']
                                om.powerSupplyUpTime = data1['powerSupplyUpTime']
                                om.powerSupplyState = data1['powerSupplyState']
                                om.snmpindex = oid1.strip('.')
# Convert powerSupplyUpTime from milliseconds to hours
                        om.powerSupplyUpTime = om.powerSupplyUpTime / 1000 / 60 / 60 /24

# Transform numeric powerSupplyState into a status string via operatingStateLookup
                        if (om.powerSupplyState < 1 or om.powerSupplyState > 7):
                            om.powerSupplyState = 1
                        om.powerSupplyState = self.operatingStateLookup[om.powerSupplyState]
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
