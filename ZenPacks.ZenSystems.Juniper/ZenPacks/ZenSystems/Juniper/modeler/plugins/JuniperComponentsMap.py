##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 24th, 2011
# Revised:		
#
# JuniperComponents modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """JuniperComponentsMap

Gather table information from Juniper Components tables
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class JuniperComponentsMap(SnmpPlugin):
    """Map Juniper Components table to model."""
    maptype = "JuniperComponentsMap"
    modname = "ZenPacks.ZenSystems.Juniper.JuniperComponents"
    relname = "JuniperComp"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('jnxContentsTable',
                    '.1.3.6.1.4.1.2636.3.1.8.1',
                    {
                        '.1': 'containerIndex',
                        '.5': 'contentsType',
                        '.6': 'contentsDescr',
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
        containersTable = tabledata.get('jnxContainersTable')

# If no data supplied then simply return
        if not containersTable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in containersTable.items():
            try:
                om = self.objectMap(data)
                if om.containerLevel == 1:
                    om.containerDescr = '....' + om.containerDescr
                elif om.containerLevel == 2:
                    om.containerDescr = '........' + om.containerDescr
                om.containerParentIndex = om.containerNextLevel
                if om.containerParentIndex != 0:
#                    log.info(' om.containerParentIndex is %s  and om.containerDescr is %s ' % (om.containerParentIndex, om.containerDescr) )
                    for oid1,data1 in containersTable.items():
                        if oid1.endswith(str(om.containerParentIndex)):
#                            log.info('self descr is %s  parent Descr is %s and oid1 is %s' % (om.containerDescr, data1['containerDescr'], oid1) )
                            om.containerParentDescr = data1['containerDescr']
                om.snmpindex = oid.strip('.')
                tempname = om.containerDescr.replace(' ','_')
                tempname = tempname.replace('.','')
                om.id = self.prepId( tempname + '_' + str( om.snmpindex.replace('.','_') ) )
            except AttributeError:
                log.info(' Attribute error')
                continue
            rm.append(om)
#            log.info('rm %s' % (rm) )

        return rm
