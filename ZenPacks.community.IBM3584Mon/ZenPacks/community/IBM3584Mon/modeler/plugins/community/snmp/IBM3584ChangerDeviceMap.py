################################################################################
#
# This program is part of the IBM3584Mon Zenpack for Zenoss.
# Copyright (C) 2009 Josh Baird.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

""" IBM3584ChangerDeviceMap models the 3584s frames from the SML MIB """

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBM3584ChangerDeviceMap(SnmpPlugin):
    """Map IBM ChangerDevice table to model."""

    maptype = "IBM3584ChangerDeviceMap"
    modname = "ZenPacks.community.IBM3584Mon.IBM3584ChangerDevice"
    relname = "changerdevices"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('changerDeviceTable',
                    '.1.3.6.1.4.1.14851.3.1.11.2.1',
                    {
                        '.2': 'deviceid',
		        '.3': 'mediaflipping', # 1 = true, 2 = false
                        '.5': 'name',
                        '.6': 'description', 
                        '.9': 'status',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        #log.info('results %s', results)
        getdata, tabledata = results
        rm = self.relMap()
        cdtable = tabledata.get('changerDeviceTable')
	for oid, frame in cdtable.iteritems():
	    try:
                om = self.objectMap(frame)
                om.snmpindex = oid.strip('.')
                #om.id = self.prepId('changer%s'%om.snmpindex)
                om.id = self.prepId("%s" % (om.name))
                om.name = "%s" % (getattr(om, 'name', 'Unknown'))
            except AttributeError:
                continue
            rm.append(om)
        return rm





