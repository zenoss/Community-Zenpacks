###############################################################################
#
# ActiveUserStatus modeler plugin
#
###############################################################################

__doc__ = """ ActiveUserStatus

ActiveUserStatus maps Opengear serial ports to OG-STATUS_MIB

$id: $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class ActiveUserStatus(SnmpPlugin):

    relname = "ActiveUsr"
    modname = 'ZenPacks.Opengear.ConsoleServer.ActiveUser'

    columns = {
         '.1': 'ogSerialPortActiveUsersIndex',
         '.2': 'ogSerialPortActiveUsersPort',
         '.3': 'ogSerialPortActiveUsersName',
    }

    snmpGetTableMaps = (
        GetTableMap(
            'ogSerialPortActiveUsersEntry', '.1.3.6.1.4.1.25049.16.2.1',
            columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results

        log.debug("Get Data= %s", getdata,)
        log.debug("Table Data= %s", tabledata,)

        table = tabledata.get("ogSerialPortActiveUsersEntry")
        rm = self.relMap()

        log.debug('Table Values= %s', table.values())
        for info in table.values():

            #info['dcd'] = info['ogActiveUserStatusDCD']
            #info['dtr'] = info['ogActiveUserStatusDTR']
            #info['dsr'] = info['ogActiveUserStatusDSR']
            #info['cts'] = info['ogActiveUserStatusCTS']
            #info['rts'] = info['ogActiveUserStatusRTS']

            om = self.objectMap(info)
            #om.snmpindex = int(info['ogSerialPortActiveUsersIndex'])
            om.id = self.prepId("%s_port_%s_user_%s" % (
                device.id,
                str(info['ogSerialPortActiveUsersPort']),
                str(info['ogSerialPortActiveUsersName']),
            ))

            rm.append(om)

        return [rm]
