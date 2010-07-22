################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """RouteMap

RouteMap gathers and stores routing information.

$Id: RouterMap.py,v 1.1 2010/07/23 00:08:37 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin

class RouteMap(WMIPlugin):

    maptype = "RouteMap"
    relname = "routes"
    compname = "os"
    modname = "Products.ZenModel.IpRouteEntry"
    deviceProperties = \
                WMIPlugin.deviceProperties + ('zRouteMapCollectOnlyLocal',
                                               'zRouteMapCollectOnlyIndirect',
                                               'zRouteMapMaxRoutes')


    tables = {
            "Win32_IP4RouteTable":
                (
                "Win32_IP4RouteTable",
                None,
                "root/cimv2",
                    {
                    '__path':'snmpindex',
                    'Destination':'id',
                    'Mask':'routemask',
                    'Metric1':'metric1',
                    'InterfaceIndex':'setInterfaceIndex',
                    'NextHop':'setNextHopIp',
                    'Protocol':'routeproto',
                    'Type':'routetype',
                    }
                ),
            }


    def process(self, device, results, log):
        """collect WMI information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        routetable = results.get("Win32_IP4RouteTable", None)
        if not routetable: return
        localOnly = getattr(device, 'zRouteMapCollectOnlyLocal', False)
        indirectOnly = getattr(device, 'zRouteMapCollectOnlyIndirect', False)
        maxRoutes = getattr(device, 'zRouteMapMaxRoutes', 500)
        rm = self.relMap()
        for route in routetable:
            om = self.objectMap(route)
            if not hasattr(om, "id"): continue
            if not hasattr(om, "routemask"): continue
            om.routemask = self.maskToBits(om.routemask)

            # Workaround for existing but invalid netmasks
            if om.routemask is None: continue

            om.setTarget = om.id + "/" + str(om.routemask)
            om.id = om.id + "_" + str(om.routemask)
            if om.routemask == 32: continue
            routeproto = getattr(om, 'routeproto', 'other')
            om.routeproto = self.mapSnmpVal(routeproto, self.routeProtoMap)
            if localOnly and om.routeproto != 'local':
                continue
            if not hasattr(om, 'routetype'): 
                continue    
            om.routetype = self.mapSnmpVal(om.routetype, self.routeTypeMap)
            if indirectOnly and om.routetype != 'indirect':
                continue
            if len(rm.maps) > maxRoutes:
                log.error("Maximum number of routes (%d) exceeded", maxRoutes)
                return 
            rm.append(om)
        return rm


    def mapSnmpVal(self, value, map):
        if len(map)+1 >= value:
            value = map[value-1]
        return value


    routeTypeMap = ('other', 'invalid', 'direct', 'indirect')
    routeProtoMap = ('other', 'local', 'netmgmt', 'icmp',
            'egp', 'ggp', 'hello', 'rip', 'is-is', 'es-is',
            'ciscoIgrp', 'bbnSpfIgrp', 'ospf', 'bgp')
