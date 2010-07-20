import json
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
    command = 'ohai memory'
    compname = 'hw'
    relname = "filesystems"
    modname = "Products.ZenModel.Filesystem"

    def process(self, device, results, log):
        log.info('Processing the ohai memory info for device %s' % device.id)
        maps = []

        #results are JSON-formatted output
        #get a JSON parser and pull out values
        joutput = json.loads(results)
        joutput.sort()

        total_value = joutput[21][1][:-2]
        total_units = joutput[21][1][-2:]
        total_size = int(total_value) * MULTIPLIER.get(total_units, 1)
        maps.append(ObjectMap({"totalMemory": total_size}, compname="hw"))

        swap_value = joutput[20][1]['total'][:-2]
        swap_units = joutput[20][1]['total'][-2:]
        swap_size = int(swap_value) * MULTIPLIER.get(swap_units, 1)
        maps.append(ObjectMap({"totalSwap": swap_size}, compname="os"))

        log.debug(maps)
        return maps

