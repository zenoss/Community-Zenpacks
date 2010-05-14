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

__doc__="""SUNProcessMap

SUNProcessMap maps the process tables to interface objects

$Id: SUNProcessMap.py,v 1.2 2004/04/07 16:26:53 malbon Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class SUNProcessMap(SnmpPlugin):

    maptype = "OSProcessMap"
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"
    classname = 'createFromObjectMap'
    collector = 'zensunprocess'
    meta_type = 'OSProcess'

    columns = {
         '.1': 'snmpindex',
         '.10': 'procName',
         }

    snmpGetTableMaps = (
        GetTableMap('processTable', '.1.3.6.1.4.1.42.3.12.1.1', columns),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        
        #get the SNMP process data
        pstable = tabledata.get("processTable")
        
        log.debug("=== process information received ===")
        for p in pstable.keys():
            log.debug("snmpidx: %s\tprocess: %s" % (p, pstable[p]))
        
        rm = self.relMap()
        for proc in pstable.values():
           om = self.objectMap(proc)
	   om.collectors = ['zensunprocess']
	   om.parameters = ''
           om.meta_type = 'OSProcess'
           #ppath = getattr(om, '_procPath', False) 
           #if ppath and ppath.find('\\') == -1:
           #    om.procName = om._procPath
           if not getattr(om, 'procName', False): 
              	log.warn("Skipping process with no name")
              	continue
           #om.parameters = getattr(om, 'parameters', '')
           else:
                rm.append(om)
        return rm


