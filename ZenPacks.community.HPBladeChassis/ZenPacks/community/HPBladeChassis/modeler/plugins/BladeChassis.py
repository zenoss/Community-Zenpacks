# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
# Created By  :  Wouter D'Haeseleer
# Created On  :  05-11-2007
# Company     :  Imas NV
#
###########################################################################

import re

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class BladeChassis(CommandPlugin):
    """
    Run show enclosure info the OA to get details.
    """
    command = 'SHOW ENCLOSURE INFO'
    relname = "bladechassis"
    modname = 'ZenPacks.community.HPBladeChassis'

    def process(self, device, results, log):
        rm = self.relMap()
        log.info('Collecting Enclosure Information for device %s' % device.id)

        icCount = 0 # keep track of what we've seen for various reasons

        # create our object model
        om = self.objectMap()
        
        resultslines = results.split("\n")
        for line in resultslines:
            match = re.match('^([^:]+):.(.*)$', line.strip())
            if match:
                (key, value) = match.groups()

                if "Enclosure Name" in key:
                    om.bcEnclosureName = value

                if "Enclosure Type" in key:
                    om.bcEnclosureType = value

                if "Part Number" in key:
                    om.bcPartNumber = value

                if "Serial Number" in key:
                    om.bcSerialNumber = value

                if "UUID" in key:
                    om.bcUUID = value

                if "Asset Tag" in key:
                    om.bcAssetTag = value

                if "PDU Type" in key:
                    om.bcPduType = value

                # we get away with this because the more explicit match is above
                if "PDU Spare Part Number" in key:
                    om.bcPduSparePartNumber = value

        return om
