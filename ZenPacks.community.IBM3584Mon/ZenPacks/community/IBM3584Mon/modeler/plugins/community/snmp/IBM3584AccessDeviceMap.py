################################################################################
#
# This program is part of the IBM3584Mon Zenpack for Zenoss.
# Copyright (C) 2009 Josh Baird.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

""" IBM3584AccessDeviceMap  models the 3584s library from the SML MIB """

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class IBM3584AccessDeviceMap(SnmpPlugin):
    """Map IBM Tape Drives table to model."""

    maptype = "IBM3584AccessDeviceMap"
    modname = "ZenPacks.community.IBM3584Mon.IBM3584AccessDevice"
    relname = "accessdevices"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('accessDeviceTable',
                    '1.3.6.1.4.1.2.6.182.3.6.2.1',
                    {
		        '.2': 'devicetype',
                        '.3': 'model',
                        '.5': 'status',
                        '.6': 'needsCleaning',
                    }
        ),
        GetTableMap('accessFirmwareDeviceTable',
                    '1.3.6.1.4.1.2.6.182.3.9.2.1',
                    {
                        '.3': 'firmware',
                    }
        ),

    )


    devicetypemap = {0: 'Unknown',
		     1: 'Worm Drive',
                     2: 'Magneto Optical Drive',
                     3: 'Tape Drive',
                     4: 'DVD Drive',
                     5: 'CDROM Drive',
                     }


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        accessdevicetable = tabledata.get('accessDeviceTable')
        accessfwdevicetable = tabledata.get('accessFirmwareDeviceTable')

        # This dictionary will index the accessFirmwareDeviceTable SNMP map with the snmpindexid of
        # the accessDeviceTable.  Example of how you can correlate values from multiple GetTableMaps
        firmwares = dict([(oid.strip('.'), value['firmware']) for oid, value in accessfwdevicetable.iteritems()])
        #firmwares = dict([(oid.strip('.'), value) for oid, value in accessfwdevicetable.iteritems()])

	# Sanity check (SNMP response)
	if not accessdevicetable:
		log.warn('No SNMP response from %s for the %s plugin', device.id, self.name() )
        	log.warn( "Data= %s", getdata )
                return

        for oid, accessdevice in accessdevicetable.iteritems():
            try:
                om = self.objectMap(accessdevice)

	        # Set devicetype / availability per map
	        om.snmpindex = oid.strip('.')
	        om.id = self.prepId('Access Device %s' % om.snmpindex)
                om.devicetype = self.devicetypemap.get(getattr(om, 'devicetype', 1), "Unknown")
		om.needsCleaning = getattr(om, 'needsCleaning', '  ')
                #log.info('Debug: Need Cleaning: %s', om.needsCleaning)
                
                # Get firmware from the dictionary defined above
                om.firmware = firmwares.get(om.snmpindex)
                #log.info('Debug: Firmware: %s', firmware)
                   
		# Split makemodelserial into three tokens (make, model, serial)	
		# Example: IBM     ULT3580-TD2     9110813989
                make, om.model, om.serial = getattr(om, 'model', '   ').split()
                if make:
                    om.model = '%s %s' % (make, om.model)

            except AttributeError:
                continue
            rm.append(om)
        return rm




