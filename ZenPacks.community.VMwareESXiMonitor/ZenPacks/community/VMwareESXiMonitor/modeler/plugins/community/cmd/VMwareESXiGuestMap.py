################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import Globals
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
import re, commands, os
from Products.DataCollector.plugins.DataMaps import ObjectMap

class VMwareESXiGuestMap(PythonPlugin):

	relname = "guestDevices"
	modname = 'ZenPacks.zenoss.ZenossVirtualHostMonitor.VirtualMachine'
	deviceProperties = PythonPlugin.deviceProperties + ('zCommandUsername','zCommandPassword')

	def collect(self, device, log):
		log.info('Getting VMware ESXi guest info for device %s' % device.id)
		cmd = os.path.abspath('%s/../../../../libexec/esxi_guestinfo.pl' % os.path.dirname(__file__))
		username = getattr(device, 'zCommandUsername', None)
		password = getattr(device, 'zCommandPassword', None)
		if (not username or not password):
			return None
		( stat, output) = commands.getstatusoutput( "/usr/bin/perl %s --server %s --username %s --password '%s'" % (cmd, device.id, username, password))
		if(stat != 0):
			return None
		else:
			results = output
			return results

	def process(self, device, results, log):
		log.info('Processing VMware ESXi guest info for device %s' % device.id)
		rm = self.relMap()
		rlines = results.split("\n")
		for line in rlines:
			if line.startswith("Warning:"):
				log.warning('%s' % line);
			elif re.search(';', line):
				name, memSize, os, powerStatus, status = line.split(';')
				info = {}
				info['adminStatus'] = powerStatus == "poweredOn"
				info['operStatus'] = status == "green"
				info['memory'] = int(memSize)
				info['osType'] = os
				info['displayName'] = name
				om = self.objectMap(info)
				om.id = self.prepId(name)
				rm.append(om)
		log.debug(rm)

		return [rm]
