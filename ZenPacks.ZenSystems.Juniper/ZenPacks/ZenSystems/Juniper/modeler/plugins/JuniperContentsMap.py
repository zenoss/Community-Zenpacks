##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 16th, 2011
# Revised:		
#
# JuniperContents modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperContentsMap

Gather table information from Juniper Contents tables
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperContentsMap(SnmpPlugin):
    """Map Juniper Contents table to model."""
    maptype = "JuniperContentsMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperContents"
    relname = "JuniperConte"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxContentsTable',
                    '.1.3.6.1.4.1.2636.3.1.8.1',
                    {
                        '.1': 'containerIndex',
                        '.5': 'contentsType',
                        '.6': 'contentsDescr',
                        '.7': 'contentsSerialNo',
                        '.8': 'contentsRevision',
                        '.10': 'contentsPartNo',
                        '.11': 'contentsChassisId',
                        '.12': 'contentsChassisDescr',
                        '.13': 'contentsChassisCLEI',
                    }
        ),
        GetTableMap('jnxOperatingTable',
                    '.1.3.6.1.4.1.2636.3.1.13.1',
                    {
                        '.6': 'contentsState',
                        '.7': 'contentsTemp',
                        '.8': 'contentsCPU',
                        '.13': 'contentsUpTime',
                        '.15': 'contentsMemory',
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
                for oid1, data1 in operatingTable.items():
                    if oid1 == oid:
                        om.contentsState = data1['contentsState']
                        om.contentsTemp = data1['contentsTemp']
                        om.contentsCPU = data1['contentsCPU']
                        om.contentsUpTime = data1['contentsUpTime']
                        om.contentsMemory = data1['contentsMemory']
                        for oid2, data2 in containersTable.items():
#                            log.info( ' oid is %s - oid2 is %s - data is %s' % (oid, oid2 , data2))
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
# Convert contentsUpTime from milliseconds to hours
                om.contentsUpTime = om.contentsUpTime / 1000 / 60 / 60 /24
# Transform numeric contentsState into a status string via operatingStateLookup
                if (om.contentsState < 1 or om.contentsState > 7):
                    om.contentsState = 1
                om.contentsState = self.operatingStateLookup[om.contentsState]
                om.id = self.prepId( om.contentsDescr.replace(' ','_') + '_' + str( om.snmpindex.replace('.','_') ) )
#                om.id = self.prepId(om.snmpindex)
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
