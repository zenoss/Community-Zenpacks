###############################################################################
#
# EnvironmentAlertStatus modeler plugin
#
###############################################################################

__doc__ = """ EnvironmentAlertStatus

EnvironmentAlertStatus maps Opengear serial ports to OG-STATUS_MIB

$id: $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class EnvironmentAlertStatus(SnmpPlugin):

    relname = "EnvironmentAlrt"
    modname = 'ZenPacks.Opengear.ConsoleServer.EnvironmentAlert'

    columns = {
         '.1': 'ogEnvAlertStatusIndex',
         '.2': 'ogEnvAlertStatusDevice',
         '.3': 'ogEnvAlertStatusSensor',
         '.4': 'ogEnvAlertStatusOutlet',
         '.5': 'ogEnvAlertStatusValue',
         '.6': 'ogEnvAlertStatusOldValue',
         '.6': 'ogEnvAlertStatusStatus',
    }

    snmpGetTableMaps = (
        GetTableMap(
            'ogEnvAlertStatusEntry', '.1.3.6.1.4.1.25049.16.6.1',
            columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        log.debug("Get Data= %s", getdata,)
        log.debug("Table Data= %s", tabledata,)

        table = tabledata.get("ogEnvAlertStatusEntry")
        rm = self.relMap()

        log.debug('Table Values= %s', table.values())
        for info in table.values():

            om = self.objectMap(info)
            om.snmpindex = int(info['ogEnvAlertStatusIndex'])
            om.id = self.prepId("%s_envAlert_%s" % (
                device.id,
                str(info['ogEnvAlertStatusIndex']),
            ))

            rm.append(om)

        return [rm]
