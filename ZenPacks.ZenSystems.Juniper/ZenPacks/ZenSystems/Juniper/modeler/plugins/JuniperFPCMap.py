##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 28th, 2011
# Revised:		
#
# JuniperFPC modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperFPCMap

Gather table information from Juniper Contents tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperFPCMap(SnmpPlugin):
    """Map Juniper FPC table to model."""
    maptype = "JuniperFPCMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperFPC"
    relname = "JuniperFP"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxContentsTable',
                    '.1.3.6.1.4.1.2636.3.1.8.1',
                    {
                        '.1': 'containerIndex',
                        '.5': 'FPCType',
                        '.6': 'FPCDescr',
                        '.7': 'FPCSerialNo',
                        '.8': 'FPCRevision',
                        '.10': 'FPCPartNo',
                        '.11': 'FPCChassisId',
                        '.12': 'FPCChassisDescr',
                        '.13': 'FPCChassisCLEI',
                    }
        ),
        GetTableMap('jnxOperatingTable',
                    '.1.3.6.1.4.1.2636.3.1.13.1',
                    {
                        '.6': 'FPCState',
                        '.7': 'FPCTemp',
                        '.8': 'FPCCPU',
                        '.13': 'FPCUpTime',
                        '.15': 'FPCMemory',
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
                FPCDescr = om.FPCDescr
#                log.info(' FPCDescr is %s ' % (om.FPCDescr))
                isaFPC = re.match(r'(.*FPC.*)', FPCDescr.upper())
                if not isaFPC:
                    continue
                else:
                    for oid1, data1 in operatingTable.items():
                        if oid1 == oid:
                            om.FPCState = data1['FPCState']
                            om.FPCTemp = data1['FPCTemp']
                            om.FPCCPU = data1['FPCCPU']
                            om.FPCUpTime = data1['FPCUpTime']
                            om.FPCMemory = data1['FPCMemory']
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
# Convert FPCUpTime from milliseconds to hours
                    om.FPCUpTime = om.FPCUpTime / 1000 / 60 / 60 /24
# Transform numeric FPCState into a status string via operatingStateLookup
                    if (om.FPCState < 1 or om.FPCState > 7):
                        om.FPCState = 1
                    om.FPCState = self.operatingStateLookup[om.FPCState]
                    om.id = self.prepId( om.FPCDescr.replace(' ','_') + '_' + str( om.snmpindex.replace('.','_') ) )
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
