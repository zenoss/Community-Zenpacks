###############################################################################
#
# SerialPorts command parser plugin
#
###############################################################################

__doc__ = """ SerialPorts

SerialPorts maps Opengear the "config -g config" command to zenoss data

$id: $"""

__version__ = "$Revision: 1.5 $"[11:-2]

import os
import Globals
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class SerialPorts(CommandPlugin):

    command = "/bin/cat /var/run/serial-ports && /bin/config -g config.ports"
    relname = "SerialPrt"
    modname = 'ZenPacks.Opengear.ConsoleServer.SerialPort'

    def getLabel(self, port):
        return "Port %d" % (port,)

    def getSettings(self, speed, parity, charsize, stopbits):
        settings = []
        settings.append(str(speed))
        settings.append(str(charsize))
        if parity == "None":
            settings.append("N")
        elif parity == "Odd":
            settings.append("O")
        elif parity == "Even":
            settings.append("E")
        elif parity == "Mark":
            settings.append("M")
        elif parity == "Space":
            settings.append("S")

        settings.append(str(stopbits))
        return "-".join(settings)

    def getMode(self, mode, ssh, telnet, rfc2217, rawtcp):
        if mode == "portmanager":
            protocols = []
            if ssh:
                protocols.append("SSH")
            if telnet:
                protocols.append("Telnet")
            if rfc2217:
                protocols.append("RFC-2217")
            if rawtcp:
                protocols.append("Raw TCP")

            if len(protocols) > 0:
                return "Console (%s)" % (", ".join(protocols),)
            else:
                return "Console"
        elif mode == "console":
            return "Local Console"
        elif mode == "powerman":
            return "RPC"
        elif mode == "reserved":
            return "Environmental"

        return mode

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        log.debug('results: %s', str(results),)

        rm = self.relMap()
        lines = results.split(os.linesep)
        nports = 0
        config = {}
        for line in lines:

            if line.startswith("port"):
                nports += 1
                continue

            elif line.startswith("config.ports"):
                splitted = line.split()
                if len(splitted) > 1:
                    config[splitted[0]] = ' '.join(splitted[1:])

        log.debug("nports: %d", nports)
        for port in range(1, nports + 1):
            info = {}

            prefix = "config.ports.port%d" % (port,)
            info['serialPortNumber'] = port
            info['serialPortLabel'] = \
                config.get(prefix + ".label", self.getLabel(port))
            info['serialPortMode'] = \
                config.get(prefix + ".mode", "portmanager")
            info['serialPortLoglevel'] = config.get(prefix + ".loglevel", 0)
            info['serialPortSpeed'] = config.get(prefix + ".speed", 9600)
            info['serialPortParity'] = config.get(prefix + ".parity", "None")
            info['serialPortCharsize'] = config.get(prefix + ".charsize", 8)
            info['serialPortStop'] = config.get(prefix + ".stop", 1)
            info['serialPortFlowcontrol'] = \
                    config.get(prefix + ".flowcontrol", "None")
            info['serialPortProtocol'] = \
                    config.get(prefix + ".protocol", "RS232")
            info['serialPortSsh'] = (
                config.get(prefix + ".ssh", "off") == "on")
            info['serialPortTelnet'] = (
                config.get(prefix + ".telnet", "off") == "on")
            info['serialPortRfc2217'] = (
                config.get(prefix + ".rfc2217", "off") == "on")
            info['serialPortRawtcp'] = (
                config.get(prefix + ".rawtcp", "off") == "on")
            info['serialPortTerminal'] = \
                config.get(prefix + ".terminal", "vt220")
            info['serialPortSettingSummary'] = self.getSettings(
                info['serialPortSpeed'], info['serialPortParity'],
                info['serialPortCharsize'], info['serialPortStop'])
            info['serialPortModeSummary'] = self.getMode(
                info["serialPortMode"],
                info['serialPortSsh'], info['serialPortTelnet'],
                info['serialPortRfc2217'], info['serialPortRawtcp'])

            info['ogSerialPortStatusPort'] = port
            info['ogSerialPortStatusRxBytes'] = 0
            info['ogSerialPortStatusTxBytes'] = 0
            info['ogSerialPortStatusSpeed'] = info['serialPortSpeed']
            info['ogSerialPortStatusDCD'] = 0
            info['ogSerialPortStatusDTR'] = 0
            info['ogSerialPortStatusDSR'] = 0
            info['ogSerialPortStatusCTS'] = 0
            info['ogSerialPortStatusRTS'] = 0
            #info['dcd'] = False
            #info['dtr'] = False
            #info['dsr'] = False
            #info['cts'] = False
            #info['rts'] = False

            om = self.objectMap(info)
            om.snmpindex = port
            if port < 10:
                om.id = self.prepId("Port 0%d" % (port,))
            else:
                om.id = self.prepId("Port %d" % (port,))

            log.debug("Appending object: %s" % (om.__dict__,))
            rm.append(om)

        log.debug("Returning: %r %s" % (rm, rm,))
        return [rm]
