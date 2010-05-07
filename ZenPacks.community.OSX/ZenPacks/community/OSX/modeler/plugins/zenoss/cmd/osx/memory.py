#This finds the memory for the OS X box.  Swap is dynamically created with OS X,
#so finding the allocated swap isn't very useful

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

MULTIPLIER = {
    'kB' : 1024,
    'MB' : 1024 * 1024,
    'M' : 1024 * 1024,
    'Megabytes' : 1024 * 1024,
    'GB' : 1024 * 1024 * 1024,
    'G' : 1024 * 1024 * 1024,
    'Gigabytes' : 1024 * 1024 * 1024,
    'b' : 1
}

class memory(CommandPlugin):
    """
    find the memory
    """
    maptype = "FileSystemMap"
    command = 'system_profiler -detailLevel mini SPHardwareDataType | grep Memory'
    compname = 'hw'
    relname = "filesystems"
    modname = "Products.ZenModel.Filesystem"


    def process(self, device, results, log):
        log.info('Collecting memory for device %s' % device.id)
        maps = []

        # Process Memory line
        memory=results.split(":")[1].strip()
        mem_value, unit= memory.split()
        mem_size = int(mem_value) * MULTIPLIER.get(unit, 1)

        maps.append(ObjectMap({"totalMemory": mem_size}, compname="hw"))
        log.debug(maps)
        return maps

