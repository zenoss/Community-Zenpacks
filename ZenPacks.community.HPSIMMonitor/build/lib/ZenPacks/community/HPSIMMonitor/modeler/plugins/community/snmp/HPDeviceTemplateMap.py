__doc__="""HPDeviceTemplateMap

HPDeviceTemplate maps the total CPU column in Systems Insight Manager

$Id: HPDeviceTemplate.py,v 1.00 2008/06/13 16:01 mikea Exp $"""

__version__ = '$Revision: 1.00 $'

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
#import transaction

class HPDeviceTemplateMap(SnmpPlugin):

    #maptype = 'DeviceMap'
    deviceProperties = SnmpPlugin.deviceProperties + ('zDeviceTemplates',)
    columns = {
            '.1': 'snmpindex',
            '.2': 'cpuName',
            '.4': 'cpuPercentProcessorTime'
    }

    devcolumns = {
        '.1.3.6.1.4.1.9600.1.1.5.1.5.6.95.84.111.116.97.108': 'cpuTime' 
    }

    snmpGetTableMaps = (
            GetTableMap('winos-cpu-table','.1.3.6.1.4.1.232.19.2.3.2.1', columns),
    )
    
    snmpGetMap = GetMap(devcolumns)

    def process(self, device, results, log):
        """collect snmp information from this device"""
        #log.info(dir(device))
        #log.info(str(self.deviceProperties))
        log.info('processing %s for device %s', self.name(), device.id)
        #templates = device.zDeviceTemplates
        getdata, tabledata = results
        cputable = tabledata.get('winos-cpu-table')
        CTemplates = getattr(device, 'zDeviceTemplates',None)
        #log.debug(str(device.zDeviceTemplates))
        #tom is the Temprary Object Map. This allows us to check if cpu information is provided by SNMP-Informant
        log.debug('---- Checking for SNMP-Informant data ----')
        tom = self.objectMap(getdata)
	#log.debug(tom.items())
        if 'cpuTime' not in tom.items():
            log.debug('==== No SNMP-Informant Mib data retrieved ====')
        else:
            log.debug('==== SNMP-Informant data retrieved ====')
            Template = 'Device'
        log.debug('---- Processing SIM CPU Table ----')
        Template = ''
        for ifindex, data in cputable.items():
            log.debug('Processor index %s is %s', data['snmpindex'], data['cpuName'])
            if data['cpuName'] == '_Total':
                if ifindex == '2':
                    Template = 'HPDevice1'
                elif ifindex == '3':
                    Template = 'HPDevice2'
                elif ifindex == '5':
                    Template = 'HPDevice4'
                else:
                    Template = 'Device'
        if Template == '':
            Template = 'Device'
        log.debug('Selected Template is: %s' % Template)
        log.debug('Current Device Templaces: %s' % str(device.zDeviceTemplates))
	newTemplates = []
	for each in device.zDeviceTemplates:
            if each in ['Device','HPDevice1','HPDevice2','HPDevice4']:
                  newTemplates.append(Template)
            else:
                  newTemplates.append(each)
	om = self.objectMap({'bindTemplates': newTemplates})
        return om

