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

class BladeServers(CommandPlugin):
    """
    Run show server info all on the OA to get details about the blade.
    """
    command = 'SHOW SERVER INFO ALL'
    relname = "bladeservers"
    modname = 'ZenPacks.community.HPBladeChassis.BladeServer'

    def process(self, device, results, log):
        rm = self.relMap()
        log.info('Collecting Blade Servers for device %s' % device.id)

        bladeCount = 0 # keep track of what we've seen for various reasons


        resultslines = results.split("\n")
        for line in resultslines:
            match = re.match('^Server.Blade.#([0-9]+).Information:$', line.strip())
            if match:
                # First line of a blade detail section, create object and get started
                # If this isn't the first blade, we want to save the last one
                if bladeCount > 0:
                    rm.append(om)
                    # Save the hostname, so that if next blade is a storage blade
                    # We can tag it with it's host
                    oldHostName = om.bsDisplayName
                # Now create the new object and initalise it some
                # We set the snmpindex so that the collector is happy
                om = self.objectMap()
                om.bsPosition = int(match.groups()[0])
                om.snmpindex = om.bsPosition
                om.id = self.prepId("%s slot %2d" % (device.id, om.bsPosition))
                om.bsInstalledRam = 0
                om.bsCPUCount = 0
                bladeCount = bladeCount + 1
                log.debug("Found a blade header, processing blade %d with position %s" % (bladeCount, om.bsPosition))
                continue

            # Now look for the information we want, etc

            # First check, is the next line "no blade here"
            match = re.match('^Server.Blade.Type:.No.Server.Blade.Installed$', line.strip())
            if match:
                # We need to set a bunch of default values for "no blade here" and continue
                om.bsDisplayName = "Empty Slot"
                continue
            match = re.match('^Type:.((Server|Storage|Unknown).*)$',line.strip())
            if match:
                if "Storage" in match.groups()[0]:
                    om.bsDisplayName = oldHostName + " Storage Blade"
                if "Unknown" in match.groups()[0]:
                    om.bsDisplayName = "ERROR - Unrecognized Blade"
                continue
            match = re.match('^Product.Name:.(.*)$',line.strip())
            if match:
                # We set displayname to the product name, so that storage blades
                # turn up okay, for server blades Server Name will overwrite this
                om.bsProductId = match.groups()[0]
                continue
            match = re.match('^Part.Number:.(.*)$',line.strip())
            if match:
                om.bsPartNumber = match.groups()[0]
                continue
            match = re.match('^System.Board.Spare.Part.Number:.(.*)$',line.strip())
            if match:
                om.bsSystemBoardPartNum = match.groups()[0]
                continue
            match = re.match('^Serial Number:.(.*)$',line.strip())
            if match:
                om.bsSerialNum = match.groups()[0]
                continue
            match = re.match('^Server.Name:.(.*)$',line.strip())
            if match:
                om.bsDisplayName = match.groups()[0]
                continue
            match = re.match('^CPU.[0-9]:.(.*)$',line.strip())
            if match:
                om.bsCPUCount = om.bsCPUCount + 1
                om.bsCPUType = match.groups()[0]
                continue
            match = re.match('^Memory:.(.*).MB$',line.strip())
            if match:
                om.bsInstalledRam = int(match.groups()[0])
                continue
            match = re.match('^NIC.1.MAC.Address:.(.*)$',line.strip())
            if match:
                om.bsNic1Mac = match.groups()[0]
                continue
            match = re.match('^NIC.2.MAC.Address:.(.*)$',line.strip())
            if match:
                om.bsNic2Mac = match.groups()[0]
                continue
            match = re.match('^Firmware.Version:.(.*)$',line.strip())
            if match:
                om.bsIloFirmwareVersion = match.groups()[0]
                continue
            match = re.match('^IP Address:.(.*)$',line.strip())
            if match:
                om.bsIloIp = match.groups()[0]
                continue

        # append last object at end of loop
        if bladeCount > 0:
            rm.append(om)

        log.info("Finished processing results, %d blades found" % bladeCount)

        return rm
