###############################################################################
#
# NutAlertStatus modeler plugin
#
###############################################################################

__doc__ = """ NutAlertStatus

NutAlertStatus maps Opengear serial ports to OG-STATUS_MIB

$id: $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class NutAlertStatus(SnmpPlugin):

    relname = "NutAlrt"
    modname = 'ZenPacks.Opengear.ConsoleServer.NutAlert'

    columns = {
         '.1': 'ogNutAlertStatusIndex',
         '.2': 'ogNutAlertStatusPort',
         '.3': 'ogNutAlertStatusName',
         '.4': 'ogNutAlertStatusHost',
         '.5': 'ogNutAlertStatusStatus',
    }

    snmpGetTableMaps = (
        GetTableMap(
            'ogNutAlertStatusEntry', '.1.3.6.1.4.1.25049.16.7.1',
            columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        log.debug("Get Data= %s", getdata,)
        log.debug("Table Data= %s", tabledata,)

        table = tabledata.get("ogNutAlertStatusEntry")
        rm = self.relMap()

        log.debug('Table Values= %s', table.values())
        for info in table.values():

            om = self.objectMap(info)
            om.snmpindex = int(info['ogNutAlertStatusIndex'])
            om.id = self.prepId("%s_nutAlert_%s" % (
                device.id,
                str(info['ogNutAlertStatusIndex']),
            ))

            rm.append(om)

        return [rm]
