##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 2nd, 2011
# Revised:		
#
# JuniperBaseComp modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperBaseCompMap

Gather table information from Juniper Contents tables
"""

import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperBaseCompMap(SnmpPlugin):
    """Map Juniper BaseComp table to model."""
    maptype = "JuniperBaseCompMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperBaseComp"
    relname = "JuniperBC"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxContentsTable',
                    '.1.3.6.1.4.1.2636.3.1.8.1',
                    {
                        '.1': 'containerIndex',
                        '.5': 'BaseCompType',
                        '.6': 'BaseCompDescr',
                        '.7': 'BaseCompSerialNo',
                        '.8': 'BaseCompRevision',
                        '.10': 'BaseCompPartNo',
                        '.11': 'BaseCompChassisId',
                        '.12': 'BaseCompChassisDescr',
                        '.13': 'BaseCompChassisCLEI',
                    }
        ),
        GetTableMap('jnxOperatingTable',
                    '.1.3.6.1.4.1.2636.3.1.13.1',
                    {
                        '.6': 'BaseCompState',
                        '.7': 'BaseCompTemp',
                        '.8': 'BaseCompCPU',
                        '.13': 'BaseCompUpTime',
                        '.15': 'BaseCompMemory',
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

    bCRegex = (
        # 'node0 midplane' or simply 'midplane'
        re.compile(r'(.*MIDPLANE.*)'),
        # 'node0 USB Hub' or simple 'USB Hub'
        re.compile(r'(.*USB HUB.*)'),
        # TFEB Intake temperature sensor
        re.compile(r'(.*TFEB.*)'),
        # CB 0
        re.compile(r'(.*CB.*)'),
        # FPM Board
        re.compile(r'(.*FPM.*)'),
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
                BaseCompDescr = om.BaseCompDescr
                BaseCompDescr = BaseCompDescr.upper()
                for regex in self.bCRegex:
                    m = regex.search(BaseCompDescr)
#                    log.info(' regex is %s and BaseCompDescr is %s' % (m, BaseCompDescr))
                    if not m:
                        continue
                    else:
                        for oid1, data1 in operatingTable.items():
                            if oid1 == oid:
                                om.BaseCompState = data1['BaseCompState']
                                om.BaseCompTemp = data1['BaseCompTemp']
                                om.BaseCompCPU = data1['BaseCompCPU']
                                om.BaseCompUpTime = data1['BaseCompUpTime']
                                om.BaseCompMemory = data1['BaseCompMemory']
                                for oid2, data2 in containersTable.items():
#                                    log.info( ' oid is %s - oid2 is %s - data is %s' % (oid, oid2 , data2))
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
# Convert BaseCompUpTime from milliseconds to hours
                        om.BaseCompUpTime = om.BaseCompUpTime / 1000 / 60 / 60 /24
# Transform numeric BaseCompState into a status string via operatingStateLookup
                        if (om.BaseCompState < 1 or om.BaseCompState > 7):
                            om.BaseCompState = 1
                        om.BaseCompState = self.operatingStateLookup[om.BaseCompState]
                        om.id = self.prepId( om.BaseCompDescr.replace(' ','_') + '_' + str( om.snmpindex.replace('.','_') ) )
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
