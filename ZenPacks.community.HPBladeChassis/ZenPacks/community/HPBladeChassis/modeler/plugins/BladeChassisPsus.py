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

class BladeChassisPsus(CommandPlugin):
    """
    Run show enclosure powersupply all on the OA to get details.
    """
    command = 'SHOW ENCLOSURE POWERSUPPLY ALL'
    relname = "bladechassispsus"
    modname = 'ZenPacks.community.HPBladeChassis.BladeChassisPsu'

    def process(self, device, results, log):
        rm = self.relMap()
        log.info('Collecting Psu Information for device %s' % device.id)

        psuCount = 0 # keep track of what we've seen for various reasons


        resultslines = results.split("\n")
        for line in resultslines:
            match = re.match('^Power.Supply.#([0-9]+).Information:$', line.strip())
            if match:
                # First line of a psu detail section, create object and get started
                # If this isn't the first psu, we want to save the last one
                try:
                    if om.id:
                        log.debug("Writing a PSU entry")
                        rm.append(om)
                except:
                    log.debug("Not adding an empty PSU entry")
                # Now create the new object and initalise it some
                # We set the snmpindex so that the collector is happy

                om = self.objectMap()
                om.bcpNumber = int(match.groups()[0])
                om.snmpindex = om.bcpNumber
                om.id = self.prepId(om.bcpNumber)
                psuCount = psuCount + 1
                log.debug("Found a psu, processing psu %d with position %s" % (psuCount, om.bcpNumber))
                continue

            # Now look for the information we want, etc

            match = re.match('^Status:.(.*)$',line.strip())
            if match:
                if "Power Supply Bay Empty" in match.groups()[0]:
                    # don't do anything with this
                    om = None
                else:
                    om.bcpStatus = match.groups()[0]
                continue
            match = re.match('^Capacity:.(.*)$',line.strip())
            if match:
                om.bcpCapacity = match.groups()[0]
                continue
            match = re.match('^Serial Number:.(.*)$',line.strip())
            if match:
                om.bcpSerialNum = match.groups()[0]
                continue
            match = re.match('^Product.Name:.(.*)$',line.strip())
            if match:
                om.bcpProductName = match.groups()[0]
                continue
            match = re.match('^Part.Number:.(.*)$',line.strip())
            if match:
                om.bcpPartNumber = match.groups()[0]
                continue
            match = re.match('^Spare.Part.Number:.(.*)$',line.strip())
            if match:
                om.bcpSparePartNumber = match.groups()[0]
                continue
            match = re.match('^Product.Ver:.(.*)$',line.strip())
            if match:
                om.bcpProductVersion = match.groups()[0]
                continue

        # append last object at end of loop
        try:
            if om.id:
                log.debug("Writing a PSU entry")
                rm.append(om)
        except:
            log.debug("Not adding an empty PSU entry")

        log.info("Finished processing results, %d psus found" % psuCount)

        return rm
