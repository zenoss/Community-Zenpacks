###############################################################################
#
# RpcStatus modeler plugin
#
###############################################################################

__doc__ = """ RpcStatus

RpcStatus maps Opengear serial ports to OG-STATUS_MIB

$id: $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class RpcStatus(SnmpPlugin):

    relname = "RpcStat"
    modname = 'ZenPacks.Opengear.ConsoleServer.RpcStatus'

    columns = {
         '.1': 'ogRpcStatusIndex',
         '.2': 'ogRpcStatusName',
         '.3': 'ogRpcStatusMaxTemp',
         '.4': 'ogRpcStatusAlertCount',
    }

    snmpGetTableMaps = (
        GetTableMap(
            'ogRpcStatusEntry', '.1.3.6.1.4.1.25049.16.3.1',
            columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        log.debug("Get Data= %s", getdata,)
        log.debug("Table Data= %s", tabledata,)

        table = tabledata.get("ogRpcStatusEntry")
        rm = self.relMap()

        log.debug('Table Values= %s', table.values())
        for info in table.values():

            om = self.objectMap(info)
            #om.snmpindex = int(info['ogRpcStatusIndex'])
            om.id = self.prepId("%s_rpcStatus_%s" % (
                device.id,
                str(info['ogRpcStatusName']),
            ))

            rm.append(om)

        return [rm]
