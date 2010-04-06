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

class BladeChassisInterconnects(CommandPlugin):
    """
    Run show interconnect info all on the OA to get details.
    """
    command = 'SHOW INTERCONNECT INFO ALL'
    relname = "bladechassisinterconnects"
    modname = 'ZenPacks.community.HPBladeChassis.BladeChassisInterconnect'

    def process(self, device, results, log):
        rm = self.relMap()
        log.info('Collecting Interconnect Information for device %s' % device.id)

        icCount = 0 # keep track of what we've seen for various reasons


        resultslines = results.split("\n")
        for line in resultslines:
            match = re.match('^([0-9]+)\..(.*)$', line.strip())
            if match:
                # First line of a ic detail section, create object and get started
                # If this isn't the first ic, we want to save the last one
                try:
                    if om.id:
                        log.debug("Writing an interconnect %d" % icCount)
                        rm.append(om)
                except:
                    log.debug("Missing this one out since the last interconnect was invalid")
                        
                # Now create the new object and initalise it some
                # We set the snmpindex so that the collector is happy

                # Look here for empty interconenct bays
                if "<absent>" in match.groups()[1]:
                    om = None
                    continue
                om = self.objectMap()
                om.bciNumber = int(match.groups()[0])
                om.bciType = match.groups()[1]
                om.snmpindex = om.bciNumber
                om.id = self.prepId(om.bciNumber)
                icCount = icCount + 1
                log.debug("Found an interconnect, processing...")
                continue

            # Now look for the information we want, etc

            match = re.match('^Product.Name:.(.*)$',line.strip())
            if match:
                om.bciProductName = match.groups()[0]
                continue
            match = re.match('^In\-Band.IPv4.Address:.(.*)$',line.strip())
            if match:
                om.bciMgmtIp = match.groups()[0]
                continue
            match = re.match('^Part.Number:.(.*)$',line.strip())
            if match:
                om.bciPartNumber = match.groups()[0]
                continue
            match = re.match('^Spare.Part.Number:.(.*)$',line.strip())
            if match:
                om.bciSparePartNumber = match.groups()[0]
                continue
            match = re.match('^Serial.Number:.(.*)$',line.strip())
            if match:
                om.bciSerialNum = match.groups()[0]
                continue

        # append last object at end of loop
        try:
            if om.id:
                log.debug("Writing an interconnect %d" % icCount)
                rm.append(om)
        except:
            log.debug("Missing this one out since the last interconnect was invalid")

        log.info("Finished processing results, %d interconnects found" % icCount)

        return rm
