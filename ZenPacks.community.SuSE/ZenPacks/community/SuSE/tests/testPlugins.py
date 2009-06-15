import os

from Products.DataCollector.tests.BasePluginsTestCase \
        import BasePluginsTestCase

from ZenPacks.community.SuSE.modeler.plugins.zenoss.cmd.linux.suse_rpm \
        import suse_rpm

from ZenPacks.community.SuSE.modeler.plugins.zenoss.cmd.linux.suse_uname_a \
        import suse_uname_a

class SuSELinuxPluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data
        directory.
        """
        Plugins = [suse_uname_a,suse_rpm]
        datadir = "%s/plugindata/linux" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(SuSELinuxPluginsTestCase))
    return suite

