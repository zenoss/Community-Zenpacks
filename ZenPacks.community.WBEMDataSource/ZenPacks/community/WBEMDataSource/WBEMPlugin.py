################################################################################
#
# This program is part of the WBEMDataSource Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""WBEMPlugin

wrapper for PythonPlugin

$Id: WBEMPlugin.py,v 1.0 2009/07/31 21:29:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import CollectorPlugin
from WBEMClient import WBEMClient
from twisted.internet import defer

class WBEMPlugin(CollectorPlugin):
    """
    A WBEMPlugin defines a native Python collection routine and a parsing
    method to turn the returned data structure into a datamap. A valid
    WBEMPlugin must implement the process method.
    """
    transport = "python"
    deviceProperties = CollectorPlugin.deviceProperties + (
        'zWinUser',
        'zWinPassword',
        'zWbemPort',
        'zWbemProxy',
        'zWbemUseSSL',
    )
    

    def queries(self):
        raise NotImplementedError

    def collect(self, device, log):
        d = defer.maybeDeferred(WBEMClient(device).query, self.queries())
        return d

    def preprocess(self, results, log):
        if isinstance(results, Exception):
            log.error(results)
            return None
        return results




