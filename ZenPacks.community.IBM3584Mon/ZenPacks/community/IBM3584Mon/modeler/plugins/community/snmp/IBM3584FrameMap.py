################################################################################
#
# This program is part of the IBM3584Mon Zenpack for Zenoss.
# Copyright (C) 2009 Josh Baird.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

""" IBM3584FrameMap models the 3584s frames from the SML MIB """

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBM3584FrameMap(SnmpPlugin):
    """Map IBM frame table to model."""

    maptype = "IBM3584FrameMap"
    modname = "ZenPacks.community.IBM3584Mon.IBM3584Frame"
    relname = "frames"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('frameDeviceTable',
                    '.1.3.6.1.4.1.14851.3.1.4.10.1',
                    {
                        '.2': '_vendor',
		        '.3': 'model',
                        '.4': 'serial',
                        '.10': 'status', 
                        '.11': 'frametype',
                    }
        ),
    )

    typemap = {0: 'Unknown',
               17: 'Main System Chassis',
               18: 'Expansion Chassis',
               19: 'Sub Chassis',
               32769: 'Service Bay',
               }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        frametable = tabledata.get('frameDeviceTable')
	for oid, frame in frametable.iteritems():
	    try:
                om = self.objectMap(frame)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId('Frame %s' % om.snmpindex)
                om.model = '%s %s'%(getattr(om, '_vendor', 'Unknown'),
                                    getattr(om, 'model', 'Unknown'))
                om.serial = getattr(om, 'serial', 'Unknown')
                om.frametype = self.typemap.get(getattr(om, 'frametype', 1), "Unknown")

                # Make sure we set the product key
                om.setProductKey = om.model

            except AttributeError:
                continue
            rm.append(om)
        return rm





