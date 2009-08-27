################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPDeviceMap

HPDeviceMap map mib elements from HP/Compaq Insight Manager mib to get hw and os
products.

$Id: HPDeviceMap.py,v 1.0 2009/07/06 09:26:53 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
import re

class HPDeviceMap(SnmpPlugin):
    """Map mib elements from HP/Compaq Insight Manager mib to get hw and os
    products.
    """

    maptype = "HPDeviceMap"

    snmpGetMap = GetMap({
        '.1.3.6.1.4.1.232.2.2.2.1.0' : 'setHWSerialNumber',
        '.1.3.6.1.4.1.232.2.2.4.2.0' : 'setHWProductKey',
        '.1.3.6.1.4.1.232.11.2.2.1.0' : 'setOSProductKey',
        '.1.3.6.1.4.1.232.11.2.2.2.0' : '_OSVer',
        })


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        if getdata['setHWProductKey'] is None: return None
	om = self.objectMap(getdata)
        if om.setOSProductKey and om.setOSProductKey.find("NetWare") > -1:
	    om.setOSProductKey = "Novell %s %s" %(om.setOSProductKey, om._OSVer)
            manuf = "Novell"
        elif re.search(r'Microsoft', om.setOSProductKey, re.I):
            manuf = "Microsoft"
        elif re.search(r'Red\s*Hat', om.setOSProductKey, re.I):
            manuf = "Red Hat"
        elif re.search(r'VMware', om.setOSProductKey, re.I):
	    om.setOSProductKey = om.setOSProductKey.split('-', 1)[1].strip()
	    om.setOSProductKey = "%s %s" %(om.setOSProductKey, om._OSVer)
            manuf = "VMware"
        elif re.search(r'SuSE', om.setOSProductKey, re.I):
	    om.setOSProductKey = om.setOSProductKey.split('-', 1)[1].strip()
	    om.setOSProductKey = "Novell %s %s" %(om.setOSProductKey, om._OSVer)
            manuf = "Novell"
	try:
            from Products.DataCollector.plugins.DataMaps import MultiArgs
            om.setHWProductKey = MultiArgs(om.setHWProductKey, "HP")
            om.setOSProductKey = MultiArgs(om.setOSProductKey, manuf)
	except:
	    pass
        return om

