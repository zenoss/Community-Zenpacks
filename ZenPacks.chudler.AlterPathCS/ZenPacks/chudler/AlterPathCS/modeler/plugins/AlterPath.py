import Globals
from Products.DataCollector.plugins.CollectorPlugin \
     import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps \
     import ObjectMap

class AlterPath(SnmpPlugin):

    relname = "terminals"
    modname = 'ZenPacks.chudler.AlterPathCS.Terminal'
    
    columns = {
         '.1': 'snmpindex',
         '.2': 'deviceName',
         '.3': 'serverAlias',
         '.5': 'txBytes',
         '.6': 'rxBytes',
         '.15': 'CTS',
         '.12': 'DCD',
         }

    snmpGetTableMaps = (
        GetTableMap('cyacsinfo', '.1.3.6.1.4.1.2925.4.3.1.1', columns),
    )

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        table = tabledata.get("cyacsinfo")
        rm = self.relMap()
        for info in table.values():
            info['connected'] = info['CTS'] == 1
            info['up'] = info['DCD'] == 1
            om = self.objectMap(info)
            om.id = self.prepId(om.deviceName)
            rm.append(om)
        return [rm]
