################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPFcaCntlrMap

HPFcaCntlrMap maps the cpqFcaCntlrTable table to cpqFcaCntlr objects

$Id: HPFcaCntlrMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPExpansionCardMap import HPExpansionCardMap

class HPFcaCntlrMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqFcaCntlrTable table to model."""

    maptype = "cpqFcaCntlr"
    modname = "ZenPacks.community.HPMon.cpqFcaCntlr"

    snmpGetTableMaps = (
        GetTableMap('cpqFcaCntlrTable',
	            '.1.3.6.1.4.1.232.16.2.2.1.1',
		    {
		        '.1': 'chassis',
			'.2': 'snmpindex',
			'.3': 'model',
			'.4': 'FWRev',
			'.5': 'status',
			'.8': 'wwpn',
			'.9': 'serialNumber',
			'.10': 'role',
			'.11': 'redundancyType',
			'.14': 'wwnn',
		    }
	),
        GetTableMap('cpqSsChassisTable',
	            '.1.3.6.1.4.1.232.8.2.2.1.1',
		    {
			'.1': 'snmpindex',
			'.4': 'name',
		    }
	),
    )

    models = {1: 'Unknown Fibre Channel Array Controller',
	    2: 'Compaq StorageWorks RAID Array 4000/4100 Controller',
	    3: 'Compaq StorageWorks Modular Smart Array 1000 Controller',
	    4: 'HP StorageWorks Modular Smart Array 500 Controller',
	    5: 'Compaq StorageWorks Enterprise/Modular RAID Array Controller',
	    6: 'Compaq StorageWorks Enterprise Virtual Array Controller',
	    7: 'HP StorageWorks Modular Smart Array 500 G2 Controller',
	    8: 'HP StorageWorks Modular Smart Array 20 Controller',
	    9: 'HP StorageWorks Modular Smart Array 1500 CS Controller',
	    10: 'HP StorageWorks Modular Smart Array 1510i Controller',
	    11: 'HP StorageWorks Modular Smart Array 2060s Controller',
	    12: 'HP StorageWorks Modular Smart Array 2070s Controller',
	    }

    redundancyTypes =  {1: 'other',
		        2: 'Not Redundancy',
		        3: 'Active-Standby',
		        4: 'Primary-Secondary',
		        5: 'Active-Active',
		        }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	cardtable = tabledata.get('cpqFcaCntlrTable')
        chassismap = {}
	chassistable = tabledata.get('cpqSsChassisTable')
	for chassis in chassistable.values():
	    chassismap[chassis['snmpindex']] = chassis['name']
	external = 'community.snmp.HPSsChassisMap' in getattr(device, 'zCollectorPlugins', [])
	if not device.id in HPExpansionCardMap.oms:
	    HPExpansionCardMap.oms[device.id] = []
        for card in cardtable.values():
            try:
                om = self.objectMap(card)
		om.snmpindex = "%d.%d" % (om.chassis, om.snmpindex)
                om.id = self.prepId("cpqFcaCntlr%s" % om.snmpindex.replace('.', '_'))
                om.slot = getattr(om, 'slot', 0)
		om.model = self.models.get(getattr(om, 'model', 1), '%s (%d)' %(self.models[1], om.model))
                om.setProductKey = "%s" % om.model
		om.redundancyType = self.redundancyTypes.get(getattr(om, 'redundancyType', 1), om.redundancyType)
		om.chassis = chassismap.get(om.chassis, '')
		om.external = external
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
	return

