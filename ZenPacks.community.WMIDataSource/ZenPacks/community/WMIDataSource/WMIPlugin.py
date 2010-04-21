################################################################################
#
# This program is part of the WMIDataSource Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WMIPlugin

wrapper for PythonPlugin

$Id: WMIPlugin.py,v 1.3 2010/04/21 18:39:13 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import CollectorPlugin
from twisted.python.failure import Failure
from WMIClient import WMIClient

class WMIPlugin(CollectorPlugin):
    """
    A WMIPlugin defines a native Python collection routine and a parsing
    method to turn the returned data structure into a datamap. A valid
    WMIPlugin must implement the process method.
    """
    transport = "python"
    deviceProperties = CollectorPlugin.deviceProperties + (
        'zWinUser',
        'zWinPassword',
        'zWmiProxy',
    )

    includeQualifiers = True
    tables = {}

    def queries(self, device = None):
        return self.tables

    def collect(self, device, log):
        return WMIClient(device).query(self.queries(device),
                                                        self.includeQualifiers)

    def preprocess(self, results, log):
        newres = {}
        for table, value in results.iteritems():
            if value != []:
                if isinstance(value[0], Failure):
                    log.error(value[0].getErrorMessage())
                    continue
            newres[table] = value
        return newres




