###############################################################################
#
# EmdStatus modeler plugin
#
###############################################################################

__doc__ = """ EmdStatus

EmdStatus maps Opengear serial ports to OG-STATUS_MIB

$id: $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class EmdStatus(SnmpPlugin):

    relname = "EmdStat"
    modname = 'ZenPacks.Opengear.ConsoleServer.EmdStatus'

    columns = {
         '.1': 'ogEmdStatusIndex',
         '.2': 'ogEmdStatusName',
         '.3': 'ogEmdStatusTemp',
         '.4': 'ogEmdStatusHumidity',
         '.5': 'ogEmdStatusAlertCount',
    }

    snmpGetTableMaps = (
        GetTableMap(
            'ogEmdStatusEntry', '.1.3.6.1.4.1.25049.16.4.1',
            columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        log.debug("Get Data= %s", getdata,)
        log.debug("Table Data= %s", tabledata,)

        table = tabledata.get("ogEmdStatusEntry")
        rm = self.relMap()

        log.debug('Table Values= %s', table.values())
        for info in table.values():

            om = self.objectMap(info)
            #om.snmpindex = int(info['ogEmdStatusIndex'])
            om.id = self.prepId("%s_emdStatus_%s" % (
                device.id,
                str(info['ogEmdStatusName']),
            ))

            rm.append(om)

        return [rm]
