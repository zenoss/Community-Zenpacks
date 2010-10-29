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
import commands, re, os
from Products.DataCollector.plugins.DataMaps import ObjectMap

class VMwareESXiHostMap(PythonPlugin):

	maptype = "DeviceMap"
	compname = ""
	deviceProperties = PythonPlugin.deviceProperties + ('zCommandUsername','zCommandPassword')

	def collect(self, device, log):
		log.info('Getting VMware ESXi host info for device %s' % device.id)
		cmd = os.path.abspath('%s/../../../../libexec/esxi_hostinfo.pl' % os.path.dirname(__file__))
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
		log.info('Processing VMware ESXi host info for device %s' % device.id)
		
		rlines = results.split("\n")
		for line in rlines:
			if line.startswith("Warning:"):
				log.warning('%s' % line)
			elif re.search(';', line):
				osVendor, osProduct, hwVendor, hwProduct = line.split(';')
				om = self.objectMap()
				om.setOSProductKey = osProduct
				om.setHWProductKey = hwProduct

		return om
