##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 3rd, 2011
# Revised:		Feb 11th, 2011
#			Collect single instance power supply info
#			and set snmpindex to 0
#
# ApcPduPS modler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """ApcPduPSMap

Gather table information from APC PDU devices power supplies.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class ApcPduPSMap(SnmpPlugin):
    """Map APC PDU power supply data to model. These are scalars not table."""
    maptype = "ApcPduPSMap"
    modname = "ZenPacks.ZenSystems.ApcPdu.ApcPduPS"
    relname = "ApcPduP"
    compname = ""

    snmpGetMap = GetMap({
                    '.1.3.6.1.4.1.318.1.1.12.4.1.1.0'	: 'supply1Status',
                    '.1.3.6.1.4.1.318.1.1.12.4.1.2.0'	: 'supply2Status',
                    })

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if not getdata:
            log.warn(' No SNMP response from %s for the %s plugin ' % ( device.id, self.name ) )
            return
        rm = self.relMap()
        om = self.objectMap(getdata)
        if int(om.supply1Status == 1):
            om.supply1Status = 'OK'
        elif int(om.supply1Status == 2):
            om.supply1Status = 'Failed'
        else:
            om.supply1Status = 'Unknown'

        if int(om.supply2Status == 1):
            om.supply2Status = 'OK'
        elif int(om.supply2Status == 2):
            om.supply2Status = 'Failed'
        else:
            om.supply2Status = 'Unknown'
        om.id = "Power_Supplies"
        om.id = self.prepId(om.id)
# Fix om.snmpindex to 0 as this is a scalar
        om.snmpindex = '0'
        rm.append(om)
        return rm


