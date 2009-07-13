###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.SolarisCommandPlugin \
     import SolarisCommandPlugin
import re

class netstat_an(SolarisCommandPlugin):
    """
    Collect running ip services using netstat -an on a solaris box.
    """
    maptype = "IpServiceMap"
    command = "/usr/bin/netstat -an"
    compname = "os"
    relname = "ipservices"
    modname = "Products.ZenModel.IpService"

    PROTO = {
            'UDP_IPv4' : 'udp4',
            'UDP_IPv6' : 'udp6',
            'TCP_IPv4' : 'tcp',
            'TCP_IPv6' : 'tcp6'
             }

    def process(self, device, results, log):
        log.info('Collecting Ip Services for device %s' % device.id)
        rm = self.relMap()
        data = results.split("SCTP:")[0]
        subdata = data.split("\n\n")
        protocol_regex = re.compile("\n?(\w*)\:\s(.*)\n")
        ip_port_regex = re.compile("(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3})\.(\d+)")
        ipv6_regex = re.compile(":.*\.(\d+)")
        services = {}
        for i in subdata:
            p=protocol_regex.search(i)
            if p:
                proto=self.PROTO.get("%s_%s" % (p.group(1),p.group(2)))

            # Strip the header information off
            try:
                # Strip the header information off
                substr=i.split('-\n')[1]
                for j in substr.split('\n'):
                    # normalize on address 0.0.0.0 means all addresses
                    addr = port = ""
                    line=j.split()
                    ip_port=ip_port_regex.search(line[0])
                    ipv6_port=ipv6_regex.search(line[0])
                    if line[0]=='*.*': continue
                    addr_port=line[0].split('.')
                    if addr_port[0] == '*':
                        addr = "0.0.0.0"
                        port = addr_port[-1]
                    elif ip_port:
                        addr = ip_port.group(1)
                        port = ip_port.group(2)
                    elif ipv6_port:
                        addr = ipv6_port.group(1)
                        port = ipv6_port.group(2)
                    if addr == "0.0.0.0" or not services.has_key(port):
                        services[port] = (addr, proto)
            except:
                # Ignore errors
                pass

        ports = {}
        for port, value in services.items():
            addr, proto = value
            om = ports.get((proto, port), None)
            if om:
                om.ipaddresses.append(addr)
            else:
                om = self.objectMap()
                om.protocol = proto
                om.port = int(port)
                om.id = '%s_%05d' % (om.protocol,om.port)
                om.setServiceClass = {'protocol': proto, 'port':om.port}
                om.ipaddresses = [addr,]
                om.discoveryAgent = self.name()
                ports[(proto, port)] = om
                rm.append(om)
        return rm
