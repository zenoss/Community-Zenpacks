###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2008, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################


import re
import logging

from Products.ZenRRD.CommandParser import CommandParser


log = logging.getLogger("zen.zencommand")

"""
Items to collect:
coolingStatus
enclosureStatus
OAStatus
powerAvailableDC
powerCapacityDC
powerPresentAC
powerStatus
"""


class EnclosureStatus(CommandParser):
    
    
    def processResults(self, cmd, result):
        """
        Parse the results of the "SHOW ENCLOSURE STATUS" command
        to get details about power usage and component status.
        """
        output = cmd.result.output
        
        dps = dict([(dp.id, dp) for dp in cmd.points])

        outlines = output.split('\n')
        log.debug("EnclosureStatusParser: I have %d lines to parse" % len(outlines))

        for i, line in enumerate(outlines):
            if "Enclosure" in line:
                if "OK" in outlines[i+1]:
                    result.values.append( (dps["enclosureStatus"], float(0)) )
                else:
                    result.values.append( (dps["enclosureStatus"], float(1)) )
            if "Onboard Administrator" in line:
                if "OK" in outlines[i+1]:
                    result.values.append( (dps["OAStatus"], float(0)) )
                else:
                    result.values.append( (dps["OAStatus"], float(1)) )
            if "Power Subsystem" in line:
                if "OK" in outlines[i+1]:
                    result.values.append( (dps["powerStatus"], float(0)) )
                else:
                    result.values.append( (dps["powerStatus"], float(1)) )
            if "Power" in line:
                log.debug("EnclosureStatusParser: Found line with Power in it: %s" % line)
                match = re.match("^([^:]+):.([0-9]+).Watts.*$", line.strip())
                if match:
                    log.debug("EnclosureStatusParser: Found line to match the regex: %s" % line)
                    (key, value) = match.groups()
                    if "Power Capacity" in key:
                        result.values.append( (dps["powerCapacityDC"], float(value)) )
                    if "Power Available" in key:
                        result.values.append( (dps["powerAvailableDC"], float(value)) )
                    if "Present Power" in key:
                        result.values.append( (dps["powerPresentAC"], float(value)) )
            if "Cooling Subsystem" in line:
                if "OK" in outlines[i+1]:
                    result.values.append( (dps["coolingStatus"], float(0)) )
                else:
                    result.values.append( (dps["coolingStatus"], float(1)) )

        return result
