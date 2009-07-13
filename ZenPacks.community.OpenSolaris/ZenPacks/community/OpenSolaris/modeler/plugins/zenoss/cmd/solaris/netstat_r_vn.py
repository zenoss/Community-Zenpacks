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

TARGET=0
NETMASK=1
GATEWAY=2
INTERFACE=3
FLAGS=8

from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.SolarisCommandPlugin \
         import SolarisCommandPlugin

class netstat_r_vn(SolarisCommandPlugin):

    maptype = "RouteMap"
    command = '/usr/bin/netstat -r -vn'
    compname = "os"
    relname = "routes"
    modname = "Products.ZenModel.IpRouteEntry"
    deviceProperties = SolarisCommandPlugin.deviceProperties + (
        'zRouteMapCollectOnlyIndirect',
        )

#Kernel IP routing table
#Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
#192.168.31.0    0.0.0.0         255.255.255.0   U         0 0          0 eth1
#169.254.0.0     0.0.0.0         255.255.0.0     U         0 0          0 eth1
#0.0.0.0         192.168.31.2    0.0.0.0         UG        0 0          0 eth1


#IRE Table: IPv4
#  Destination             Mask           Gateway          Device Mxfrg Rtt   Ref Flg  Out  In/Fwd
#-------------------- --------------- -------------------- ------ ----- ----- --- --- ----- ------
#default              0.0.0.0         192.168.31.2         e1000g0  1500*    0   1 UG      47      0
#192.168.31.0         255.255.255.0   192.168.31.133       e1000g0  1500*    0   1 U      122      0
#127.0.0.1            255.255.255.255 127.0.0.1            lo0     8232*    0   1 UH      21      0

#IRE Table: IPv6
#  Destination/Mask            Gateway                    If    PMTU   Rtt  Ref Flags  Out   In/Fwd
#--------------------------- --------------------------- ----- ------ ----- --- ----- ------ ------
#fe80::/10                   fe80::20c:29ff:fe22:94aa    e1000g0  1500*     0   1 U          0      0
#::1                         ::1                         lo0    8252*     0   1 UH         0      0

    def process(self, device, results, log):
        log.info('Collecting routes for device %s' % device.id)
        indirectOnly = getattr(device, 'zRouteMapCollectOnlyIndirect', False)
        rm = self.relMap()
        rlines = results.split("\n")
        for line in rlines:
            aline = line.split()
            try:
                if aline[0] == 'default': aline[0] = '0.0.0.0'
            except:
                pass
            if len(aline) != 10 or not self.isip(aline[0]): continue
            route = self.objectMap()
            route.routemask = self.maskToBits(aline[NETMASK])
            if route.routemask == 32: continue

            if "G" in aline[FLAGS]:
                route.routetype = 'indirect'
            else:
                route.routetype = 'direct'
            if indirectOnly and route.routetype != 'indirect':
                continue

            if "D" in aline[FLAGS]: route.routeproto = "dynamic"
            else: route.routeproto = "local"

            route.id = aline[TARGET]
            route.setTarget = route.id + "/" + str(route.routemask)
            route.id = route.id + "_" + str(route.routemask)
            route.setInterfaceName = aline[INTERFACE]
            route.setNextHopIp = aline[GATEWAY]
            rm.append(route)
        return rm
