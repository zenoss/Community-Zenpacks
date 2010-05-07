from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

CPUMULTIPLIER = {
    'MHz' : 1,
    'GHz' : 1000
}

L2MULTIPLIER = {
    'kB' : 1,
    'M' : 1024,
    'MB' : 1024,
    'Megabytes' : 1024,
}

class cpu(CommandPlugin):
    """
    find the cpu information
    """
    maptype = "CPUMap"
    command = 'system_profiler -detailLevel mini SPHardwareDataType'
    compname = 'hw'
    relname = "cpus"
    modname = "Products.ZenModel.CPU"

# Hardware:

#     Hardware Overview:

#       Model Name: MacBook Pro
#       Model Identifier: MacBookPro4,1
#       Processor Name: Intel Core 2 Duo
#       Processor Speed: 2.4 GHz
#       Number Of Processors: 1
#       Total Number Of Cores: 2
#       L2 Cache: 3 MB
#       Memory: 4 GB
#       Bus Speed: 800 MHz
#       Boot ROM Version: MBP41.00C1.B00
#       SMC Version (system): 1.27f2
#       Sudden Motion Sensor:
#           State: Enabled


    def process(self, device, results, log):
        """parse command output from this device"""
        log.info('processing processor resources %s' % device.id)
        rm = self.relMap()

        command_output = results.split('\n')
        om = self.objectMap()
        number = 0
        for line in command_output:
            if line: #check for blank lines
                key, value = line.split(':')
                key = key.strip()
                #       Processor Name: Intel Core 2 Duo
                if key == 'Processor Name':
                    om.description = value.strip()
                    manufacturer = om.description.split()[0]
                    om.setProductKey = MultiArgs(om.description,manufacturer)
                #       Processor Speed: 2.4 GHz
                if key == 'Processor Speed':
                    speed, unit = value.strip().split()
                    om.clockspeed = float(speed) * CPUMULTIPLIER.get(unit, 1)
                #       Bus Speed: 800 MHz
                if key == 'Bus Speed':
                    speed, unit = value.strip().split()
                    om.extspeed = float(speed) * CPUMULTIPLIER.get(unit, 1)
                #       Number Of Processors: 1
                if key == 'Number Of Processors':
                    number = int(value.strip())
                #       L2 Cache: 3 MB
                if key == 'L2 Cache':
                    cache, unit = value.strip().split()
                    om.cacheSizeL2 = int(cache) * L2MULTIPLIER.get(unit, 1)
                    
        #insert an objectMap for each CPU
        for n in range(number):
            om.id = str(n)
            om.socket = str(n)
            rm.append(om)
                
        log.debug(rm)
        return rm

