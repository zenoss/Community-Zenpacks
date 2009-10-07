# -*- coding: utf-8 -*-
import os

from Products.DataCollector.tests.BasePluginsTestCase \
        import BasePluginsTestCase

from ZenPacks.community.Mandriva.modeler.plugins.zenoss.cmd.linux.mandriva_rpm \
        import mandriva_rpm

from ZenPacks.community.Mandriva.modeler.plugins.zenoss.cmd.linux.mandriva_uname_a \
        import mandriva_uname_a

class MandrivaLinuxPluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data
        directory.
        """
        Plugins = [mandriva_uname_a,mandriva_rpm]
        datadir = "%s/plugindata/linux" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(MandrivaLinuxPluginsTestCase))
    return suite

