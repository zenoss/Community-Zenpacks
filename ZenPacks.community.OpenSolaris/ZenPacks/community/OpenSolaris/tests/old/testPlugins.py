import os

from Products.DataCollector.tests.BasePluginsTestCase \
        import BasePluginsTestCase

from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.memory \
        import memory
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.opensolaris_uname_a \
        import opensolaris_uname_a
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.process \
        import process
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.pkginfo \
        import pkginfo
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.cpu \
        import cpu
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.netstat_an \
        import netstat_an
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.netstat_r_vn \
        import netstat_r_vn
from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.ifconfig \
        import ifconfig

class OpenSolarisPluginsTestCase(BasePluginsTestCase):

    def runTest(self):
        """
        Test all of the plugins that have test data files in the data
        directory.
        """
        Plugins = [ ifconfig, netstat_r_vn,netstat_an,cpu,memory,opensolaris_uname_a,pkginfo,process]
        datadir = "%s/plugindata/Solaris" % (os.path.dirname(__file__))
        self._testDataFiles(datadir, Plugins)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(OpenSolarisPluginsTestCase))
    return suite

