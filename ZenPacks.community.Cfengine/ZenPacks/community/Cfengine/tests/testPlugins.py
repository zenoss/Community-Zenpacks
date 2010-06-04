import os

from Products.DataCollector.tests.BasePluginsTestCase import BasePluginsTestCase

from ZenPacks.community.Cfengine.modeler.plugins.community.cmd.cfenginemodeler import cfenginemodeler

class CfenginePluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data directory.
        """
        Plugins = [ cfenginemodeler ]
        datadir = "%s/plugindata/cfengine" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(CfenginePluginsTestCase))
    return suite

