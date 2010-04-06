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

class BladeChassisFans(CommandPlugin):
    """
    Run show enclosure fans all on the OA to get details about the fans.
    """
    command = 'SHOW ENCLOSURE FAN ALL'
    relname = "bladechassisfans"
    modname = 'ZenPacks.community.HPBladeChassis.BladeChassisFan'

    def process(self, device, results, log):
        rm = self.relMap()
        log.info('Collecting Fan Information for device %s' % device.id)

        fanCount = 0 # keep track of what we've seen for various reasons


        resultslines = results.split("\n")
        for line in resultslines:
            match = re.match('^Fan.#([0-9]+).information:$', line.strip())
            if match:
                # First line of a fan detail section, create object and get started
                # If this isn't the first fan, we want to save the last one
                try:
                    if om.id:
                        log.debug("Writing a fan")
                        rm.append(om)
                except:
                    log.debug("Missing this one out since the last fan slot was empty")
                # Now create the new object and initalise it some
                # We set the snmpindex so that the collector is happy
                # Look here for empty interconenct bays
                if "<absent>" in match.groups()[0]:
                    om = None
                    continue
                om = self.objectMap()
                om.bcfNumber = int(match.groups()[0])
                om.snmpindex = om.bcfNumber
                om.id = self.prepId(om.bcfNumber)
                fanCount = fanCount + 1
                log.debug("Found a fan, processing fan %d with position %s" % (fanCount, om.bcfNumber))
                continue

            # Now look for the information we want, etc

            match = re.match('^Status:.(.*)$',line.strip())
            if match:
                om.bcfStatus = match.groups()[0]
                continue
            match = re.match('^Serial Number:.(.*)$',line.strip())
            if match:
                om.bcfSerialNum = match.groups()[0]
                continue
            match = re.match('^Product.Name:.(.*)$',line.strip())
            if match:
                om.bcfProductName = match.groups()[0]
                continue
            match = re.match('^Part.Number:.(.*)$',line.strip())
            if match:
                om.bcfPartNumber = match.groups()[0]
                continue
            match = re.match('^Spare.Part.Number:.(.*)$',line.strip())
            if match:
                om.bcfSparePartNumber = match.groups()[0]
                continue
            match = re.match('^Version:.(.*)$',line.strip())
            if match:
                om.bcfProductVersion = match.groups()[0]
                continue

        # append last object at end of loop
        try:
            if om.id:
                log.debug("Writing a fan entry")
                rm.append(om)
        except:
            log.debug("Not writing an invalid fan entry")

        log.info("Finished processing results, %d fans found" % fanCount)

        return rm
