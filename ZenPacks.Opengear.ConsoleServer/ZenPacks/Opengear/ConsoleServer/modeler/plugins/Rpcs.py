###############################################################################
#
# Rpcs command parser plugin
#
###############################################################################

__doc__ = """ Rpcs

Rpcs maps Opengear the "config -g config" command to zenoss data

$id: $"""

__version__ = "$Revision: 1.4 $"[11:-2]

import os
import Globals
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class Rpcs(CommandPlugin):

    command = "/bin/config -g config.sdt.hosts -g config.ports"
    relname = "RpcCfg"
    modname = 'ZenPacks.Opengear.ConsoleServer.Rpc'

    NETWORK_FORMAT = "config.sdt.hosts.host%d"
    SERIAL_FORMAT = "config.ports.port%d"
    MAX_DEVICES = 64

    def get_connected(self, i, format, prefix, config):
        if format == self.NETWORK_FORMAT:
            return "Network - %s (%s)" % (
                config.get(prefix + ".address"),
                config.get(prefix + ".name"),)
        elif format == self.SERIAL_FORMAT:
            return "Serial - Port #%d (%s)" % (
                i, config.get(prefix + ".label", "Port %d" % (i,)),)
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
        for format in (self.SERIAL_FORMAT, self.NETWORK_FORMAT,):
            for i in range(1, self.MAX_DEVICES):
                prefix = format % (i,)
                type = "%s.device.type" % (prefix,)
                if type not in config:
                    continue

                if config[type] != "rpc":
                    continue

                name = \
                    config.get(prefix + ".power.name",
                        config.get(prefix + ".name", None))
                if name is None:
                    log.warn("No name found for RPC: %d, skipping" % (
                        total + 1,))
                    continue

                info = {}
                total += 1
                info['rpcName'] = name
                info['rpcDescription'] = config.get(
                    prefix + ".power.description",
                    config.get(prefix + ".description", ""))
                info['rpcType'] = config.get(prefix + ".power.type", "Unknown")
                info['rpcConnected'] = self.get_connected(
                    i, format, prefix, config)
                info['rpcLogStatus'] = (config.get(
                    prefix + ".power.log.enabled", "off") == "on")

                log.debug("info: %s" % (str(info),))

                om = self.objectMap(info)
                om.snmpindex = total
                om.id = self.prepId(name)
                rm.append(om)

                log.debug("Found RPC: %d: %s" % (total, str(name),))

        log.debug("Found %d  RPCs" % (total,))

        return [rm]
