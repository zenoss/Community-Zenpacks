################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OdbcPlugin

wrapper for PythonPlugin

$Id: OdbcPlugin.py,v 1.1 2009/11/11 13:26:23 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import CollectorPlugin
from OdbcClient import OdbcClient, CError
from twisted.internet import defer

class OdbcPlugin(CollectorPlugin):
    """
    A OdbcPlugin defines a native Python collection routine and a parsing
    method to turn the returned data structure into a datamap. A valid
    OdbcPlugin must implement the process method.
    """
    transport = "python"

    def queries(self, device):
        raise NotImplementedError

    def collect(self, device, log):
        d = defer.maybeDeferred(OdbcClient(device).query, self.queries(device))
        return d

    def preprocess(self, results, log):
        newres = {}
        for table, value in results.iteritems():
            if isinstance(value[0], CError):
                log.error(value[0].getErrorMessage())
                continue
	    newres[table] = value
        return newres




