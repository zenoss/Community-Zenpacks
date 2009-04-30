################################################################################
#
# This program is part of the Components Cleaner Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""ComponentsCleaner

Components Cleaner remove hardware components from Device

$Id: ComponentsCleaner.py,v 1.0 2009/04/24 16:30:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

class ComponentsCleaner(PythonPlugin):
    """Remove hardware components from device."""
    
    compname = "hw"

    def collect(self, device, log):
        return ('cards', 'cpus', 'fans', 'harddisks', 'powersupplies', 'temperaturesensors')

    def process(self, device, results, log):
        """remove hardware components from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
	maps = []
	for self.relname in results:
            rm = self.relMap()
	    maps.append(rm)
        return maps
