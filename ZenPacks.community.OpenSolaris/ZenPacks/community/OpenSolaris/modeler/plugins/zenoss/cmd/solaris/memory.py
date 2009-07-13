from Products.DataCollector.plugins.CollectorPlugin import LinuxCommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.SolarisCommandPlugin \
                import SolarisCommandPlugin

MULTIPLIER = {
    'kB' : 1024,
    'MB' : 1024 * 1024,
    'M' : 1024 * 1024,
    'Megabytes' : 1024 * 1024,
    'b' : 1
}


class memory(SolarisCommandPlugin):
    """
    find the memory and swap fields
    """
    maptype = "FileSystemMap"
    command = '/usr/sbin/prtconf|grep Memory && /usr/sbin/swap -l|tail -1'
    compname = 'hw'
    relname = "filesystems"
    modname = "Products.ZenModel.Filesystem"


    def process(self, device, results, log):
        log.info('Collecting memory and swap for device %s' % device.id)

        maps = []
        memory_line=""
        swap_lines=[]
        lines=results.split("\n")
        memory_line=lines[0]
        swap_lines=results.split("\n")[1:]

        # Process Memory line
        memory=memory_line.split(':')[1]
        mem_value, unit= memory.split()
        mem_size = int(mem_value) * MULTIPLIER.get(unit, 1)

        swap_size=0
        # Process Swap Spaces
        for line in swap_lines:
            vals = line.split()
            if len(vals) != 5:
                continue

            swapfile, dev, swaplo, blocks, free = vals
            swap_size += (int(blocks) / 2)

        maps.append(ObjectMap({"totalMemory": mem_size}, compname="hw"))
        maps.append(ObjectMap({"totalSwap": swap_size}, compname="os"))
        return maps

