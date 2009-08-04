################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""isql

ibmStatus parser Objects

$Id: isql.py,v 1.0 2009/07/21 01:26:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenRRD.CommandParser import CommandParser
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence


class ibmStatus(CommandParser):

    def processResults(self, cmd, result):
        statusmap = {'Unknown': 0,
                     'Other': 1,
                     'OK': 2,
		     'Degraded': 3,
		     'Stressed': 4,
		     'Predictive Failure': 5,
		     'Error': 6,
		     'Non-Recoverable Error': 7,
		     'Starting': 8,
		     'Stopping': 9,
		     'Stopped': 10,
		     'In Service': 11,
		     'No Contact': 12,
		     'Lost Communication': 13,
		     'Aborted': 14,
		     'Dormant': 15,
		     'Supporting Entity in Error': 16,
		     'Completed': 17,
		     'Power Mode': 18,
                    }
        output = cmd.result.output
        output = output.splitlines()[-1].strip('"')
        value = statusmap.get(output, 0)
        exitCode = cmd.result.exitCode
        severity = cmd.severity
        if exitCode == 0:
            severity = 0
        elif exitCode == 2:
            severity = min(severity + 1, 5)
        msg = 'Status: %s' % value
        result.events.append(dict(device=cmd.deviceConfig.device,
                                  summary=msg,
                                  severity=severity,
                                  message=msg,
                                  performanceData=value,
                                  eventKey=cmd.eventKey,
                                  eventClass=cmd.eventClass,
                                  component=cmd.component))

        result.values.append( (cmd.points[0], value) )

