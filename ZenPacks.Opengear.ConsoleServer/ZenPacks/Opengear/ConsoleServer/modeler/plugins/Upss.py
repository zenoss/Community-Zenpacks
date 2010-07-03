###############################################################################
#
# Upss command parser plugin
#
###############################################################################

__doc__ = """ Upss

Upss maps Opengear the "config -g config" command to zenoss data

$id: $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import os
import Globals
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class Upss(CommandPlugin):

    command = "/bin/config -g config.ups"
    relname = "UpsCfg"
    modname = 'ZenPacks.Opengear.ConsoleServer.Ups'

    NETWORK_FORMAT = "config.ups.remotes.remote%d"
    SERIAL_FORMAT = "config.ups.monitors.monitor%d"
    MAX_DEVICES = 64

    def get_connected(self, i, format, prefix, config):
        if format == self.NETWORK_FORMAT:
            return "Network - %s (%s)" % (
                config.get(prefix + ".address"),
                config.get(prefix + ".name"),)
        elif format == self.SERIAL_FORMAT:
            return "Serial - %s (%s)" % (
                config.get(prefix + ".port", ""),
                config.get(prefix + ".name"),)
        return "Unknown"

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
        for format in (self.NETWORK_FORMAT, self.SERIAL_FORMAT,):
            for i in range(1, self.MAX_DEVICES):
                prefix = format % (i,)

                name = config.get(prefix + ".name")
                if name is None:
                    break

                info = {}
                total += 1
                info['upsName'] = name
                info['upsDescription'] = config.get(prefix + ".description", "")

                if format == self.SERIAL_FORMAT:
                    info['upsType'] = config.get(prefix + ".driver", "")
                elif format == self.NETWORK_FORMAT:
                    info['upsType'] = "Network Connected"
                    info['upsAddress'] = config.get(prefix + ".address", "")
                info['upsConnected'] = \
                        self.get_connected(i, format, prefix, config)
                info['upsLogStatus'] = (config.get(
                    prefix + ".log.enabled", "off") == "on")

                log.debug("info: %s" % (str(info),))

                om = self.objectMap(info)
                om.snmpindex = total
                om.id = self.prepId(name)
                rm.append(om)

        return [rm]
