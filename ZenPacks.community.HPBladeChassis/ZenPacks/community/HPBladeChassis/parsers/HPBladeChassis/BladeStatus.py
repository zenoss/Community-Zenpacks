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
bladeHealth
bladePowerConsumed
"""


class BladeStatus(CommandParser):
    
    
    def processResults(self, cmd, result):
        """
        Parse the results of the "SHOW ENCLOSURE STATUS" command
        to get details about power usage and component status.
        """
        output = cmd.result.output
        
        dps = dict([(dp.id, dp) for dp in cmd.points])

        outlines = output.split('\n')
        log.debug("BladeStatusParser: I have %d lines to parse" % len(outlines))

        for i, line in enumerate(outlines):
            match = re.match('^([^:]+):.(.*)$', line.strip())
            if match:
                (key, value) = match.groups()
                if "Health" in key:
                    if "OK" in value:
                        result.values.append( (dps["bladeHealth"], float(0)) ) 
                    else:
                        result.values.append( (dps["bladeHealth"], float(1)) )
                if "Current Wattage" in key:
                        result.values.append( (dps["bladePowerConsumed"], float(value)) )

        return result
