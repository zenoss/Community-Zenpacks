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
CPUTempC
ambientTempC
memoryTempC
systemTempC
"""


class BladeTemps(CommandParser):
    
    
    def processResults(self, cmd, result):
        """
        Parse the results of the "SHOW SERVER TEMP #" command
        to get details about temperatures.
        """
        output = cmd.result.output
        
        dps = dict([(dp.id, dp) for dp in cmd.points])

        outlines = output.split('\n')
        log.debug("BladeTempsParser: I have %d lines to parse" % len(outlines))

        for line in outlines:
            if "System Zone" in line:
                bits = line.split()
                log.debug("BladeTempsParser: %s" % bits[3])
                result.values.append( (dps["systemTempC"], float(bits[3].split("C/")[0])) )
            if "CPU Zone" in line:
                bits = line.split()
                result.values.append( (dps["CPUTempC"], float(bits[3].split("C/")[0])) )
            if "Memory Zone" in line:
                bits = line.split()
                result.values.append( (dps["memoryTempC"], float(bits[3].split("C/")[0])) )
            if "Ambient Zone" in line:
                bits = line.split()
                result.values.append( (dps["ambientTempC"], float(bits[3].split("C/")[0])) )


        return result
