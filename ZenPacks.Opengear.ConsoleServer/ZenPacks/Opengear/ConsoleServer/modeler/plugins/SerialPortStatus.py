###############################################################################
#
# SerialPortStatus modeler plugin
#
###############################################################################

__doc__ = """ SerialPortStatus

SerialPortStatus maps Opengear serial ports to OG-STATUS_MIB

$id: $"""

__version__ = "$Revision: 1.4 $"[11:-2]

import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class SerialPortStatus(SnmpPlugin):

    relname = "SerialPrtStat"
    modname = 'ZenPacks.Opengear.ConsoleServer.SerialPortStatus'

    columns = {
         '.1': 'ogSerialPortStatusIndex',
         '.2': 'ogSerialPortStatusPort',
         '.3': 'ogSerialPortStatusRxBytes',
         '.4': 'ogSerialPortStatusTxBytes',
         '.5': 'ogSerialPortStatusSpeed',
         '.6': 'ogSerialPortStatusDCD',
         '.7': 'ogSerialPortStatusDTR',
         '.8': 'ogSerialPortStatusDSR',
         '.9': 'ogSerialPortStatusCTS',
         '.10':'ogSerialPortStatusRTS',
    }

    snmpGetTableMaps = (
        GetTableMap(
            'ogSerialPortStatusEntry', '.1.3.6.1.4.1.25049.16.1.1', columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        log.debug("Get Data= %s", getdata,)
        log.debug("Table Data= %s", tabledata,)

        table = tabledata.get("ogSerialPortStatusEntry")
        rm = self.relMap()

        log.debug('Table Values= %s', table.values())
        for info in table.values():

            info['dcd'] = info['ogSerialPortStatusDCD']
            info['dtr'] = info['ogSerialPortStatusDTR']
            info['dsr'] = info['ogSerialPortStatusDSR']
            info['cts'] = info['ogSerialPortStatusCTS']
            info['rts'] = info['ogSerialPortStatusRTS']

            om = self.objectMap(info)
            om.snmpindex = int(info['ogSerialPortStatusPort'])
            om.id = self.prepId("%s_console_%s" % (
                device.id, str(info['ogSerialPortStatusPort']),))

            rm.append(om)

        return [rm]
