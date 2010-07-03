###############################################################################
#
# SignalAlertStatus modeler plugin
#
###############################################################################

__doc__ = """ SignalAlertStatus

SignalAlertStatus maps Opengear serial ports to OG-STATUS_MIB

$id: $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class SignalAlertStatus(SnmpPlugin):

    relname = "SignalAlrt"
    modname = 'ZenPacks.Opengear.ConsoleServer.SignalAlert'

    columns = {
         '.1': 'ogSignalAlertStatusIndex',
         '.2': 'ogSignalAlertStatusPort',
         '.3': 'ogSignalAlertStatusLabel',
         '.4': 'ogSignalAlertStatusSignalName',
         '.5': 'ogSignalAlertStatusState',
    }

    snmpGetTableMaps = (
        GetTableMap(
            'ogSignalAlertStatusEntry', '.1.3.6.1.4.1.25049.16.5.1',
            columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        log.debug("Get Data= %s", getdata,)
        log.debug("Table Data= %s", tabledata,)

        table = tabledata.get("ogSignalAlertStatusEntry")
        rm = self.relMap()

        log.debug('Table Values= %s', table.values())
        for info in table.values():

            om = self.objectMap(info)
            om.snmpindex = int(info['ogSignalAlertStatusIndex'])
            om.id = self.prepId("%s_rpc_%s" % (
                device.id,
                str(info['ogSignalAlertStatusIndex']),
            ))

            rm.append(om)

        return [rm]
