import Globals
from Products.DataCollector.plugins.CollectorPlugin \
	 import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps \
	 import ObjectMap

class VirtualMachines(SnmpPlugin):

	maptype = "vmwareVirtualMachinesMap"
	relname = "virtualmachines"
	modname = 'ZenPacks.vmware.VirtualMachines.VirtualMachine'
	
	columns = {
		'.7': 'snmpindex',
		'.2': 'vmDisplayName',
		'.4': 'vmGuestOS',
		'.6': 'vmState',
		'.7': 'vmVMID',
		'.8': 'vmGuestState',
	}
	
	snmpGetTableMaps = (
		GetTableMap('vminfo', '.1.3.6.1.4.1.6876.2.1.1', columns),
	)

	def process(self, device, results, log):
		"""collect snmp information from this esx server"""
		
		# log that we are processing device
		log.info('processing %s for device %s', self.name(), device.id)
		log.info("VirtualMachine results: %r", results)
		getdata, tabledata = results
		table = tabledata.get("vminfo")
		rm = self.relMap()
		for info in table.values():
			#verify column exists
			#if not self.checkColumns(info, self.columns, log): continue
			
			# create the object map which puts our snmp stat into
			# the VirtualMachine object
			om = self.objectMap(info)
			om.id = self.prepId(om.vmDisplayName)
			om.snmpindex = om.vmVMID
			rm.append(om)
		return [rm]
