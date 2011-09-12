##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 3rd, 2011
# Revised:
#
# ApcPduOutlet modler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """ApcPduOutletMap

Gather table information from APC PDU devices outlets.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class ApcPduOutletMap(SnmpPlugin):
    """Map APC PDU Outlet table to model."""
    maptype = "ApcPduOutletMap"
    modname = "ZenPacks.ZenSystems.ApcPdu.ApcPduOutlet"
    relname = "ApcPduOut"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('ApcPduOutletTable',
                    '.1.3.6.1.4.1.318.1.1.12.3.5.1.1',
                    {
                        '.1': 'outNumber',
                        '.2': 'outName',
                        '.4': 'outState',
                        '.6': 'outBank',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        outlettable = tabledata.get('ApcPduOutletTable')

# If no data supplied then simply return
        if not outlettable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in outlettable.items():
            try:
                om = self.objectMap(data)
                om.snmpindex = oid.strip('.')
                om.outName = om.outName.replace(' ','_')
                if int(om.outState) == 1:
                    om.outState = 'On'
                elif int(om.outState) == 2:
                    om.outState = 'Off'
                else:
                    om.outState = 'Unknown'
                om.id = self.prepId(str(om.outNumber) + "_" + om.outName)
            except AttributeError:
                continue
            rm.append(om)
        return rm


