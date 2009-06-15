import os

from Products.DataCollector.tests.BasePluginsTestCase \
        import BasePluginsTestCase

from ZenPacks.community.Gentoo.modeler.plugins.zenoss.cmd.linux.eix \
        import eix

from ZenPacks.community.Gentoo.modeler.plugins.zenoss.cmd.linux.gentoo_uname_a \
        import gentoo_uname_a

class GentooLinuxPluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data
        directory.
        """
        Plugins = [gentoo_uname_a,eix]
        datadir = "%s/plugindata/linux" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(GentooLinuxPluginsTestCase))
    return suite

