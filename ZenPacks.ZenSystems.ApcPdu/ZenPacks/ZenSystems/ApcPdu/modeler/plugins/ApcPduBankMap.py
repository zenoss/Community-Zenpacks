##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 3rd, 2011
# Revised:
#
# ApcPduBank modler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """ApcPduBankMap

Gather table information from APC PDU devices banks.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class ApcPduBankMap(SnmpPlugin):
    """Map APC PDU Bank table to model."""
    maptype = "ApcPduBankMap"
    modname = "ZenPacks.ZenSystems.ApcPdu.ApcPduBank"
    relname = "ApcPduBan"
    compname = ""

    snmpGetTableMaps = (
        GetTableMap('ApcPduBankTable',
                    '.1.3.6.1.4.1.318.1.1.12.2.3.1.1',
                    {
                        '.5': 'bankNumber',
                        '.3': 'bankState',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        banktable = tabledata.get('ApcPduBankTable')

# If no data supplied then simply return
        if not banktable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in banktable.items():
            try:
                om = self.objectMap(data)
# Map bank state so 1 (Normal) -> sev 0, 3 (near o'load) -> sev 4 and 4 (oload) -> 5
                if (om.bankState < 1 or om.bankState > 4):
                    om.bankState = 0
                index = om.bankState
                om.bankState = self.bankStateMap[index][0]
                om.bankStateText = self.bankStateMap[index][1]
                om.snmpindex = oid.strip('.')
                om.id = "Object_Id_" + self.prepId(str(om.bankNumber))
            except AttributeError:
                continue
            rm.append(om)
        return rm

    bankStateMap  = { 0: (2, 'Unknown'),
                      1: (0, 'Normal'),
                      2: (2, 'Low Load'),
                      3: (4, 'Near Overload'),
                      4: (5, 'Overload')
                    }

