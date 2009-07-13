from Products.DataCollector.plugins.DataMaps import ObjectMap
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.SolarisCommandPlugin \
                import SolarisCommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

import re

MULTIPLIER = {
    'MHz' : 1,
    'GHz' : 1000
}

VENDOR = {
    'GenuineIntel': 'Intel',
    'AMD': 'Amd'
}

class cpu(SolarisCommandPlugin):
    """
    find the memory and swap fields
    """
    maptype = "CPUMap"
    command = '/usr/sbin/psrinfo -pv'
    compname = 'hw'
    relname = "cpus"
    modname = "Products.ZenModel.CPU"

#The physical processor has 1 virtual processor (0)
#  x86 (GenuineIntel 10676 family 6 model 23 step 6 clock 2393 MHz)
#        Intel(r) Core(tm)2 Duo CPU     P8600  @ 2.40GHz
#The physical processor has 1 virtual processor (1)
#  x86 (GenuineIntel 10676 family 6 model 23 step 6 clock 2393 MHz)
#        Intel(r) Core(tm)2 Duo CPU     P8600  @ 2.40GHz

    idregex=re.compile(r'processor \((.*)\)\n')
    Manufacturer_regex=re.compile(r'.*\n\s+\w+ \((\w+)\s')
    clockspeed_regex=re.compile(r'.*clock (\d+)\s(\w+).*\n')
    description_regex=re.compile(r'.*\n.*\n\s+(.*)\n')

    def process(self, device, results, log):
        """parse command output from this device"""
        log.info('processing processor resources %s' % device.id)
        rm = self.relMap()

        config = {}
        for row in results.split('The'):
            id = self.idregex.search(row)
            if id:
                id=id.group(1)
            manufacturer = self.Manufacturer_regex.search(row)
            if manufacturer:
                manufacturer=VENDOR.get(manufacturer.group(1), manufacturer.group(1))

            description = self.description_regex.search(row)
            if description:
                description=description.group(1)

            clockspeed = self.clockspeed_regex.search(row)
            if clockspeed:
                clockspeed = int(clockspeed.group(1)) * MULTIPLIER.get(clockspeed.group(1), 1)


            #name = name.strip()
            #value = value.strip()

            #if name == 'hw.cpufrequency': config['clockspeed'] = int(value)
            #if name == 'hw.l1icachesize': config['cacheSizeL1'] = int(value) / 1024
            #if name == 'hw.l2cachesize': config['cacheSizeL2'] = int(value) / 1024
            #if name == 'machdep.cpu.brand_string': config['description'] = value

            om = self.objectMap()
            om.description = description
            om.setProductKey = MultiArgs(description,manufacturer)
            om.id = id
            om.socket = id
            om.clockspeed=clockspeed
            if id != None: rm.append(om)
        log.debug(rm)
        return rm

