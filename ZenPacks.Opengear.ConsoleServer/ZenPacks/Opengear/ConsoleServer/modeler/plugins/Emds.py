###############################################################################
#
# Emds command parser plugin
#
###############################################################################

__doc__ = """ Emds

Emds maps Opengear the "config -g config" command to zenoss data

$id: $"""

__version__ = "$Revision: 1.4 $"[11:-2]

import os
import Globals
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class Emds(CommandPlugin):

    command = "/bin/config -g config.internals -g config.ports"
    relname = "EmdCfg"
    modname = 'ZenPacks.Opengear.ConsoleServer.Emd'

    INTERNAL_FORMAT = "config.internals.internal%d"
    SERIAL_FORMAT = "config.ports.port%d"
    MAX_DEVICES = 64

    def get_connected(self, i, format, prefix, config):
        if format == self.INTERNAL_FORMAT:
            return "Internal"
        elif format == self.SERIAL_FORMAT:
            return "Serial - Port #%d (%s)" % (
                i, config.get(prefix + ".label", "Port %d" % (i,)),)
        return "Unknown"

    def get_enabled(self, format, prefix, config):
        if format == self.SERIAL_FORMAT:
            return True

        return  (config.get(prefix + ".device.enabled", "off") == "on")

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        log.debug('results: %s', str(results),)

        rm = self.relMap()
        lines = results.split(os.linesep)
        config = {}
        for line in lines:

            splitted = line.split()
            if len(splitted) > 1:
                config[splitted[0]] = ' '.join(splitted[1:])

        total = 0
        for format in (self.INTERNAL_FORMAT, self.SERIAL_FORMAT,):
            for i in range(1, self.MAX_DEVICES):
                prefix = format % (i,)
                type = "%s.device.type" % (prefix,)
                if type not in config:
                    continue

                if config[type] != "enviro":
                    continue

                name = config.get(
                    prefix + ".enviro.name", config.get(
                        prefix + ".name", None))
                if name is None:
                    log.error("No EMD name provided")
                    continue

                info = {}
                total += 1
                info['emdName'] = name
                info['emdDescription'] = \
                    config.get(prefix + ".enviro.description",
                        config.get(prefix + ".description", ""))
                info['emdConnected'] = \
                        self.get_connected(i, format, prefix, config)
                info['emdLogStatus'] = (config.get(
                    prefix + ".enviro.log.enabled", "off") == "on")
                info['emdEnabled'] = self.get_enabled(format, prefix, config)

                log.debug("info: %s" % (str(info),))

                om = self.objectMap(info)
                om.snmpindex = total
                om.id = self.prepId(name)
                rm.append(om)

        log.debug("Found %d  EMDs" % (total,))

        return [rm]
