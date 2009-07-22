import os

from Products.DataCollector.tests.BasePluginsTestCase \
        import BasePluginsTestCase

from ZenPacks.community.Ubuntu.modeler.plugins.zenoss.cmd.linux.ubuntu_aptitude \
        import ubuntu_aptitude

from ZenPacks.community.Ubuntu.modeler.plugins.zenoss.cmd.linux.ubuntu_uname_a \
        import ubuntu_uname_a

class UbuntuLinuxPluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data
        directory.
        """
        Plugins = [ubuntu_uname_a,ubuntu_aptitude]
        datadir = "%s/plugindata/linux" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(UbuntuLinuxPluginsTestCase))
    return suite
