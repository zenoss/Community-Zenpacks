import Globals
from Products.DataCollector.plugins.CollectorPlugin \
	 import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps \
	 import ObjectMap

class BlueArcClusterNodeMap(SnmpPlugin):

	maptype = "BlueArcClusterNodesMap"
	relname = "nodes"
	modname = 'ZenPacks.DrD_Studios.BlueArc.ClusterNode'
	
	columns = {
		'.1': 'snmpindex',
		'.1': 'nodeID',
		'.2': 'nodeName',
		'.3': 'nodeIP',
		'.4': 'nodeStatus',
	}
	
	snmpGetTableMaps = (
		GetTableMap('node', '.1.3.6.1.4.1.11096.6.1.1.1.2.5.9.1', columns),
	)

	def process(self, device, results, log):
		""" collect snmp information from this cluster """
		
		# log that we are processing device
		log.info('processing %s for device %s', self.name(), device.id)
		log.info("Cluster Node results: %r", results)

		getdata, tabledata = results
		table = tabledata.get("node")
		rm = self.relMap()
		for info in table.values():
			#verify column exists
			#if not self.checkColumns(info, self.columns, log): continue
			
			om = self.objectMap(info)
			om.snmpindex  = om.nodeID
			om.id         = self.prepId(om.nodeName)
			om.nodeID     = om.nodeID
			om.nodeName   = om.nodeName
			om.nodeIP     = om.nodeIP
			om.nodeStatus = om.nodeStatus
			rm.append(om)
		return [rm]
