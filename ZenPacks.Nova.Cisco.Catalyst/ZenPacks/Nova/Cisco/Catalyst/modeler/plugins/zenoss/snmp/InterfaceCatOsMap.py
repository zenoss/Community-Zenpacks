###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__ = """InterfaceCatOsMap

    Extends the standard InterfaceMap to use 1.3.6.1.4.1.9.5.1.4.1.1.4
    (the CatOS interface description) as the interface's description 
    instead of the standard interface description.  Also uses ifName 
    instead of ifDescr.
"""

from copy import deepcopy
from Products.DataCollector.plugins.zenoss.snmp.InterfaceMap \
    import InterfaceMap
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap

class InterfaceCatOsMap(InterfaceMap):
    
    snmpGetTableMaps = InterfaceMap.baseSnmpGetTableMaps + (
        # Extended interface information.
        GetTableMap('ifalias', '.1.3.6.1.2.1.31.1.1.1',
                {'.1' : 'ifName',
                 '.6' : 'ifHCInOctets',
                 '.7' : 'ifHCInUcastPkts',
                 '.15': 'highSpeed'}
        ),
        GetTableMap('ifcatos', '.1.3.6.1.4.1.9.5.1.4.1.1',
                {'.11' : 'ifindex',
                 '.4'  : 'description'}
        ),
    )

    def process(self, device, results, log):
        """
        Pre-process the IF-MIB ifXTable to use the ifAlias as the interface's
        name instead of the ifDescr.  Also to use description from alternate OIDs.
        """

        if 'ifalias' in results[1] and 'iftable' in results[1]:
            for a_idx, alias in results[1]['ifalias'].items():
                for i_idx, iface in results[1]['iftable'].items():
                    if a_idx == i_idx:
                        results[1]['iftable'][i_idx]['id'] = alias['ifName']

        if 'ifcatos' in results[1] and 'iftable' in results[1]:
            for a_idx, catos in results[1]['ifcatos'].items():
                for i_idx, iface in results[1]['iftable'].items():
                    if catos['ifindex'] == iface['ifindex']:
                        results[1]['ifalias'][i_idx]['description'] = catos['description']
        
        return super(InterfaceCatOsMap, self).process(device, results, log)
