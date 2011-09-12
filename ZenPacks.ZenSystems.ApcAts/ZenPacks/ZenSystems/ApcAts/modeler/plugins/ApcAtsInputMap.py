##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 7th, 2011
# Revised:		Februry 10th, 2011 - Added statuSelectedSource
#			and translation table for inputType
#
# ApcAtsInput modeler plugin
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

__doc__ = """ApcAtsInputMap

Gather table information from APC ATS devices inputs.
"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap, GetTableMap

class ApcAtsInputMap(SnmpPlugin):
    """Map APC ATS Input table to model."""
    maptype = "ApcAtsInputMap"
    modname = "ZenPacks.ZenSystems.ApcAts.ApcAtsInput"
    relname = "ApcAtsIn"
    compname = ""

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.318.1.1.8.5.1.2.0': 'statusSelectedSource',
         })

    snmpGetTableMaps = (
        GetTableMap('ApcAtsInputTable',
                    '.1.3.6.1.4.1.318.1.1.8.5.3.2.1',
                    {
                        '.2': 'inputType',
                        '.6': 'inputName',
                        '.4': 'inputFrequency',
                    }
        ),
        GetTableMap('ApcAtsInputPhaseTable',
                    '.1.3.6.1.4.1.318.1.1.8.5.3.3.1',
                    {
                        '.3': 'inputVoltage',
                    }
        ),

    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        inputtable = tabledata.get('ApcAtsInputTable')
        inputPhasetable = tabledata.get('ApcAtsInputPhaseTable')

# If no data supplied then simply return
        if not inputtable:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            log.warn( "Data= %s", tabledata )
            return
 
        for oid, data in inputtable.items():
            try:
                om = self.objectMap(data)
#                log.info("oid is  %s om.inputFrequency is %s" % (oid, om.inputFrequency))
#                log.info("inputPhasetable is   %s " % (inputPhasetable))
                for voltoid, voltdata in inputPhasetable.items():
                    if voltoid.startswith(oid):
                        om.inputVoltage = voltdata['inputVoltage']
                        om.snmpindex = voltoid.strip('.')
                om.statusSelectedSource = getdata['statusSelectedSource']
                if om.statusSelectedSource == 1:
                    om.statusSelectedSource = 'A'
                else:
                    om.statusSelectedSource = 'B'


# Decode numeric input type into descriptive string

                inputTypeNum = int(om.inputType)
                if (inputTypeNum < 1 or inputTypeNum > 3):
                    om.inputType = "Unknown"
                else:
                    om.inputType = self.inputTypeMap[inputTypeNum]
                om.inputName = om.inputName.replace(' ','_')
                om.id = self.prepId(om.inputName)
            except AttributeError:
                log.info(' Attribute error')
                continue
            rm.append(om)
#            log.info('rm %s' % (rm) )

        return rm

    inputTypeMap = { 1: 'Unknown',
                     2: 'Main',
                     3: 'Bypass'
                   }

