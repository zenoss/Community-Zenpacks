import os

from Products.DataCollector.tests.BasePluginsTestCase \
        import BasePluginsTestCase

from ZenPacks.community.Fedora.modeler.plugins.zenoss.cmd.linux.fedora_rpm \
        import fedora_rpm

from ZenPacks.community.Fedora.modeler.plugins.zenoss.cmd.linux.fedora_uname_a \
        import fedora_uname_a

class FedoraLinuxPluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data
        directory.
        """
        Plugins = [fedora_uname_a,fedora_rpm]
        datadir = "%s/plugindata/linux" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(FedoraLinuxPluginsTestCase))
    return suite

