import json
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

L2MULTIPLIER = {
    'kB' : 1,
    'KB' : 1,
    'M' : 1024,
    'mB' : 1024,
    'MB' : 1024,
    'Megabytes' : 1024,
}

class cpu(CommandPlugin):
    """
    find the cpu information
    """
    maptype = "CPUMap"
    command = 'ohai cpu'
    compname = 'hw'
    relname = "cpus"
    modname = "Products.ZenModel.CPU"

    def process(self, device, results, log):
        """parse command output from this device"""
        log.info('Processing the ohai cpu info for device %s' % device.id)
        rm = self.relMap()
        om = self.objectMap()
        #results are JSON-formatted output
        #get a JSON parser and pull out values
        joutput = json.loads(results)
        joutput.sort()
        #"total"
        number = joutput[2][1]
        #"model_name"
        om.description = joutput[0][1]['model_name']
        #"vendor_id"
        manufacturer = joutput[0][1]['vendor_id']
        if manufacturer == 'GenuineIntel':
            manufacturer = 'Intel'
        om.setProductKey = MultiArgs(om.description,manufacturer)
        #"mhz"
        om.clockspeed = float(joutput[0][1]['mhz'])
        #"cache_size"
        cache_size = joutput[0][1]['cache_size']
        cache, unit = cache_size.split()
        om.cacheSizeL2 = int(cache) * L2MULTIPLIER.get(unit, 1)
                    
        #insert an objectMap for each CPU
        for n in range(number):
            om.id = str(n)
            om.socket = str(n)
            rm.append(om)
                
        log.debug(rm)
        return rm

