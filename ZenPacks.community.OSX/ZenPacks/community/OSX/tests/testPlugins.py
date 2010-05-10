import os

from Products.DataCollector.tests.BasePluginsTestCase import BasePluginsTestCase

from ZenPacks.community.OSX.modeler.plugins.zenoss.cmd.osx.cpu import cpu
from ZenPacks.community.OSX.modeler.plugins.zenoss.cmd.osx.memory import memory
from ZenPacks.community.OSX.modeler.plugins.zenoss.cmd.osx.software import software
from ZenPacks.community.OSX.modeler.plugins.zenoss.cmd.osx.uname_a import uname_a

class OSXPluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data directory.
        """
        Plugins = [ uname_a, memory, cpu, software]
        datadir = "%s/plugindata/osx" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(OSXPluginsTestCase))
    return suite

