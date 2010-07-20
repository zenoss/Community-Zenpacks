import os

from Products.DataCollector.tests.BasePluginsTestCase import BasePluginsTestCase

from ZenPacks.community.ChefClient.modeler.plugins.community.cmd.chef.cpu import cpu
from ZenPacks.community.ChefClient.modeler.plugins.community.cmd.chef.host import host
from ZenPacks.community.ChefClient.modeler.plugins.community.cmd.chef.memory import memory

class ChefClientPluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data directory.
        """
        Plugins = [ host, memory, cpu ]
        datadir = "%s/plugindata/chef" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ChefClientPluginsTestCase))
    return suite

