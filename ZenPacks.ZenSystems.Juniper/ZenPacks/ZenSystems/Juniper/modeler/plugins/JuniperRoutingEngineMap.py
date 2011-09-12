##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 1st, 2011
# Revised:		
#
# JuniperRoutingEngine modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperRoutingEngineMap

Gather table information from Juniper Contents tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperRoutingEngineMap(SnmpPlugin):
    """Map Juniper RoutingEngine table to model."""
    maptype = "JuniperRoutingEngineMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperRoutingEngine"
    relname = "JuniperRE"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxContentsTable',
                    '.1.3.6.1.4.1.2636.3.1.8.1',
                    {
                        '.1': 'containerIndex',
                        '.5': 'RoutingEngineType',
                        '.6': 'RoutingEngineDescr',
                        '.7': 'RoutingEngineSerialNo',
                        '.8': 'RoutingEngineRevision',
                        '.10': 'RoutingEnginePartNo',
                        '.11': 'RoutingEngineChassisId',
                        '.12': 'RoutingEngineChassisDescr',
                        '.13': 'RoutingEngineChassisCLEI',
                    }
        ),
        GetTableMap('jnxOperatingTable',
                    '.1.3.6.1.4.1.2636.3.1.13.1',
                    {
                        '.6': 'RoutingEngineState',
                        '.7': 'RoutingEngineTemp',
                        '.8': 'RoutingEngineCPU',
                        '.13': 'RoutingEngineUpTime',
                        '.15': 'RoutingEngineMemory',
                    }
        ),
        GetTableMap('jnxContainersTable',
                    '.1.3.6.1.4.1.2636.3.1.6.1',
                    {
                        '.1': 'containerIndex',
                        '.3': 'containerLevel',
                        '.4': 'containerNextLevel',
                        '.5': 'containerType',
                        '.6': 'containerDescr',
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
        containersTable = tabledata.get('jnxContainersTable')

# If no data supplied then simply return
        if not contentsTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in contentsTable.items():
            try:
                om = self.objectMap(data)
                RoutingEngineDescr = om.RoutingEngineDescr
#                log.info(' RoutingEngineDescr is %s ' % (om.RoutingEngineDescr))
                isaRoutingEngine = re.match(r'(.*ROUTING ENGINE.*)', RoutingEngineDescr.upper())
                if not isaRoutingEngine:
                    continue
                else:
                    for oid1, data1 in operatingTable.items():
                        if oid1 == oid:
                            om.RoutingEngineState = data1['RoutingEngineState']
                            om.RoutingEngineTemp = data1['RoutingEngineTemp']
                            om.RoutingEngineCPU = data1['RoutingEngineCPU']
                            om.RoutingEngineUpTime = data1['RoutingEngineUpTime']
                            om.RoutingEngineMemory = data1['RoutingEngineMemory']
                            for oid2, data2 in containersTable.items():
#                                log.info( ' oid is %s - oid2 is %s - data is %s' % (oid, oid2 , data2))
                                if oid.startswith(oid2):
                                    om.containerDescr = data2['containerDescr']
                                    if data2['containerLevel'] == 1:
                                        om.containerDescr = '....' + om.containerDescr
                                    elif data2['containerLevel'] == 2:
                                        om.containerDescr = '........' + om.containerDescr
                                    om.containerParentIndex = data2['containerNextLevel']
                                    if om.containerParentIndex != 0:
                                        for oid3, data3 in  containersTable.items():
                                            if oid3.endswith(str(om.containerParentIndex)):
                                                om.containerParentDescr = data3['containerDescr']
                            om.snmpindex = oid1.strip('.')
# Convert RoutingEngineUpTime from milliseconds to hours
                    om.RoutingEngineUpTime = om.RoutingEngineUpTime / 1000 / 60 / 60 /24
# Transform numeric RoutingEngineState into a status string via operatingStateLookup
                    if (om.RoutingEngineState < 1 or om.RoutingEngineState > 7):
                        om.RoutingEngineState = 1
                    om.RoutingEngineState = self.operatingStateLookup[om.RoutingEngineState]
                    om.id = self.prepId( om.RoutingEngineDescr.replace(' ','_') + '_' + str( om.snmpindex.replace('.','_') ) )
            except AttributeError:
                log.info(' Attribute error')
                continue
            rm.append(om)
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
