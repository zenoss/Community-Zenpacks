import Globals
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class SentryCDUSensorMap(SnmpPlugin):

    relname = "sentrysensors"
    modname = 'ZenPacks.chudler.SentryCDU.SentrySensor'
    
    sensors = {
         '.2': 'id',
         '.3': 'sysName',
         '.4': 'tempProbeStatus', # 6 = lost, 0 = normal
         '.9': 'humProbeStatus', # 6 = lost, 0 = normal
         '.13': 'scale', # 1 = fahr, 2 = celsius
         }

    vendors = { 'sentry': '1718.3',
                'rittal': '2606.100.1'
              }

    snmpGetTableMaps = []
    for vendor, oid in vendors.items():
        sensorName = vendor + 'sensors'
        sensorOid = '.1.3.6.1.4.1.' + oid + '.2.5.1'
        sensorMap = GetTableMap(sensorName, sensorOid, sensors)
        snmpGetTableMaps.append(sensorMap)

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	rm = self.relMap()
	for vendor, oid in self.vendors.items():
        	sensors = tabledata.get(vendor + 'sensors')
		for idx, sensorInfo in sensors.items():
            		if sensorInfo['tempProbeStatus'] != 0 or sensorInfo['humProbeStatus'] != 0:
                		# if either sensor is not in "normal" mode, do not store it in the DB
                		continue
            		log.info('Found a Environmental Sensor on this CDU named %s', sensorInfo['sysName'])
            		sensorInfo['snmpindex'] = str(idx)
            		sensorInfo['tempOid'] = '.1.3.6.1.4.1.' + oid + '.2.5.1.6.' + str(idx)
            		sensorInfo['humidityOid'] = '.1.3.6.1.4.1.' + oid + '.2.5.1.10.' + str(idx)
            		om = self.objectMap(sensorInfo)
            		rm.append(om)
        return [rm]
