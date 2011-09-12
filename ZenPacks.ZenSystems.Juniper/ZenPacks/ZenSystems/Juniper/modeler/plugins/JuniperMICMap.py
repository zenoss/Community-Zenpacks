##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 2nd, 2011
# Revised:		
#
# JuniperMIC modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperMICMap

Gather table information from Juniper Contents tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperMICMap(SnmpPlugin):
    """Map Juniper MIC table to model."""
    maptype = "JuniperMICMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperMIC"
    relname = "JuniperMI"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxContentsTable',
                    '.1.3.6.1.4.1.2636.3.1.8.1',
                    {
                        '.1': 'containerIndex',
                        '.5': 'MICType',
                        '.6': 'MICDescr',
                        '.7': 'MICSerialNo',
                        '.8': 'MICRevision',
                        '.10': 'MICPartNo',
                        '.11': 'MICChassisId',
                        '.12': 'MICChassisDescr',
                        '.13': 'MICChassisCLEI',
                    }
        ),
        GetTableMap('jnxOperatingTable',
                    '.1.3.6.1.4.1.2636.3.1.13.1',
                    {
                        '.6': 'MICState',
                        '.7': 'MICTemp',
                        '.8': 'MICCPU',
                        '.13': 'MICUpTime',
                        '.15': 'MICMemory',
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
                MICDescr = om.MICDescr
#                log.info(' MICDescr is %s ' % (om.MICDescr))
                isaMIC = re.match(r'(.*MIC.*)', MICDescr.upper())
                if not isaMIC:
                    continue
                else:
                    for oid1, data1 in operatingTable.items():
                        if oid1 == oid:
                            om.MICState = data1['MICState']
                            om.MICTemp = data1['MICTemp']
                            om.MICCPU = data1['MICCPU']
                            om.MICUpTime = data1['MICUpTime']
                            om.MICMemory = data1['MICMemory']
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
# Convert MICUpTime from milliseconds to hours
                    om.MICUpTime = om.MICUpTime / 1000 / 60 / 60 /24
# Transform numeric MICState into a status string via operatingStateLookup
                    if (om.MICState < 1 or om.MICState > 7):
                        om.MICState = 1
                    om.MICState = self.operatingStateLookup[om.MICState]
                    om.id = self.prepId( om.MICDescr.replace(' ','_') + '_' + str( om.snmpindex.replace('.','_') ) )
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
